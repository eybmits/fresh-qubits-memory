#!/usr/bin/env python3
"""Render the current administrative cover letter; never contact a portal."""

import json
import os
from pathlib import Path
import subprocess
import tempfile


REPO = Path(__file__).resolve().parents[1]
ADMIN = REPO / "paper/submission-admin/prl-2026-10-18"
HEADINGS = {"Main result", "Why Physical Review Letters", "Materials and declarations"}


def tex(text):
    replacements = {
        "\\": r"\textbackslash{}", "&": r"\&", "%": r"\%", "$": r"\$",
        "#": r"\#", "_": r"\_", "{": r"\{", "}": r"\}",
        "~": r"\textasciitilde{}", "^": r"\textasciicircum{}",
        "Θ": r"\ensuremath{\Theta}", "’": "'", "“": "``", "”": "''",
    }
    escaped = "".join(replacements.get(c, c) for c in text)
    return escaped.replace(
        r"exp[\ensuremath{\Theta}(k)]", r"\ensuremath{\exp[\Theta(k)]}"
    ).replace(r"\ensuremath{\Theta}(log T)", r"\ensuremath{\Theta(\log T)}")


def main():
    body = (ADMIN / "cover_letter_body.txt").read_text().strip()
    referees = json.loads((ADMIN / "referees.json").read_text())
    text_sections = []
    tex_sections = []
    for key, title in (("suggested", "Suggested referees"), ("alternates", "Alternate referees")):
        text_sections.append(title)
        tex_sections.append(r"\coverheading{" + title + "}")
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
    sender = paragraphs[0].splitlines()
    header = (
        r"\begin{minipage}[t]{0.78\textwidth}"
        + r"{\sffamily\bfseries\fontsize{15}{18}\selectfont " + tex(sender[0]) + "}\\\\[4pt]\n"
        + r"{\fontsize{9}{11}\selectfont "
        + "\\\\\n".join(tex(line) for line in sender[1:])
        + r"}\end{minipage}\hfill\begin{minipage}[t]{0.20\textwidth}\raggedleft"
        + r"\fontsize{9}{11}\selectfont Munich\\October 18, 2026\end{minipage}"
        + r"\par\vspace{8pt}{\color{rulegray}\hrule height 0.5pt}\vspace{12pt}"
    )
    rendered = []
    for paragraph in paragraphs[2:]:
        if paragraph in HEADINGS:
            rendered.append(r"\coverheading{" + tex(paragraph) + "}")
        else:
            rendered.append("\\\\\n".join(tex(line) for line in paragraph.splitlines()))
    rendered_body = header + "\n\n" + "\n\n".join(rendered)
    source = r"""\documentclass[11pt,a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{lmodern}
\usepackage[a4paper,top=19mm,bottom=19mm,left=22mm,right=22mm]{geometry}
\usepackage{microtype}
\usepackage{xcolor}
\definecolor{rulegray}{gray}{0.65}
\newcommand{\coverheading}[1]{\par\addvspace{7pt}\noindent{\sffamily\bfseries\fontsize{10.5}{13}\selectfont #1}\par\nobreak\vspace{1pt}}
\usepackage[hidelinks]{hyperref}
\input{glyphtounicode}\pdfgentounicode=1
\hypersetup{pdftitle={Cover Letter - PRL Submission},pdfauthor={Markus Baumann}}
\pdfinfoomitdate=1\pdftrailerid{}\pdfsuppressptexinfo=15
\setlength{\parindent}{0pt}\setlength{\parskip}{6pt}
\pagestyle{empty}
\begin{document}
\fontsize{11}{13.5}\selectfont
""" + rendered_body + r"""
\newpage
\fontsize{10.5}{12.5}\selectfont
{\sffamily\bfseries\fontsize{15}{18}\selectfont Referee suggestions}\hfill Markus Baumann et al.\\[4pt]
The Fundamental Memory Ceiling of Noisy Quantum Reservoirs
\par\vspace{7pt}{\color{rulegray}\hrule height 0.5pt}\vspace{5pt}
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
