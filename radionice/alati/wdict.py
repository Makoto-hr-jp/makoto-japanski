"""
@what:  Word dictionary parser - convert provisional text file format to word entry objects.
@why:   Step in automated dictionary generation.
@who:   Tomislav Mamić
@when:  2022-06-17
"""

# built-in
import re

SOURCE = "./data/rijeci_pocetna.html"
TR_REGEX = re.compile(r"<tr>(.*?)</tr>", re.DOTALL)

def extract_table_rows(path: str) -> "list[str]":
    with open(path, encoding="utf-8") as src:
        return re.findall(TR_REGEX, src.read())

def main():
    pass

if __name__ == "__main__":
    main()