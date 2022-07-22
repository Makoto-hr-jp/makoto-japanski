"""
@what:  Kanji dictionary compiler - create .tex files from parsed kanji dictionaries.
@why:   Step in automated dictionary generation.
@who:   Tomislav Mamić
@when:  2021-08-14
"""

import re
from subprocess import Popen
import kdict

DEFAULT_TEMPLATE = "./kdict_output/template.tex"
DEFAULT_OUTPUT = "./kdict_output/"

CHAR_REMAPS = {"~": "\\textasciitilde "}

def process_special_chars(segment: str) -> str:
    ret = segment
    for old, new in CHAR_REMAPS.items():
        ret = ret.replace(old, new)
    return ret

def example_to_tex(example: dict) -> str:
    return (f"\\example{{{example['kanji']}}}"
            f"{{{example['reading']}}}"
            f"{{{example['meaning']}}}")

def kanji_to_tex(kanji: str, examples: list) -> str:
    """Aggregate examples for each kanji."""
    entry = [f"\\begin{{dictentry}}{{{kanji}}}"]
    entry += [example_to_tex(ex) for ex in examples]
    entry.append(f"\\end{{dictentry}}")

    return "\n".join(entry)

def insert_footnote_mark(field: str, num: int, uid: int) -> str:
    """Replace a footnote placeholder with tex footnote mark."""
    return re.sub(f"\<{num}\>", fr"\\footnotemark[{uid}]", field)

def update_footnote_marks(ex: dict, num: int, uid: int):
    """Update kanji description with footnote marks."""
    for field in kdict.FN_FIELDS:
        ex[field] = insert_footnote_mark(ex[field], num, uid)

def make_unique_footnotes(content: dict) -> dict:
    """Aggregate identical footnotes from all kanji descriptions and correct their references."""
    unique = {}
    cur_mark = 1
    for _, examples in content.items():
        for example in examples:
            for fn, num in example["footnotes"].items():
                if fn in unique:
                    update_footnote_marks(example, num, unique[fn])
                else:
                    unique[fn] = cur_mark
                    update_footnote_marks(example, num, cur_mark)
                    cur_mark += 1
    return unique

def content_to_tex(content: dict) -> str:
    """Aggregate content output for each entry."""
    footnotes = make_unique_footnotes(content)
    print(footnotes)

    content = [kanji_to_tex(kanji, examples) for kanji, examples in content.items()]

    # add unique footnotes
    for fn, uid in footnotes.items():
        content.append(f"\\footnotetext[{uid}]{{{fn}}}")

    return "\n\n".join(content)

def make_tex(lesson: int, content: dict, template=DEFAULT_TEMPLATE, output=DEFAULT_OUTPUT):
    """Make lesson tex."""
    lnum = f"{lesson}".zfill(3)
    print(lnum)
    cdump = content_to_tex(content)
    with open(template, encoding="utf-8") as f:
        raw = f.read()
    out = raw.replace("@LNUM", lnum)
    out = out.replace("@CONTENT", cdump)
    out = process_special_chars(out)
    outname = output+f"kdict_{lnum}.tex"
    with open(outname, "w", encoding="utf-8") as f:
        f.write(out)
    return outname

DEFAULT_OPTS = ["-synctex=0",
                "-interaction=nonstopmode",
                "-aux-directory=../tex_aux",
                "-output-directory=./release"]
def compile_tex(texpath: str):
    """Tex compiler for convenience."""
    cproc = Popen(["xelatex", texpath] + DEFAULT_OPTS)
    pipes = cproc.communicate()
    print(pipes)

if __name__ == "__main__":
    data = kdict.parse_sources(kdict.SOURCES)
    for lesson, content in data.items():
        texname = make_tex(lesson, content)
        compile_tex(texname)