Write a script that refreshes all static files. Call it statictools.py. Store in project_root/static/

Steps:
- Walk through all of static dir recursively and do an mtime check on each file.
- Store result in file_status.txt.
- If a new file is found, add the absolute path and mtime into file_status.
- Each line will have: abspath, mtime, and hash of the time at which the script is started.
- At the end of the operation, delete the lines that have old time hashes.
- Update 

Use a context processor to add version numbers to templates.  Store info where?  In what form (json, pickle, dictionary)?


Use MD5 hash to detect file changes. Creates a MD5 hash txt file in the static folder if one does not exist.

Args:
1. --refresh_cache = deletes files in the _collected_static folder and run ./manage.py collectstatic.
2. --templates = checks to make sure that templates

Keep app templates in their respective folders.  keep index.html and base.html in main templates folder.
