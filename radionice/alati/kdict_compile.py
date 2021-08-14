"""
@what:  Kanji dictionary compiler - create .tex files from parsed kanji dictionaries.
@why:   Step in automated dictionary generation.
@who:   Tomislav Mamić
@when:  2021-08-14
"""

from subprocess import Popen
import kdict

DEFAULT_TEMPLATE = "./kdict_output/template.tex"
DEFAULT_OUTPUT = "./kdict_output/"

def example_to_tex(example: dict) -> str:
    return f"\\example{{{example['kanji']}}}{{{example['reading']}}}{{{example['meaning']}}}"

def kanji_to_tex(kanji: str, examples: list) -> str:
    """Aggregate examples for each kanji."""
    entry = [f"\\begin{{dictentry}}{{{kanji}}}"]
    entry += [example_to_tex(ex) for ex in examples]
    entry.append(f"\\end{{dictentry}}")

    return "\n".join(entry)

def content_to_tex(content: dict) -> str:
    """Aggregate content output for each entry."""
    return "\n\n".join((kanji_to_tex(kanji, examples) for kanji, examples in content.items()))

def make_tex(lesson: int, content: dict, template=DEFAULT_TEMPLATE, output=DEFAULT_OUTPUT):
    """Make lesson tex."""
    lnum = f"{lesson}".zfill(3)
    cdump = content_to_tex(content)
    with open(template, encoding="utf-8") as f:
        raw = f.read()
    out = raw.replace("@LNUM", lnum)
    out = out.replace("@CONTENT", cdump)
    outname = output+f"kdict_{lnum}.tex"
    with open(outname, "w", encoding="utf-8") as f:
        f.write(out)
    return outname

DEFAULT_OPTS = ("-synctex=0",
                "-interaction=nonstopmode",
                "-aux-directory=../tex_aux",
                "-output-directory=./release")
def compile_tex(texpath: str):
    """Tex compiler for convenience."""
    cproc = Popen(["xelatex", texpath] + list(DEFAULT_OPTS))

if __name__ == "__main__":
    data = kdict.parse_sources(kdict.SOURCES)
    for lesson, content in data.items():
        texname = make_tex(lesson, content)
        compile_tex(texname)