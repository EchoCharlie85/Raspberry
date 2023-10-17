from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY
import utime
from pimoroni_i2c import PimoroniI2C
from breakout_sgp30 import BreakoutSGP30
from pimoroni import RGBLED

# Init Display
display = PicoGraphics(display=DISPLAY_PICO_DISPLAY, rotate=180)
display.set_font('bitmap8')
display.set_backlight(0.5)

# Init LED
led = RGBLED(6, 7, 8) #RGBLED PIN definition

# Fonction qui retourne le niveau de CO2 et TVOC
def mesure_capteur():
    air_quality = sgp30.get_air_quality()
    eCO2 = air_quality[BreakoutSGP30.ECO2]
    TVOC = air_quality[BreakoutSGP30.TVOC]
    return eCO2, TVOC
  
# Fonction qui efface l'ecran
def clear():
    my_pen = display.create_pen(0,0,0)
    display.set_pen(my_pen)
    display.clear()
    display.update()
      
# Gere la couleur en fonction du niveau de CO2
def get_color(CO2):
    if eCO2 < 500:
        return 0,0xff,0 #vert
    elif eCO2 < 1000:
        return 0xff,165,0 #orange
    else:
        return 0xff,0,0 #rouge

# Initialisation du capteur
PINS_PICO_EXPLORER = {"sda": 20, "scl": 21}
i2c = PimoroniI2C(**PINS_PICO_EXPLORER)
sgp30 = BreakoutSGP30(i2c)
sgp30.soft_reset()
utime.sleep(1)    
sgp30.start_measurement(False)
  
# Boucle du programme principal
while True:
    # Lecture de la qualite de l'air sur le capteur    
    eCO2, TVOC = mesure_capteur()       
    print("CO2 ", eCO2, " TVOC ", TVOC)
    r,g,b = get_color(eCO2)
    # Affichage sur l'ecran
    my_pen = display.create_pen(0xff,0xff,0xff)
    display.set_pen(my_pen)      
    display.text("CO2 ppm", 30, 10, 240, 4)
    my_pen = display.create_pen(r,g,b)
    display.set_pen(my_pen)      
    display.text("{}".format(eCO2), 40, 70, 240, 5)
    led.set_rgb(r,g,b)
    display.update()
    utime.sleep(1)                                    
    clear()