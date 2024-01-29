import os
import re
import json

class SnippetsPageManager:
    lstOptions = [{
			"name":"Retour",
			"target":"homePage:none",
		}
    ]

    def __init__(self, scr):
        self.toRoute:str = None
        self.selectedCallBack = None
        self.selectedClbkName = ""
        self.scr = scr
        self.snippets = {}
        with open("snippets.json", 'r') as f:
            for snippet in json.load(f):
                self.snippets[snippet["title"]] = {
                    title:snippet["title"],
                    command:snippet["command"]
                }

    def getClBkName(self):
        return self.selectedClbkName
    
    def executeSnippet(self, snippetName:str):
        self.scr.clear()
        self.scr.put_text("Executing",0,5)
        self.scr.put_text("snippet...",0,20)
        self.scr.put_text(snippetName,0,35)
        self.scr.redraw()
        cmd = os.popen(self.snippets[snippetName]["command"])
        results = cmd.readlines()
        if cmd.errors:
            self.scr.clear()
            self.scr.put_text("Error",0,5)
            self.scr.put_text("Executing",0,20)
            self.scr.put_text("snippet...",0,35)
            self.scr.put_text(snippetName,0,50)
            self.scr.redraw()
            sleep(2)
        cmd.close()
        self.drawListOptions(0)

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

        for snippet in self.snippets:
            self.scr.put_text(snippet["title"],0,posYItem)
            posYItem += 15

        self.scr.redraw()
