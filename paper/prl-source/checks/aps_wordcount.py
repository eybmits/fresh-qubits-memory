"""Estimate the Letter length using the APS length-guide procedure.

Usage: python3 aps_wordcount.py memory_limits_prl.tex <figure-folder> [workdir] [-v]

The counting copy uses nofootinbib and omits the title block, displayed equations,
acknowledgments, and bibliography. CTAN wordcount.tex counts the typeset text;
APS equivalents are added for equations and figures. The actual manuscript is
never modified. This helper supports the single-column equation/align/gather
and one-PDF-per-figure layout used by this Letter, and rejects unsupported math
or tables rather than silently undercounting them. See:
https://journals.aps.org/authors/length-guide
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess


def run(command, work, *, input_text=None, log_name=None):
    result = subprocess.run(command, cwd=work, input=input_text,
                            capture_output=True, text=True, timeout=120)
    if log_name:
        (work / log_name).write_text(result.stdout + result.stderr)
    if result.returncode:
        raise RuntimeError(f"Command failed ({result.returncode}): {command!r}\n"
                           f"{(result.stdout + result.stderr)[-4000:]}")
    return result.stdout


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("figure_folder", type=Path)
    parser.add_argument("workdir", type=Path, nargs="?", default=Path("wc_work"))
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()
    source, figdir, work = (p.resolve() for p in
                           (args.source, args.figure_folder, args.workdir))
    if work == source.parent:
        raise ValueError("Use a separate work directory, not the source folder")
    work.mkdir(parents=True, exist_ok=True)
    original = source.read_text()
    # Comments must not contribute equation rows, figures, or premature markers.
    tex = re.sub(r"(?m)(?<!\\)%.*$", "", original)
    pre, body = tex.split(r"\begin{document}", 1)
    body = body[:body.index(r"\bibliography{refs}")]
    if re.search(r"\\begin\{(?:table\*?|widetext|eqnarray\*?|multline\*?)\}", body):
        raise ValueError("Tables or unsupported/wide equations require a separate APS count")
    if re.search(r"(?<!\\)\\\[", body) or "$$" in body:
        raise ValueError("Convert unnumbered display math to equation* before counting")
    equation = re.compile(r"\\begin\{(equation|align|gather)(\*?)\}(.*?)"
                          r"\\end\{\1\2\}", re.S)
    rows = sum(m.group(3).count(r"\\") + 1 for m in equation.finditer(body))
    counted_body = equation.sub("", body).replace(r"\maketitle", "")
    counted_body = re.sub(r"\\begin\{acknowledgments\}.*?\\end\{acknowledgments\}",
                          "", counted_body, flags=re.S)
    # The full Letter resolves citations and cross-references for the counting
    # pass, which reads its .aux without writing it (wordcount.tex uses nofiles).
    pre = re.sub(r"\\documentclass\[([^]]*)\]", lambda m:
                 r"\documentclass[" + m.group(1) + ",nofootinbib]", pre, count=1)
    pre = re.sub(r"\\graphicspath\{\{[^}]*\}\}", "", pre)
    pre += "\\graphicspath{{%s/}}\n" % figdir.as_posix()
    shutil.copyfile(source.parent / "refs.bib", work / "refs.bib")
    full = pre + r"\begin{document}" + body
    full += "\\bibliography{refs}\n\\end{document}\n"
    job = work / "letter_wc.tex"
    job.write_text(full)
    latex = ["pdflatex", "-interaction=nonstopmode", "-halt-on-error",
             "-no-shell-escape", "letter_wc.tex"]
    for index, command in enumerate((latex, ["bibtex", "letter_wc"], latex, latex), 1):
        run(command, work, log_name=f"pass-{index}.txt")
    full_log = (work / "letter_wc.log").read_text(errors="replace")
    if re.search(r"(?:Citation|Reference) .* undefined|There were undefined", full_log):
        raise RuntimeError("Unresolved references in the full-Letter counting precursor")

    # REVTeX otherwise inserts a bibliography automatically at enddocument, even
    # after the explicit bibliography command was removed and with nofootinbib.
    no_auto_bibliography = r"\makeatletter\let\auto@bib\@empty\makeatother"
    job.write_text(pre + r"\begin{document}" + counted_body + "\n"
                   + no_auto_bibliography + "\n\\end{document}\n")
    # Do not use -interaction=nonstopmode here: wordcount.tex reads its filename
    # with \read-1, which requires the normal interaction mode and stdin.
    run(["pdflatex", "-no-shell-escape", "wordcount.tex"], work,
        input_text="letter_wc.tex\n", log_name="wordcount-run.txt")
    log = (work / "wordcount.log").read_text(errors="replace").splitlines()
    errors = [line for line in log if line.startswith("!")]
    if errors:
        raise RuntimeError("TeX errors in counting pass: " + "\n".join(errors))
    spaces = sum(bool(re.search(r"3\.0863[3-9]", line)) and "3.08632" not in line
                 for line in log)
    chars = sum(bool(re.search(r"3\.0863[2-9]", line)) for line in log)
    if spaces == 0:
        raise RuntimeError("No wordcount.tex word markers found")

    figures = []
    for match in re.finditer(r"\\begin\{figure(\*?)\}(.*?)\\end\{figure\1\}",
                             counted_body, flags=re.S):
        names = re.findall(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]*)\}", match.group(2))
        if len(names) != 1:
            raise ValueError("Each figure must use one complete PDF for aspect-ratio counting")
        name = names[0]
        info = run(["pdfinfo", str(figdir / name)], work)
        size = re.search(r"Page size:\s+([\d.]+) x ([\d.]+)", info)
        if size is None:
            raise ValueError(f"Cannot determine PDF size: {name}")
        width, height = map(float, size.groups())
        aspect = width / height
        words = 600 / aspect + 40 if match.group(1) else 150 / aspect + 20
        figures.append({"file": name, "double_column": bool(match.group(1)),
                        "width_pt": width, "height_pt": height,
                        "aspect_ratio": aspect, "word_equivalent": words})
    figure_words = sum(f["word_equivalent"] for f in figures)
    total = spaces + 16 * rows + figure_words
    report = {"method": "APS length guide with CTAN wordcount.tex",
              "guide_url": "https://journals.aps.org/authors/length-guide",
              "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
              "typeset_words": spaces, "characters_including_spaces": chars,
              "displayed_equation_rows": rows, "equation_word_equivalent": 16 * rows,
              "figures": figures, "figure_word_equivalent": figure_words,
              "total_word_equivalent": total, "total_rounded": round(total),
              "prl_limit": 3750, "tex_errors": []}
    (work / "count.json").write_text(json.dumps(report, indent=2) + "\n")
    print(f"typeset words (wordcount.tex): {spaces}   (characters incl. spaces: {chars})")
    print(f"displayed equations: {rows} rows -> {16 * rows} words")
    print(f"figures: {round(figure_words)} words")
    print(f"TOTAL: {round(total)}   (PRL limit 3750)")
    if args.verbose:
        seq = []
        for line in log:
            match = re.search(r"\\3\.08632 (.)", line)
            if match:
                seq.append(match.group(1))
            elif re.search(r"3\.0863[3-9]", line) and "3.08632" not in line:
                seq.append("|")
        print("".join(seq))


if __name__ == "__main__":
    main()
