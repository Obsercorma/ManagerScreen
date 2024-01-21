import os
import re

def getVersionProject():
    cmd = os.popen("ssh -t git@192.168.1.4 'cd ManagerScreen.git/ ; git show HEAD:VERSION'")
    results = cmd.readlines()[1:]
    cmd.close()

    version_number = None
    # Extract the version number using regular expressions
    for line in results:
        version_number = re.match(r"(\d\.?){3}", line)
        if version_number is not None:
            return version_number.string
    return version_number
    

print(f"VERSION: {getVersionProject()}")