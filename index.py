# index.py
import sys
from utils import file_exists
from indexfile import IndexFile
from btree import BTree

def main():
    index_file = None
    btree = None

    while True:
        print("Commands: create, open, insert, search, load, print, extract, quit")
        cmd = input("Enter command: ").strip().lower()

        if cmd == 'create':
            filename = input("Enter filename: ")
            if file_exists(filename):
                overwrite = input("File exists. Overwrite? (y/n): ").strip().lower()
                if overwrite != 'y':
                    continue
            index_file = IndexFile(filename)
            index_file.create_new(overwrite=True)
            btree = BTree(index_file)
            btree.initialize_empty_tree()

        elif cmd == 'open':
            filename = input("Enter filename: ")
            if not file_exists(filename):
                print("Error: File does not exist.")
                continue
            index_file = IndexFile(filename)
            if not index_file.open_existing():
                print("Error: Invalid index file.")
                index_file = None
                btree = None
                continue
            btree = BTree(index_file)
            btree.load_root()

        elif cmd == 'insert':
            if btree is None:
                print("No file open.")
                continue
            try:
                key = int(input("Enter key: "))
                value = int(input("Enter value: "))
            except ValueError:
                print("Invalid input.")
                continue
            if btree.search(key) is not None:
                print("Error: Key already exists.")
            else:
                btree.insert(key, value)

        elif cmd == 'search':
            if btree is None:
                print("No file open.")
                continue
            try:
                key = int(input("Enter key: "))
            except ValueError:
                print("Invalid input.")
                continue
            val = btree.search(key)
            if val is None:
                print("Key not found.")
            else:
                print(f"Found: {key}, {val}")

        elif cmd == 'load':
            if btree is None:
                print("No file open.")
                continue
            loadfile = input("Enter load filename: ")
            if not file_exists(loadfile):
                print("Load file does not exist.")
                continue
            with open(loadfile, 'r') as lf:
                for line in lf:
                    line = line.strip()
                    if not line:
                        continue
                    pair = line.split(',')
                    if len(pair) != 2:
                        print("Invalid line in load file.")
                        continue
                    try:
                        k, v = int(pair[0]), int(pair[1])
                    except ValueError:
                        print("Invalid integers in load file.")
                        continue
                    if btree.search(k) is not None:
                        print(f"Error: Key {k} already exists, skipping.")
                    else:
                        btree.insert(k, v)

        elif cmd == 'print':
            if btree is None:
                print("No file open.")
                continue
            btree.print_all()

        elif cmd == 'extract':
            if btree is None:
                print("No file open.")
                continue
            out_file = input("Enter output filename: ")
            if file_exists(out_file):
                overwrite = input("File exists. Overwrite? (y/n): ").strip().lower()
                if overwrite != 'y':
                    continue
            btree.extract_all(out_file)

        elif cmd == 'quit':
            if btree is not None:
                btree.close()
            break

        else:
            print("Unknown command.")

if __name__ == "__main__":
    main()