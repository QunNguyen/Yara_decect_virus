import subprocess
import re
import platform
import os

os_name = platform.system()
if(os_name == 'Windows') :
    tasklist = subprocess.check_output(['tasklist']).decode('utf-8')
    print(tasklist)
    pattern = r"notepad\.exe\s+(\d+)"
    matches = re.findall(pattern, tasklist)
    if matches:
        pid = int(matches[0])
        subprocess.call(['taskkill', '/F', '/PID', str(pid)])
        print(pid)
else:
    ps_output = subprocess.check_output(['ps', '-A']).decode('utf-8')
    pattern = r"^\s*(\d+)\s+.*firefox.*$"
    matches = re.findall(pattern, ps_output, re.MULTILINE)
    if matches:
        pid = int(matches[0])
        os.kill(pid, 9)