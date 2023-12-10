from time import sleep, time
from st7920 import ST7920
import asyncio
import RPi.GPIO as GPIO
from gitPage import GitPageManager
from depotPage import DepotPageManager
from homePage import HomePageManager
from snippetsPage import SnippetsPageManager

stateProcess = False
pos_encoder = 0
state_chencoder = 0
selectedCallBack = None
selectedClbkName:list[str] = []

currentPage = "homePage"
defaultPage = "homePage"
pageOptions = {
    "homePage":HomePageManager,
    "gitPage":GitPageManager,
    "depotPage":DepotPageManager,
    "snippetsPage":SnippetsPageManager
}
scr = ST7920()
scr.set_rotation(1)
for page in pageOptions.items():
    pageOptions[page[0]] = pageOptions[page[0]](scr)

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

async def encoder_process():
    global clk_last_state, pos_encoder, state_chencoder, pageOptions, currentPage, selectedClbkName, defaultPage
    tmp_pos = pos_encoder
    #selectedClbkName = pageOptions[currentPage].getClBkName().split(":")
    with open("process.txt", 'r') as f:
        if f.read().strip() == "start":
            stateProcess = True
    startingTime = time()
    while stateProcess:
        if (time() - startingTime) > 2.0:
            with open("process.txt", 'r') as f:
                if f.read().strip() == "stop":
                    stateProcess = False
                    startingTime = time()
                    print("Stopping process...")
                    break
        if tmp_pos != pos_encoder:
            scr.clear()
            scr.redraw()
            pageOptions[currentPage].drawListOptions(pos_encoder)
            #if (clbkName:=pageOptions[currentPage].getClBkName()) != selectedClbkName:
            #    selectedClbkName = clbkName.split(":")
            # gitHome()
            # drawListOptions()
            tmp_pos = pos_encoder
            #await asyncio.sleep(0.1)
        clk_state = GPIO.input(CLK)
        dt_state = GPIO.input(DT)
        if clk_state != clk_last_state:
            if dt_state != clk_state:
                state_chencoder += 1
                pos_encoder += 1 if (pos_encoder<(len(pageOptions)-1) and (state_chencoder%2)==0) else 0
                #print("Rotation dans le sens horaire")
            else:
                state_chencoder -= 1
                pos_encoder -= 1 if (pos_encoder>0 and (state_chencoder%2)==0) else 0
                #print("Rotation dans le sens antihoraire")
                print(pos_encoder)
        if GPIO.input(SW) == GPIO.LOW:
            selectedClbkName = pageOptions[currentPage].getClBkName().split(":")
            toRoute = pageOptions[currentPage].getOption(selectedClbkName[0])
            pos_encoder = 0
            print(toRoute, selectedClbkName[0])
            scr.clear()
            scr.redraw()
            if toRoute["target"] == defaultPage:
                currentPage = defaultPage
                pageOptions[currentPage].drawListOptions(pos_encoder)
            else:
                tmpData = toRoute["target"].split(":")
                print(tmpData)
                currentPage = tmpData[0]
                pageOptions[currentPage].setData([selectedClbkName[1], selectedClbkName[-1]])
                pageOptions[currentPage].drawListOptions(pos_encoder)
            print("SelectedCallBackName: ", selectedClbkName)
            await asyncio.sleep(0.1)
        clk_last_state = clk_state
        await asyncio.sleep(0.01)  # Délai court pour éviter les rebonds


if __name__ == "__main__":
    try:
        scr.clear()
        scr.redraw()
        sleep(0.1)
        pageOptions[currentPage].drawListOptions(pos_encoder)
        asyncio.run(encoder_process())
    except KeyboardInterrupt:
        stateProcess = False
        print("Stopping...")
    finally:
        scr.close()
        GPIO.cleanup()



