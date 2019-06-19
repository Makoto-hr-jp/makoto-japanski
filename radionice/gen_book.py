"""
@who:   Tomislav Mamić
@when:  18.06.2019.
@what:  automated generation of book format from a folder containing lessons
@why:   manual file generation is tedious
"""
import re
import os

__compiler_settings = ("% !TeX program = xelatex ?me "
                       "-synctex=0 "
                       "-interaction=nonstopmode "
                       "-aux-directory=../tex_aux "
                       "-output-directory=./release")

"""
@what:  gather lesson file names from corresponding top-level folders
@why:   collecting lesson data
"""
__leading_num = re.compile("^[0-9]{3}_")
def gather_lesson_folders(top_folder):
    _, dirs, _ = next(os.walk(top_folder))
    return [d for d in dirs if re.search(__leading_num, d)]

"""
@what:  parse lesson file and create a dictionary with its data
@why:   content table generation
"""
__title = re.compile(r"\\dai{(.*?)}")
__id = re.compile(r"([0-9]{3})")
def parse_lesson(file):
    data = {}
    with open(file, encoding = "utf-8") as f:
        content = f.read()
    data['title'] = re.findall(__title, content)[0]
    data['ID'] = int(re.findall(__id, file)[0])
    data['path'] = file
    return data

"""
@what:  create lesson dictionaries which contain the data necessary
        for book generation
@why:   used to actually generate the book latex
"""
def get_lesson_data(top_folder):
    candidates = gather_lesson_folders(top_folder)
    if top_folder[-1] not in ['\\', '/']:
        top_folder += '/'

    # check if each dir contains a .tex with the same name
    lesson_files = []
    for c in candidates:
        target = f"{top_folder}{c}/{c}.tex"
        if os.path.isfile(target):
            lesson_files.append(target)
        else:
            print(f"Folder '{c}' does not contain a .tex file with the same name!")

    # for each lesson, generate a dictionary with basic data
    lessons = [parse_lesson(p) for p in lesson_files]
    lessons = sorted(lessons, key = lambda p: p['ID'])
    return lessons

"""
@what:  generate book .tex file
@why:   that's our goal
"""
def generate_book(top_folder):
    lessons = get_lesson_data(top_folder)

lessons = get_lesson_data("pocetni/lekcije")
