# gitmerge-cleanup
Script to clean up git merge blocks in `entity.json` files that were improperly 
committed into a DDR repo. Point the script at a directory containing a repo 
with bad `entity.json` files.

Usage:

$ python gitmerge-cleanup.py ./PATH_TO_REPO ./OUTPUTPATH

NOTE: The script will retain the HEAD content, and remove the other conflicting lines. 
