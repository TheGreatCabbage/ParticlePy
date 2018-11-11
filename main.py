from camera_detector import CameraDetector
import sys

detector = CameraDetector()

# Get command line arguments, remove dashes for easy parsing.
args = list(map(lambda x: x.replace("-", ""), sys.argv[1:]))

if "scint" in args:
    # This is where we would set 'detector' to be a ScintillatorDetector.
    raise NotImplementedError(
        "Scintillator detector has not been implemented yet.")

if "purge" in args:
    # Purge data, including logs and images.
    detector.purge_on_start = True


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
