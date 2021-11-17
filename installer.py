#!/bin/python3
import subprocess
import os
import shutil
class color:
    def red(self,name):
        print(f"\033[91m{name}\033[0m")
    def pink(self,name):
        print(f"\033[95m{name}\033[0m")
    def yellow(self,name):
        print(f"\033[93m{name}\033[0m")
    def bright(self,name):
        print(f"\033[1;32;40m{name}\033[0m")
    def blue(self,name):
        print(f"\033[1;32;34m{name}\033[0m")
    def cyan(self,name):
        print(f"\033[1;32;36m{name}\033[0m")
    def green(self,name):
        print(f"\033[92m{name}\033[0m")
colour=color()
check_root=subprocess.run("id",shell=True,capture_output=True)
if "root" not in str(check_root).lower():
        colour.red("Please run as root!!")
        os._exit(0)
try:
        shutil.rmtree("/opt/PyIntruder")
except:
        pass

try:
        os.system("pip3 install -r requirements.txt")
        colour.green("Creating files")
        os.system("mkdir /opt/PyIntruder")
        os.system("cp PyIntruder.py ShowJson.py PyI.png /opt/PyIntruder")
        os.system("chmod +x /opt/PyIntruder/PyIntruder.py")
except:

        colour.red("File not found!")
        os._exit(0)
os.system("touch /usr/share/applications/PyIntruder.desktop")
text="""[Desktop Entry]
Version=1.0
Type=Application
Name=PyIntruder
GenericName=PyIntruder
Comment=Powerful Intruder written in python by Yash and Sagnik H
Categories=Web Application Analysis;Network
Exec=/bin/PyIntruder
Icon=/opt/PyIntruder/PyI.png
Path=/bin
Terminal=false
StartupNotify=false
"""
colour.green("Creating shotcuts")
with open("/usr/share/applications/PyIntruder.desktop","w+") as f:
        f.write(text)
bash="""#!/bin/bash
python3 /opt/PyIntruder/PyIntruder.py"""
with open("/bin/PyIntruder","w+") as f2:
        f2.write(bash)
os.system("chmod +x /bin/PyIntruder /usr/share/applications/PyIntruder.desktop")
colour.yellow("Successfully installed !")
os.system("PyIntruder")
colour.blue("Enter `PyIntruder` command to run")
