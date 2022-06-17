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

FIELDS = [{'name': "lekcija", 'mandatory': False},
          {'name': "prirodno", 'mandatory': True},
          {'name': "čitanje", 'mandatory': False},
          {'name': "vrsta", 'mandatory': True},
          {'name': "prijevod", 'mandatory': True},
          {'name': "napomena", 'mandatory': False}]

def extract_table_rows(path: str) -> "list[str]":
    with open(path, encoding="utf-8") as src:
        return re.findall(TR_REGEX, src.read())

def extract_row_fields(row: str) -> "list[str]":
    data = BeautifulSoup(row)
    ret = []
    for td in data.find_all("td"):
        ret.append(td.get_text())
    return ret

def check_rows(rows: "list[str]") -> None:
    for row in rows:
        if len(row) != len(FIELDS):
            print(f"Field number mismatch ({row}).")
        for field, content in zip(FIELDS, row):
            if field['mandatory'] and not content:
                print(f"Empty mandatory field {field['name']} ({row}).")

def main():
    rows = extract_table_rows(SOURCE)
    rfields = []
    for idx, row in enumerate(rows):
        fields = extract_row_fields(row)
        rfields.append(fields)
    check_rows(rfields)

if __name__ == "__main__":
    main()