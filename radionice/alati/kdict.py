"""
@what:  Kanji dictionary parser - convert provisional text file format to kanji objects.
@why:   Step in automated dictionary generation.
@who:   Tomislav Mamić
@when:  2021-08-14
"""

import os
import re
import json

SOURCES = "./data/"

LEKCIJA = re.compile(r"([0-9]+)\.\s*lekcija\s*\n")
KANJI = re.compile(r"\-([\w\~\<\>]+)\s*\n")
EXAMPLE = re.compile(r"\-\-([\w\~\<\>]+),\s*(.+?):\s*(.*)\n")

def parse_kanji(entry: str) -> list:
    """Parse an individual entry."""
    ret = []
    for exp in re.findall(EXAMPLE, entry):
        new_ex = {"kanji": exp[0].strip(),
                  "reading": exp[1].strip(),
                  "meaning": exp[2].strip()}
        ret.append(new_ex)
    return ret

def get_kanji(seg_content: str) -> dict:
    """Split raw lesson content into individual character entries and process each one."""
    ret = {}
    entries = [entry for entry in re.split(KANJI, seg_content) if entry]
    for kanji, desc in zip(entries[::2], entries[1::2]):
        ret[kanji] = parse_kanji(desc)
    return ret

def get_segments(raw: str) -> dict:
    """Split raw string input into lesson segments and process each one."""
    segments = [seg for seg in re.split(LEKCIJA, raw) if seg]
    ret = {}
    # a list of <num><content> pairs is expected, otherwise something went wrong
    for segnum, content in zip(segments[::2], segments[1::2]):
        ret[segnum] = get_kanji(content)
    return ret

def parse_file(path: str):
    """Transform file content to python structures describing kanji entries."""
    print(f"Parsing {path}...")
    with open(path, encoding="utf-8") as src:
        raw = src.read() + "\n"
    ret = get_segments(raw)
    print(f"Found lessons: {list(ret.keys())}")
    return ret

def parse_sources(top: str):
    """Process all files in folder tree starting from top."""
    total_data = {}
    for dir, _, files in os.walk(top):
        for file in files:
            if not file.endswith(".txt"):
                continue
            data = parse_file(dir + file)
            total_data.update(data)
            dumpname = dir + file.split(".")[0] + ".json"
            with open(dumpname, "w", encoding="utf-8") as dump:
                json.dump(data, dump, indent=2, ensure_ascii=False)
    return total_data

if __name__ == "__main__":
    print(parse_sources(SOURCES))
