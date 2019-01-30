import RPi.GPIO as GPIO
import time

muon_pin = 4

GPIO.setmode(GPIO.BCM)

GPIO.setup(muon_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

f = open('data/muons.txt','a+')

detections = []

print("running, please don't touch me...")



try:
    while True:
        try:
            GPIO.wait_for_edge(muon_pin, GPIO.RISING)
        except KeyboardInterrupt:
            pass #no need to do anything here
        print('muon!')
        detections.append(time.time())
        if len(detections) == 100:
            for detection in detections:
                f.write("{}\n".format(detection))
            print('detected 100 muons since last write to file')
            detections = []
except:
    for detection in detections:
        f.write("{}\n".format(detection))
    f.close()
    GPIO.cleanup()

