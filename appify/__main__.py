'''
	This is a utility to search for .desktop files and create desktop entries.
	Copyright (C) 2021  Rohit T P

	This program is free software: you can redistribute it and/or modify
	it under the terms of the GNU Affero General Public License as published
	by the Free Software Foundation, either version 3 of the License, or
	(at your option) any later version.

	This program is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU Affero General Public License for more details.

	You should have received a copy of the GNU Affero General Public License
	along with this program.  If not, see https://www.gnu.org/licenses/
'''
import sys
from pathlib import Path
from os.path import join
from subprocess import run
from enquiries import choose


def getAbsolute(path, root):
    '''
        Converts a path relative to root to absolute path.
    '''
    path = Path(path).expanduser()

    if path.is_absolute():
        return path

    path = join(Path(root).absolute(), path)
    if not Path(path).is_file():
        return None

    return path


def phrase_desktop_file(lines, desktop_file):
    '''
        Replaces relative paths in desktop file with absolute paths. 
    '''
    root = desktop_file.parent

    for line in lines:
        if line.startswith("Exec="):
            exe = getAbsolute(line[5:-1].rstrip("\n"), root)
            eline = lines.index(line)
        elif line.startswith("Icon="):
            ico = getAbsolute(line[5:-1].rstrip("\n"), root)
            iline = lines.index(line)

    if not exe:
        print(f"Error : Exec missing in {desktop_file}")
        return False

    if not ico:
        print(f"Warning : Icon missing in {desktop_file}")

    lines[eline] = f"Exec={exe}\n"
    lines[iline] = f"Icon={ico}\n"

    return lines


def add_entry(desktop_file):
    '''
        Adds the phrased .desktop file to applications folder.
    '''
    with desktop_file.open(mode="r", newline="\n") as opened_file:
        lines = opened_file.readlines()

    edited_file = phrase_desktop_file(lines, desktop_file)

    if not edited_file:
        return False

    new_desktop_file = Path(join(
        Path.home(),
        ".local/share/applications/",
        Path(desktop_file).name
    ))

    with new_desktop_file.open(mode="w", newline="\n") as new_file:
        new_file.writelines(lines)

    return True


def get_desktop_files(root):
    '''
        Searches for .desktop file in given folder recursively.
    '''
    files = set([])

    for path in root.rglob("*.desktop"):
        if path.is_file():
            files.add(str(path))

    return files


def main():
    '''
        This function is called to start Appify.
    '''
    try:
        search_folder = Path(sys.argv[1])
    except IndexError:
        print("No search path provided.")
        return 5

    if not search_folder.exists():
        print(f"{str(search_folder)} does not exist.")
        return 1

    desktop_files = get_desktop_files(search_folder)

    if len(desktop_files) == 0:
        print(f"No .desktop files found in {search_folder}")
        return 2

    selected_files = choose(
        prompt="Select the apps you want to add.",
        choices=get_desktop_files(search_folder),
        multi=True
    )

    if len(selected_files) == 0:
        print("No files selected")
        return 3

    done = 0

    for file in selected_files:
        if add_entry(Path(file)):
            done += 1

    print(f"Moved {done} files")

    run([
        "update-desktop-database",
        join(Path.home(), ".local/share/applications/")
    ])


if __name__ == "__main__":
    main()
