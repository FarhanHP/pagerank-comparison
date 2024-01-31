import os, sys

commands = [
    f"pdflatex {sys.argv[1]}.tex",
    f"bibtex {sys.argv[1]}.tex",
    f"pdflatex {sys.argv[1]}.tex",
    f"pdflatex {sys.argv[1]}.tex"
]

for c in commands:
    os.system(c)