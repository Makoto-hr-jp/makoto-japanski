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
__author = re.compile(r"\\author{(.*?)}")
__id = re.compile(r"([0-9]{3})")
__package = re.compile(r"(\\usepackage.*?$)", re.MULTILINE)
def parse_lesson(file):
    data = {}
    with open(file, encoding = "utf-8") as f:
        content = f.read()
    data['title'] = re.findall(__title, content)[0]
    data['ID'] = int(re.findall(__id, file)[0])
    data['authors'] = [x.strip() for x in re.findall(__author, content)[0].split(",")]
    data['packages'] = re.findall(__package, content)
    return data

"""
@what:  create lesson dictionaries which contain the data necessary
        for book generation
@why:   used to actually generate the book latex
"""
def get_lesson_data(top_folder):
    candidates = gather_lesson_folders(top_folder)

    # check if each dir contains a .tex with the same name
    lesson_files = []
    for c in candidates:
        target = f"{c}/{c}.tex"
        if os.path.isfile(top_folder + target):
            lesson_files.append(target)
        else:
            print(f"Folder '{c}' does not contain a .tex file with the same name!")

    # for each lesson, generate a dictionary with basic data
    lessons = [{**parse_lesson(top_folder + p), **{'path': p}} for p in lesson_files]
    lessons = sorted(lessons, key = lambda p: p['ID'])
    return lessons

"""
@what:  generate book .tex file
@why:   that's our goal
"""
__banned_elements = ["\\author", "\\input", "!TeX", "{document}", "\\usepackage"]
banned = lambda line: True if True in [x in line for x in __banned_elements] else False
def generate_book(top_folder, title = "Skripta"):
    # extend top folder with slash if needed
    if top_folder[-1] not in ['\\', '/']:
        top_folder += '/'

    # parse lesson files
    lessons = get_lesson_data(top_folder)

    # gather unique added packages and authors
    unique_packages = []
    unique_authors = {}
    for l in lessons:
        for a in l['authors']:
            if a in unique_authors:
                unique_authors[a] += 1
            else:
                unique_authors[a] = 1

        for p in l['packages']:
            if p not in unique_packages:
                unique_packages.append(p)
    author = ", ".join(sorted(unique_authors))

    # write book preamble
    book = f"{__compiler_settings}\n"
    book += "\\input{../../006_uvez.tex}\n"
    # add missing packages
    for p in unique_packages:
        book += p + '\n'

    # add book title and author data
    book += f"\\title{{{title}}}\n"
    book += f"\\author{{{author}}}\n"

    # open book body
    book += "\\begin{document}\n\n"
    book += "{\\let\\cleardoublepage\clearpage\n\\maketitle\n\\tableofcontents}\n"

    # merge filtered lesson text
    for l in lessons:
        book += f"\\newpage\n\\fakesection{{{l['ID']:03}: {l['title']}}}\n\n"
        with open(top_folder + l['path'], 'r', encoding = "utf-8") as f:
            for line in f.readlines():
                if not banned(line):
                    book += line

    # close book body
    book += "\\end{document}\n"

    # print book to file
    with open(top_folder + "book.tex", 'w', encoding = "utf-8") as f:
        f.write(book)
    return lessons

d = generate_book(top_folder = "pocetni/lekcije", title = "Skripta\\\\\n\\large za početnu grupu japanskog\\\\\nMakoto")
