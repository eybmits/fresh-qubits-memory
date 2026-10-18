#!/usr/bin/env python3
"""Render the current administrative cover letter; never contact a portal."""

import json
import os
from pathlib import Path
import subprocess
import tempfile


REPO = Path(__file__).resolve().parents[1]
ADMIN = REPO / "paper/submission-admin/prl-2026-10-18"


def tex(text):
    replacements = {
        "\\": r"\textbackslash{}", "&": r"\&", "%": r"\%", "$": r"\$",
        "#": r"\#", "_": r"\_", "{": r"\{", "}": r"\}",
        "~": r"\textasciitilde{}", "^": r"\textasciicircum{}",
        "Θ": r"\ensuremath{\Theta}", "’": "'", "“": "``", "”": "''",
    }
    return "".join(replacements.get(c, c) for c in text)


def main():
    body = (ADMIN / "cover_letter_body.txt").read_text().strip()
    referees = json.loads((ADMIN / "referees.json").read_text())
    text_sections = []
    tex_sections = []
    for key, title in (("suggested", "Suggested referees"), ("alternates", "Alternate referees")):
        text_sections.append(title)
        tex_sections.append(r"\section*{" + title + "}")
        for ref in referees[key]:
            lines = [ref["name"], ref["affiliation"], ref["email"]]
            if ref.get("expertise"):
                lines.append(ref["expertise"])
            text_sections.append("\n".join(lines))
            tex_sections.append(
                r"\begin{samepage}\textbf{" + tex(lines[0]) + "}\\\\\n"
                + "\\\\\n".join(tex(line) for line in lines[1:])
                + "\n\\end{samepage}\\par\\vspace{5pt}"
            )
    text_sections.append("Excluded referees: none.")
    tex_sections.append("Excluded referees: none.")
    referee_text = "\n\n".join(text_sections) + "\n"
    (ADMIN / "cover_letter.txt").write_text(body + "\n\n" + referee_text)
    with_sources = referee_text + "\nVerified institutional sources (checked October 18, 2026):\n"
    for ref in referees["suggested"] + referees["alternates"]:
        with_sources += "\n" + ref["name"] + "\n" + "\n".join(ref["sources"]) + "\n"
    with_sources += "\n" + referees["verification_scope"] + "\n"
    (ADMIN / "referees.txt").write_text(with_sources)
    paragraphs = body.split("\n\n")
    rendered_body = "\n\n".join("\\\\\n".join(tex(line) for line in p.splitlines()) for p in paragraphs)
    source = r"""\documentclass[11pt,a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{lmodern}
\usepackage[a4paper,top=17mm,bottom=17mm,left=20mm,right=20mm]{geometry}
\usepackage{microtype}
\usepackage[hidelinks]{hyperref}
\input{glyphtounicode}\pdfgentounicode=1
\hypersetup{pdftitle={Cover Letter - PRL Submission},pdfauthor={Markus Baumann}}
\pdfinfoomitdate=1\pdftrailerid{}\pdfsuppressptexinfo=15
\setlength{\parindent}{0pt}\setlength{\parskip}{6pt}
\pagestyle{empty}
\begin{document}
\fontsize{10.5}{12.5}\selectfont
""" + rendered_body + r"""
\newpage
\fontsize{10.5}{12.5}\selectfont
\textbf{Referee suggestions}\hfill Markus Baumann et al.\\
The Fundamental Memory Ceiling of Noisy Quantum Reservoirs
\vspace{3pt}
""" + "\n\n".join(tex_sections) + "\n\\end{document}\n"
    environment = os.environ.copy()
    environment.update(SOURCE_DATE_EPOCH="1792281600", FORCE_SOURCE_DATE="1", TZ="UTC")
    with tempfile.TemporaryDirectory(prefix="prl-cover-") as temporary:
        directory = Path(temporary)
        (directory / "cover_letter.tex").write_text(source)
        for _ in range(2):
            result = subprocess.run(
                ["pdflatex", "-no-shell-escape", "-interaction=nonstopmode", "-halt-on-error", "cover_letter.tex"],
                cwd=directory, env=environment, text=True, stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT, timeout=60,
            )
            if result.returncode:
                raise RuntimeError(result.stdout[-8000:])
        log = (directory / "cover_letter.log").read_text()
        if "Overfull" in log:
            raise RuntimeError("Cover letter has an overfull box; inspect layout before delivery")
        (ADMIN / "cover_letter.pdf").write_bytes((directory / "cover_letter.pdf").read_bytes())
    print(ADMIN / "cover_letter.pdf")


if __name__ == "__main__":
    main()
