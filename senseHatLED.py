from sense_hat import SenseHat

class SenseHatLED:
    def __init__(self):
        self.sense = SenseHat()
        self.green = (0, 255, 0)
        self.red = (255, 0, 0)
        self.nothing = (0, 0, 0)

    def set_led_color(self, color):
        logo = [color] * 64  # Fill the entire 8x8 matrix with the chosen color
        self.sense.set_pixels(logo)

    def set_green(self):
        self.set_led_color(self.green)

    def set_red(self):
        self.set_led_color(self.red)

    def clear(self):
        self.sense.clear()