import math


class DistanceCalculator:

    @staticmethod
    def distance_3d(current, target):

        dx = current.north_m - target["north"]
        dy = current.east_m - target["east"]
        dz = current.down_m - target["down"]

        return math.sqrt(dx * dx + dy * dy + dz * dz)

    @staticmethod
    def horizontal(current, target):

        dx = current.north_m - target["north"]
        dy = current.east_m - target["east"]

        return math.sqrt(dx * dx + dy * dy)

    @staticmethod
    def vertical(current, target):

        return abs(current.down_m - target["down"])
