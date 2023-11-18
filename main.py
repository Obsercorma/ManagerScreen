#import RPi.GPIO as gpio
from st7920 import ST7920
from time import sleep

#RST_PIN = 18

#gpio.setmode(gpio.BCM)
#gpio.setup(RST_PIN, gpio.IN)
#gpio.output(RST_PIN,gpio.HIGH)
#sleep(0.1)
#gpio.output(RST_PIN,gpio.LOW)

scr = ST7920()
scr.set_rotation(3)
scr.clear()
scr.redraw()
#exit(0)
#sleep(0.1)

#try:
#       for a in range(11):
#scr.clear()
#scr.redraw()
#sleep(0.1)
scr.put_text("Portfolio",0,0)
scr.put_text("V1.14.18",0,10)
scr.put_text("Online",0,20)
scr.put_text("W:0 E:0",0,30)
scr.line(0,40,63,40)
scr.redraw()
sleep(1.0)
#except:
#       pass
#scr.close()
#gpio.cleanup()
sleep(0.1)
scr.put_text("Myth. Bot",0,50)
scr.put_text("V1.2.2",0,60)
scr.put_text("Online",0,70)
scr.line(0,80,63,80)
scr.redraw()
#sleep(2.0)
#scr.clear()
sleep(0.1)
#scr.put_text("test",0,45)
#scr.redraw()

scr.close()