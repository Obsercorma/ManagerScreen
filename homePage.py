#from time import sleep
#from st7920 import ST7920
#import asyncio
#import RPi.GPIO as GPIO

#stateProcess = True
#pos_encoder = 0
#selectedCallBack = None

#CLK = 17
#SW = 27
#DT = 18
#PWR_ENC = 24
#
#GPIO.setmode(GPIO.BCM)
#GPIO.setup(PWR_ENC, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#GPIO.setup(CLK, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#GPIO.setup(DT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#GPIO.setup(SW, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#
#clk_last_state = GPIO.input(CLK)

class HomePageManager:
	lstOptions = [
		{
			"name":"Git",
			"target":"gitPage:none",
			"isVisible":True
		},
		{
			"name":"Snippets",
			"isVisible":True,
			"target":"snippetsPage:none"
		}
	]

	def __init__(self, scr):
		self.toRoute:str = None
		self.selectedClbkName = ""
		self.scr = scr

	def setData(self, params:list[str]):
		pass

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
		self.scr.put_text("Home",0,5)
		visibleOptions = [opt for opt in range(0,len(self.lstOptions)) if self.lstOptions[opt]["isVisible"]]
		for option in visibleOptions:
			if pos_encoder == option:
				self.selectedClbkName = self.lstOptions[option]["target"]
				self.scr.fill_rect(0,posYItem,5,(posYItem+10))
				self.scr.put_text(self.lstOptions[option]["name"],10,(posYItem+3))
			else:
				self.scr.rect(0,posYItem,5,(posYItem+10))
				self.scr.put_text(self.lstOptions[option]["name"],10,(posYItem+3))
			posYItem += 15
			self.scr.redraw()

if __name__ == "__main__":
	try:
		scr = ST7920()
		scr.set_rotation(3)
		scr.clear()
		scr.redraw()
		sleep(0.1)
		showHome()
		asyncio.run(encoder_process())
	except KeyboardInterrupt:
		stateProcess = False
		print("Stopping...")
	finally:
		scr.close()
		GPIO.cleanup()
