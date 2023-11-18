from time import sleep
from st7920 import ST7920
import asyncio
import RPi.GPIO as GPIO

stateProcess = True
pos_encoder = 0
state_chencoder = 0
selectedCallBack = None

CLK = 17
SW = 27
DT = 18
PWR_ENC = 24

GPIO.setmode(GPIO.BCM)
GPIO.setup(PWR_ENC, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(CLK, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(DT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(SW, GPIO.IN, pull_up_down=GPIO.PUD_UP)

clk_last_state = GPIO.input(CLK)

def gitHome():
	scr.put_text("Depots Git",0,5)
	scr.redraw()

def goBack():
	pass

def repoPage():
	pass

lstOptions = [
    {
        "name":"Retour",
        "clbk":goBack
    },
    {
        "name":"Portfolio",
        "clbk":repoPage,
        "target":"git:portfolio"
    },
    {
        "name":"ArteBot",
        "clbk":repoPage,
        "target":"git:artebot"
    }
]

def drawListOptions():
	global pos_encoder, lstOptions
	posYItem = 15
	for option in range(0,len(lstOptions)):
		if pos_encoder == option:
			selectedCallBack = lstOptions[option]["clbk"]
			scr.fill_rect(0,posYItem,5,(posYItem+10))
			scr.put_text(lstOptions[option]["name"],10,(posYItem+3))
		else:
			scr.rect(0,posYItem,5,(posYItem+10))
			scr.put_text(lstOptions[option]["name"],10,(posYItem+3))
		posYItem += 15
	scr.redraw()

async def encoder_process():
	global clk_last_state, pos_encoder, state_chencoder
	tmp_pos = pos_encoder
	while stateProcess:
		if tmp_pos != pos_encoder:
			scr.clear()
			scr.redraw()
			gitHome()
			drawListOptions()
			tmp_pos = pos_encoder
			#await asyncio.sleep(0.1)
		clk_state = GPIO.input(CLK)
		dt_state = GPIO.input(DT)
		if clk_state != clk_last_state:
			if dt_state != clk_state:
				state_chencoder += 1
				pos_encoder += 1 if (pos_encoder<(len(lstOptions)-1) and (state_chencoder%2)==0) else 0
				print("Rotation dans le sens horaire")
			else:
				state_chencoder -= 1
				pos_encoder -= 1 if (pos_encoder>0 and (state_chencoder%2)==0) else 0
				print("Rotation dans le sens antihoraire")
			print(pos_encoder)
		if GPIO.input(SW) == GPIO.LOW:
			print("Bouton enfoncé")
		clk_last_state = clk_state
		await asyncio.sleep(0.01)  # Délai court pour éviter les rebonds

try:
	if __name__ == "__main__":
		scr = ST7920()
		scr.set_rotation(3)
		scr.clear()
		scr.redraw()
		sleep(0.1)
		gitHome()
		drawListOptions()
		asyncio.run(encoder_process())
except KeyboardInterrupt:
	stateProcess = False
	print("Stopping...")
finally:
	scr.close()
	GPIO.cleanup()

