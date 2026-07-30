class FlightController:
    def __init__(self):
        self.mode = "IDLE"

    def arm(self):
        self.mode = "ARMED"
        print("[CTRL] UAV Armed")

    def takeoff(self):
        self.mode = "TAKEOFF"
        print("[CTRL] UAV Taking Off")

    def move_to(self, x, y, z):
        print(f"[CTRL] Flying to ({x}, {y}, {z})")

    def hover(self):
        print("[CTRL] Hovering")

    def land(self):
        self.mode = "LANDING"
        print("[CTRL] Landing")


if __name__ == "__main__":
    fc = FlightController()

    fc.arm()
    fc.takeoff()
    fc.move_to(10, 5, 15)
    fc.hover()
    fc.land()
