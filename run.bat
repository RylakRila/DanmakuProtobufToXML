@echo off
python.exe ./main.py {oid} {date}
if %errorlevel%==0 echo The file is stored at /output folder.
pause
