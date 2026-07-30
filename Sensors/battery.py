class Battery:

    def __init__(self):
        self.level = 100

    def consume(self):
        self.level -= 5

    def check(self):
        print(f"[BATTERY] {self.level}%")

        if self.level <= 20:
            print("[BATTERY] WARNING - LOW BATTERY")


if __name__ == "__main__":

    battery = Battery()

    for _ in range(18):
        battery.consume()
        battery.check()
