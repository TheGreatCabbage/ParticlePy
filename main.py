from camera_detector import CameraDetector
import sys

detector = CameraDetector()

args = sys.argv[1:]
# Not implemented yet. 
#if "scint" in args: detector = ScintillatorDetector()


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
