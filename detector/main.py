import sys
from pulse_detector import PulseDetector

detector = PulseDetector()

# Get command line arguments, remove dashes for easy parsing.
args = list(map(lambda x: x.replace("-", ""), sys.argv[1:]))

if "camera" in args:
    # Shouldn't import down here, but requires PiCamera.
    from camera_detector import CameraDetector
    detector = CameraDetector()

if "purge" in args:
    # Purge data, including logs and images.
    detector.purge_on_start = True

if "nocache" in args:
    detector.cache_data = False 
    print("Cache disabled.")


def run():
    detector.start()


def halt():
    detector.stop()


# The if statement ensures that its code does not run when this file is imported.
if __name__ == "__main__":
    try:
        print("Program started. Press Ctrl+C to exit.")
        run()
    except KeyboardInterrupt:
        halt()
        print("\nProgram stopped.")
