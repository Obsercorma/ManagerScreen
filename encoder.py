import RPi.GPIO as GPIO
import time

# Configuration des broches
CLK = 17  # Exemple, remplacez par la broche que vous utilisez
DT = 18   # Exemple, remplacez par la broche que vous utilisez
SW = 27   # Exemple, remplacez par la broche que vous utilisez
PWR_ENC = 24

GPIO.setmode(GPIO.BCM)
GPIO.setup(PWR_ENC, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(CLK, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(DT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(SW, GPIO.IN, pull_up_down=GPIO.PUD_UP)

clk_last_state = GPIO.input(CLK)

try:
    while True:
        clk_state = GPIO.input(CLK)
        dt_state = GPIO.input(DT)

        if clk_state != clk_last_state:
            if dt_state != clk_state:
                print("Rotation dans le sens horaire")
            else:
                print("Rotation dans le sens antihoraire")

        if GPIO.input(SW) == GPIO.LOW:
            print("Bouton enfoncé")

        clk_last_state = clk_state
        time.sleep(0.01)  # Délai court pour éviter les rebonds

except KeyboardInterrupt:
    print("Programme interrompu par l'utilisateur")
finally:
    GPIO.cleanup()
