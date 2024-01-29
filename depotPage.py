import os
import re

class DepotPageManager:
    lstOptions = [{
			"name":"Retour",
			"target":"gitPage:none",
		}
    ]

    def __init__(self, scr):
        self.toRoute:str = None
        self.selectedCallBack = None
        self.selectedClbkName = ""
        self.scr = scr
        self.repoName = "nil"
        self.folderRepo = "nil"

    def setData(self, params:list[str]):
        self.repoName = params[0]
        self.folderRepo = params[1]
        print(self.repoName, self.folderRepo)

    def getClBkName(self):
        return self.selectedClbkName
    
    def getVersionProject(self):
        cmd = os.popen(f"""ssh -T git@192.168.1.4 -i /home/techrusse/.ssh/id_rsa.pub 'cd {self.folderRepo}/ && git show HEAD:VERSION'""")
        results = cmd.readlines()
        cmd.close()

        version_number = None
        # Extract the version number using regular expressions
        for line in results:
            version_number = re.search(r"^(\d\.?){3,}", line)
            if version_number is not None:
                return version_number.string.split("\x1b")[0]
        return version_number

    def getOption(self, clbkName:str) -> dict:
        for opt in self.lstOptions:
            if opt["target"].split(":")[0] == clbkName:
                return opt
        else:
            return {}

    def drawListOptions(self, pos_encoder:int):
        posYItem = 15
        self.scr.put_text(self.repoName,0,5)
        for option in range(0,len(self.lstOptions)):
            if pos_encoder == option:
                self.selectedClbkName = self.lstOptions[option]["target"]
                self.scr.fill_rect(0,posYItem,5,(posYItem+10))
                self.scr.put_text(self.lstOptions[option]["name"],10,(posYItem+3))
            else:
                self.scr.rect(0,posYItem,5,(posYItem+10))
                self.scr.put_text(self.lstOptions[option]["name"],10,(posYItem+3))
            posYItem += 15
        posYItem+=15
        self.scr.put_text(f"V:{self.getVersionProject()}",0,posYItem)
        # posYItem+=15
        # self.scr.put_text(f"S:Online",0,posYItem)
        # posYItem+=15
        # self.scr.put_text(f"W:0 E:0",0,posYItem)
        self.scr.redraw()

