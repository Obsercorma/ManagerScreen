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

    def setData(self, params:list[str]):
        self.repoName = params[0]
        print(self.repoName)

    def getClBkName(self):
        return self.selectedClbkName

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
        self.scr.put_text(f"V:X.X.X",0,posYItem)
        posYItem+=15
        self.scr.put_text(f"S:Online",0,posYItem)
        posYItem+=15
        self.scr.put_text(f"W:0 E:0",0,posYItem)
        self.scr.redraw()

