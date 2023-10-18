from mfrc522 import MFRC522
import utime
from machine import Pin

reader = MFRC522(spi_id=0,sck=6,miso=4,mosi=7,cs=5,rst=3)
device = Pin(28, Pin.OUT, value=0)

print("Bring TAG closer...")
print("")


while True:
    reader.init()
    (stat, tag_type) = reader.request(reader.REQIDL)
    if stat == reader.OK:
        (stat, uid) = reader.SelectTagSN()
        if stat == reader.OK:
            card = int.from_bytes(bytes(uid),"little",False)
            print("CARD ID: "+str(card))
            if card == 977574359:
                device.on()
            else:
                device.off()
utime.sleep_ms(500) 