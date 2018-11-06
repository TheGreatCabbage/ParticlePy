from camera_detector import CameraDetector
import sys

detector = CameraDetector()

args = sys.argv[1:]
if "scint" in args:
    raise NotImplementedError(
        "Scintillator detector has not been implemented yet.")


def run():
    detector.start()


def halt():
    detector.stop()


if __name__ == "__main__":
    try:
        print("Program started. Press Ctrl+C to exit.")
        run()
    except KeyboardInterrupt:
        halt()
        print("Program stopped.")
