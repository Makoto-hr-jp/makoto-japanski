"""
@who:   Tomislav Mamić
@when:  13.06.2019.
@what:  automated generation of template lesson folders
@why:   manual file generation is tedious
"""
import re
import os

__subfolder = "lekcije"

"""
@what:  ID check
@why:   enforce naming rule - ID in {0..999}
"""
def __ID_valid(ID):
    try:
        ID = int(ID)
        return 0 <= ID <= 999
    except:
        return False

"""
@what:  name check
@why:   enforce naming rule - lesson names only contain lower-case letters, numbers and underscore
"""
__name_filt = re.compile("[^a-z0-9_]")
def __name_valid(name):
    return not re.search(__name_filt, name)

"""
@what:  group check
@why:   enforce naming rule - group may only be one of the 3 specified:
        0 - pocetni
        1 - srednji
        2 - napredni
"""
__groups = ["pocetni", "srednji", "napredni"]
def __group_valid(group):
    if group in __groups:
        return True
    try:
        group = int(group)
        return 0 <= group < len(__groups)
    except:
        return False

"""
@what:  top-level template generation
@why:   ease of use
"""
def generate_template(lesson_ID, lesson_name, group, author, title):
    if not __ID_valid(lesson_ID):
        raise Exception("Lesson ID must be a positive integer from {0..999}.")
    if not __name_valid(lesson_name):
        raise Exception("Lesson name may only contain lower-case letters, numbers and '_'.")
    if not __group_valid(group):
        raise Exception("Group may be either 'pocetni' (0), 'srednji' (1) or 'napredni' (2).")
    if type(author) is not str:
        raise Exception(f"'{author}' is a funny name!")
    if type(title) is not str:
        raise Exception(f"'{title}' is a funny title!")
    
    print("creating directory... ", end = "")
    g_folder = __groups[group] if type(group) is int else group
    ID = int(lesson_ID)
    ID = f"{ID:03}"
    l_folder = f"{ID}_{lesson_name}"
    folder = f"{g_folder}/{__subfolder}/{l_folder}"
    os.mkdir(folder)
    print("OK")
    
    print("generating templates...", end = "")
    with open("003_blank.tex") as f:
        source = f.read()
    source = source.replace("../../000_template.tex", "../../../000_template.tex")
    source = source.replace("{autor}", f"{{{author}}}")
    cin = source.replace("{naslov}", f"{{Ciljevi i napomene - {title}}}")
    lst = source.replace("{naslov}", f"{{{title}}}")
    dz = source.replace("{naslov}", f"{{Domaća zadaća - {title}}}")
    with open(f"{folder}/{ID}_ciljevi_i_napomene.tex", "w") as f:
        f.write(cin)
    with open(f"{folder}/{l_folder}.tex", "w") as f:
        f.write(lst)
    with open(f"{folder}/{ID}_DZ.tex", "w") as f:
        f.write(dz)
    print("OK")

    print("done.")
