# 🐚 Bash

- Rename all .ext files to sequential numbers in folder.
`$ ls -v | cat -n | while read n f; do mv -n "$f" "$n.ext"; done`
