# Development Log

## 2024-12-06 09:00
**Before Session:**  
**a. Thoughts so far:**  
I have a good grasp of the project’s requirements. We have the basic file structure in place and a working skeleton for the B-Tree operations. The create, open, and quit commands seem fine. I’m feeling confident but I know the insert and search operations still need thorough testing.

**b. Plan for this session:**  
- Implement the insert command fully, including handling splits.
- Test insertions with various keys and ensure the B-Tree properties hold.
- Add some preliminary error handling for user input.

**During Session Notes:**  
While coding insert logic, ran into a small off-by-one error when positioning keys during node splits. Fixed it by carefully indexing keys in _split_child.  
Added a few test cases: inserted keys 1 through 50 and printed them out. The tree splits as expected.

## 2024-12-06 11:30
**After Session Reflection:**  
I accomplished the main goal: insert now works and I tested it with multiple values. I managed to fix some indexing issues in the node splitting logic. I didn’t add much error handling yet, but I did ensure invalid inputs in insert produce a clear error message. Next session, I plan on focusing on the search and load commands.

## 2024-12-07 09:00
**Before Session:**  
**a. Thoughts so far:**  
The insert logic is stable. I realize I should confirm that the B-Tree is being stored and loaded correctly from the file by reopening the file after multiple inserts. No major new thoughts, just feeling confident about moving forward.

**b. Plan for this session:**  
- Implement and test the search command thoroughly.
- Implement the load command to bulk insert from a CSV file.
- Verify the file format by creating a new index file, inserting values, closing, then reopening and searching again.

**During Session Notes:**  
Implemented search. Found a small bug where if a key is larger than all keys in a node, I must ensure the correct child pointer is followed.  
The load command now reads a file and inserts pairs. Tested with a small data.csv file.  
Re-opened the index file after closing and verified that searching still works.

## 2024-12-07 11:45
**After Session Reflection:**  
I successfully implemented search and load. Testing search shows correct results for keys present and proper error messages for missing keys. Loading from a CSV file worked after ensuring the file uses UTF-8 encoding. Next session, I’ll focus on the print and extract commands. I may also start adding more robust error handling.

## 2024-12-08 10:00
**Before Session:**  
**a. Thoughts so far:**  
The core functionality (create, open, insert, search, load) is now working. I’m feeling good about the code structure. One concern is ensuring that no more than three nodes are in memory at once. I’ll verify that and add comments to explain the caching mechanism.

**b. Plan for this session:**  
- Implement the print command to print all keys in sorted order.
- Implement the extract command to save all keys/values to a file.
- Double-check the node caching to ensure we never exceed three nodes in memory.
- Write additional comments for maintainability.

**During Session Notes:**  
Inorder traversal for print works correctly after testing with various keys.  
Extract writes out a CSV file of all key/value pairs. Tested with a file of 100 inserted keys.  
Confirmed the caching logic: after adding a fourth node, it flushes the least recently used node. Added extra debug logs and comments.

## 2024-12-08 12:15
**After Session Reflection:**  
I accomplished all the goals for today. The print and extract commands work well. The node caching logic is in place and documented. The project feels complete. Next time, I might just do some final polish, more extensive testing, and consider adding a help command or more graceful error messages. I’m satisfied with the current state.