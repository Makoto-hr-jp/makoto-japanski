"""
@what:  Word dictionary parser - convert provisional text file format to word entry objects.
@why:   Step in automated dictionary generation.
@who:   Tomislav Mamić
@when:  2022-06-17
"""

# external
from bs4 import BeautifulSoup

# built-in
import re

SOURCE = "./data/rijeci_pocetna.html"
TR_REGEX = re.compile(r"<tr>(.*?)</tr>", re.DOTALL)

def extract_table_rows(path: str) -> "list[str]":
    with open(path, encoding="utf-8") as src:
        return re.findall(TR_REGEX, src.read())

def extract_row_fields(row: str) -> "list[str]":
    data = BeautifulSoup(row)
    ret = []
    for td in data.find_all("td"):
        ret.append(td.get_text())
    return ret

def main():
    rows = extract_table_rows(SOURCE)
    for idx, row in enumerate(rows):
        fields = extract_row_fields(row)
        print(idx, fields)

if __name__ == "__main__":
    main()