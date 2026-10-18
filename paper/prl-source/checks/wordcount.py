"""Word count of the Letter according to the APS length guide (journals.aps.org/authors/length-guide):
Total = Text + Displayed math + Figures + Tables, limit 3750 words for PRL.
  Text: main body including captions and footnotes; not counted: title, byline, abstract, references,
        acknowledgments (the data-availability statement is counted here, to be conservative).
  Displayed math (two-column layout, single-column equation): 16 words per row.
  Figures: single column 150/aspect + 20, two-column 300/(0.5*aspect) + 40 (aspect = width/height).
Usage: python3 wordcount.py ../tex/memory_limits_prl.tex ../figs"""
import re, sys, subprocess, os

tex = open(sys.argv[1]).read()
tex = re.sub(r"(?m)(?<!\\)%.*$", "", tex)                  # comments are not printed
figdir = sys.argv[2]
main = tex[tex.index(r"\maketitle"):tex.index(r"\begin{acknowledgments}")]
das = tex[tex.index(r"\runin{Data availability.}"):tex.index(r"\bibliography{refs}")]
abstract = tex[tex.index(r"\begin{abstract}") + 16:tex.index(r"\end{abstract}")]

# ---- figures: captions count as text, the figure itself by its aspect ratio
figs = re.findall(r"\\begin\{figure(\*?)\}.*?\\includegraphics(?:\[[^\]]*\])?\{([^}]*)\}.*?\\caption\{(.*?)\}\s*\\label",
                  main, flags=re.S)
captions = [c for _, _, c in figs]
fig_words = 0
fig_report = []
for star, name, _ in figs:
    path = os.path.join(figdir, name)
    info = subprocess.run(["pdfinfo", path], capture_output=True, text=True).stdout
    w, h = map(float, re.search(r"Page size:\s+([\d.]+) x ([\d.]+)", info).groups())
    asp = w / h
    words = 300 / (0.5 * asp) + 40 if star else 150 / asp + 20
    fig_words += words
    fig_report.append((name, round(w / 72, 2), round(h / 72, 2), round(asp, 3), round(words)))
body = re.sub(r"\\begin\{figure\*?\}.*?\\end\{figure\*?\}", " ", main, flags=re.S)

# ---- displayed math: 16 words per row
eqs = re.findall(r"\\begin\{(equation|align|gather)\*?\}(.*?)\\end\{\1\*?\}", body, flags=re.S)
rows = sum(e.count(r"\\") + 1 for _, e in eqs)
body = re.sub(r"\\begin\{(equation|align|gather)\*?\}.*?\\end\{\1\*?\}", " ", body, flags=re.S)


def count_words(s):
    s = re.sub(r"\$[^$]*\$", " MATH ", s)                # inline math = one word
    s = re.sub(r"\\nocite\{[^}]*\}", " ", s)               # not printed
    s = re.sub(r"~?\\cite\{[^}]*\}", " [REF] ", s)          # a citation = one word
    s = re.sub(r"\\(eq)?ref\{[^}]*\}", "N", s)
    s = re.sub(r"\\(runin|emph|textbf|textit|label|caption)\{", " ", s)
    s = re.sub(r"\\label\{[^}]*\}", " ", s)
    s = re.sub(r"\\[a-zA-Z]+\*?(\[[^\]]*\])?", " ", s)
    s = re.sub(r"[{}\\~]", " ", s)
    s = s.replace("---", " ")
    return len([w for w in s.split() if re.search(r"[A-Za-z0-9\[]", w)])


text_words = count_words(body)
cap_words = sum(count_words(c) for c in captions)
das_words = count_words(das)
math_words = 16 * rows
total = text_words + cap_words + das_words + math_words + fig_words
print("abstract characters (plain text approx.):", len(re.sub(r"\s+", " ", re.sub(r"\$|\\", "", abstract)).strip()))
print("text (body, theorem)     %5d" % text_words)
print("captions                 %5d" % cap_words, [count_words(c) for c in captions])
print("data availability        %5d" % das_words)
print("displayed math  %2d rows  %5d" % (rows, math_words))
for f in fig_report:
    print("figure %-10s %4.2f x %4.2f in, aspect %.3f -> %d words" % f)
print("figures                  %5d" % fig_words)
print("TOTAL                    %5d   (limit 3750)" % total)
