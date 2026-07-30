class Navigation:

    def __init__(self):
        self.current_position = (0.0, 0.0, 0.0)
        self.target_position = None

    def update_position(self, x, y, z):
        self.current_position = (x, y, z)
        print(f"[NAV] Current Position: {self.current_position}")

    def set_target(self, x, y, z):
        self.target_position = (x, y, z)
        print(f"[NAV] Target Position: {self.target_position}")

    def navigate(self):
        if self.target_position:
            print("[NAV] Navigating...")
            print(f"[NAV] Flying to {self.target_position}")
        else:
            print("[NAV] No target available")


if __name__ == "__main__":
    nav = Navigation()

    nav.update_position(0, 0, 0)
    nav.set_target(20, 15, 10)
    nav.navigate()
