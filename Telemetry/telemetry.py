import time

class Telemetry:

    def __init__(self):
        self.altitude = 0
        self.speed = 0
        self.battery = 100

    def update(self):
        self.altitude += 2
        self.speed = 5
        self.battery -= 1

    def display(self):
        print("----------------------------")
        print(f"Altitude : {self.altitude} m")
        print(f"Speed    : {self.speed} m/s")
        print(f"Battery  : {self.battery}%")
        print("----------------------------")


if __name__ == "__main__":

    telemetry = Telemetry()

    for i in range(5):
        telemetry.update()
        telemetry.display()
        time.sleep(1)
