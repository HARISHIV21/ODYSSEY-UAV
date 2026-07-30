class Failsafe:

    def __init__(self):
        self.low_battery = False
        self.gps_lost = False
        self.communication_lost = False

    def check(self):

        if self.low_battery:
            print("[FAILSAFE] Low Battery")

        if self.gps_lost:
            print("[FAILSAFE] GPS Lost")

        if self.communication_lost:
            print("[FAILSAFE] Communication Lost")


if __name__ == "__main__":

    fs = Failsafe()

    fs.low_battery = True

    fs.check()
