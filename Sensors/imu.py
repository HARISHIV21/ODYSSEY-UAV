import random

class IMU:

    def read(self):
        return {
            "roll": round(random.uniform(-5,5),2),
            "pitch": round(random.uniform(-5,5),2),
            "yaw": round(random.uniform(0,360),2)
        }


if __name__ == "__main__":

    imu = IMU()

    print(imu.read())
