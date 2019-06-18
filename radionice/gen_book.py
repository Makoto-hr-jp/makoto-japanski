"""
@who:   Tomislav Mamić
@when:  18.06.2019.
@what:  automated generation of book format from a folder containing lessons
@why:   manual file generation is tedious
"""
import re
import os

"""
@what:  gather lesson file names from corresponding top-level folders
@why:   collecting lesson data
"""
def gather_lessons(top_folder):
    _, dirs, _ = next(os.walk(top_folder))
    for d in dirs:
        print(d)

gather_lessons("pocetni/lekcije")
