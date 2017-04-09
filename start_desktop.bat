set PYTHONPATH=%CD%
if EXIST installed (
    start pythonw desktop\main.py
    exit
) else (
    start python desktop\main.py
)