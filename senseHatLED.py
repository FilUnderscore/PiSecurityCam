from sense_hat import SenseHat
import time
import threading

class SenseHatLED:
    def __init__(self):
        try:
            self.sense = SenseHat()
        except OSError: # SenseHat not detected
            self.sense = None
        
        self.green = (0, 255, 0)
        self.red = (255, 0, 0)

    def set_led_color(self, color):
        if self.sense == None:
            return
        
        logo = [color] * 64
        self.sense.set_pixels(logo)

    def set_green(self):
        self.set_led_color(self.green)

    def set_red(self):
        self.set_led_color(self.red)

    def set_yellow(self):
        self.set_led_color(self.yellow)

    def clear(self):
        if self.sense == None:
            return
        
        self.sense.clear()
