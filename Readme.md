# B-Tree Index File Manager

This project provides an interactive program for managing index files that store B-Trees of minimal degree 10. It allows the user to create, open, insert, search, load, print, and extract key/value pairs stored in the B-Tree, as well as quit the program. The data is stored in a binary file with 512-byte blocks, and nodes are represented using a fixed-size format as specified.

## Features

- **Create**: Create a new index file with the correct header and an empty B-Tree.
- **Open**: Open an existing index file and validate its integrity.
- **Insert**: Insert a key/value pair into the B-Tree. If the key exists, print an error.
- **Search**: Search for a key and print its value if found.
- **Load**: Bulk insert key/value pairs from a CSV file.
- **Print**: Print all key/value pairs in sorted order by key.
- **Extract**: Save all key/value pairs to a CSV file.
- **Quit**: Close the currently open file and exit the program.

## File Structure

- `index.py`: Main program that handles user input and commands.
- `btree.py`: Implements B-Tree operations such as insert, search, and traversal.
- `node.py`: Defines the Node class for B-Tree nodes and handles reading/writing nodes.
- `indexfile.py`: Manages the index file including the header block and allocating new blocks.
- `utils.py`: Provides helper functions, constants, and endianness conversions.
- `devlog.md`: Development log file. You should maintain this log as you work on and test the program.
- `README.md`: This file.

## Requirements

- Python 3.x
- No external libraries required
- Code is designed to work on Linux-like environments

## Instructions

1. **Initialization**:
   - Clone or create your project directory.
   - Place all provided files (`index.py`, `btree.py`, `node.py`, `indexfile.py`, `utils.py`, `devlog.md`, `README.md`) in the project directory.
   - Initialize a git repository if needed:
     ```
     git init
     ```

2. **Development Log**:
   - Update `devlog.md` before and after each coding session.
   - Document any changes, issues encountered, and plans for subsequent sessions.

3. **Running the Program**:
   - Run:
     ```
     python3 index.py
     ```
   - Available commands:
     - `create`
     - `open`
     - `insert`
     - `search`
     - `load`
     - `print`
     - `extract`
     - `quit`

4. **Example Usage**:
   - Create a new index:
     ```
     create
     Enter filename: myindex.idx
     ```
   - Insert a key/value pair:
     ```
     insert
     Enter key: 10
     Enter value: 100
     ```
   - Search for a key:
     ```
     search
     Enter key: 10
     ```
   - Print all key/value pairs:
     ```
     print
     ```
   - Extract to CSV file:
     ```
     extract
     Enter output filename: output.csv
     ```
   - Quit:
     ```
     quit
     ```

5. **Node Caching Limit**:
   - The program maintains a maximum of three nodes in memory at once.
   - Uses a simple least recently used (LRU) mechanism. When a fourth node is needed, the least recently used node is written to disk and removed from memory.

6. **Endianness and Data Format**:
   - All integers are stored as 8-byte big-endian values.
   - Each block is 512 bytes with unused space padded.

## Notes

- Test thoroughly to confirm all operations behave correctly.
- If any issues arise, review the code, especially around file operations, endianness conversions, and B-Tree logic.
- Keep `devlog.md` updated as you work.

## License

This project is provided as is for educational purposes.