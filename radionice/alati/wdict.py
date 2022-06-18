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
from dataclasses import dataclass

SOURCE = "./data/rijeci_pocetna.html"
TR_REGEX = re.compile(r"<tr>(.*?)</tr>", re.DOTALL)

FIELDS = [{'name': "lekcija", 'mandatory': False},
          {'name': "riječ", 'mandatory': True},
          {'name': "čitanje", 'mandatory': False},
          {'name': "vrsta", 'mandatory': True},
          {'name': "značenje", 'mandatory': True},
          {'name': "napomena", 'mandatory': False}]

@dataclass
class Entry:
    lekcija: str
    riječ: str
    čitanje: str
    vrsta: str
    značenje: str
    napomena: str

    def __repr__(self) -> str:
        riječ = f"{self.riječ}" + (f" ({self.čitanje})" if self.čitanje else "")
        objašnjenje = f"{self.značenje}" + (f" ({self.napomena})" if self.napomena else "")
        return (f" lekcija: {self.lekcija}\n"
                f"   riječ: {riječ} "
                f"[{self.vrsta}]\n"
                f"značenje: {objašnjenje}")

def extract_table_rows(path: str) -> "list[str]":
    with open(path, encoding="utf-8") as src:
        return re.findall(TR_REGEX, src.read())

def extract_row_fields(row: str) -> "list[str]":
    data = BeautifulSoup(row)
    ret = []
    for td in data.find_all("td"):
        ret.append(td.get_text())
    return ret

def check_rows(rows: "list[Entry]", log=None) -> None:
    for row in rows:
        for field in FIELDS:
            if field['mandatory'] and not getattr(row, field['name']):
                output = f"Empty mandatory field '{field['name']}' in\n{row}"
                print(output)
                if log:
                    print(output, file=log)

def main():
    rows = extract_table_rows(SOURCE)
    rfields = {}
    cur_sect = ""
    # assumptions
    #   1. first entry starts with a section
    #   2. sections are not fragmented
    for row in rows:
        fields = extract_row_fields(row)
        if fields[0]:
            cur_sect = fields[0]
            rfields[cur_sect] = []
        else:
            fields[0] = cur_sect
        entry_data = Entry(*fields)
        rfields[cur_sect].append(entry_data)

    logname = ".".join(SOURCE.split(".")[:-1]) + ".log"
    with open(logname, "w", encoding="utf-8") as log:
        for sect, content in rfields.items():
            check_rows(content, log)

if __name__ == "__main__":
    main()