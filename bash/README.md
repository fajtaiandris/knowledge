# 🐚 Bash

- Batch replace in the names of the files in the folder.
`$ rename 's/this/that/g' *`
- Rename all .ext files to sequential numbers in folder.  
`$ ls -v | cat -n | while read n f; do mv -n "$f" "$n.ext"; done`
