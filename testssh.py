import os
import re

def getVersionProject():
    cmd = os.popen(f"ssh -t git@192.168.1.4 'cd PortfolioMythologicArte.git/ ; git show HEAD:VERSION'")
    results = cmd.readlines()
    cmd.close()

    print(results)

    version_number = None
    # Extract the version number using regular expressions
    for line in results:
        version_number = re.search(r"^(\d\.?){3,}", line)
        if version_number is not None:
            return version_number.string.split("\x1b")[0]
    return version_number
    

print(f"VERSION: {getVersionProject()}")