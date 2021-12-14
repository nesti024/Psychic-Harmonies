import mido
import time

from pylsl import StreamInlet, resolve_stream


# Verbindungsaufbau zum EEG stream
def initStream(type):
    try:
        # first resolve an EEG stream on the lab network
        print("looking for an EEG stream...")
        streamss = resolve_stream('type', type)
        # create a new inlet to read from the stream

    except KeyboardInterrupt as e:
        print("Ending program")
        raise e
    return streamss


# Aktuelle Daten des Streams abrufen (im Durchschnitt)
def getEEGData():
    try:
        global eegStream
        inlet = StreamInlet(eegStream[0])
        # get a new sample (you can also omit the timestamp part if you're not
        # interested in it)
        sample, timestamp = inlet.pull_sample()
        average = (sample[0] + sample[1] + sample[2] + sample[3] + sample[4]) / 5
        # print(timestamp, sample)
    except KeyboardInterrupt as e:
        print("Ending program")
        raise e
    global medianEEGData
    medianEEGData.append(average)


def getAccelData():
    try:
        global accelStream
        inlet = StreamInlet(accelStream[0])
        # get a new sample (you can also omit the timestamp part if you're not
        # interested in it)
        sample, timestamp = inlet.pull_sample()
        # print(timestamp, sample)
    except KeyboardInterrupt as e:
        print("Ending program")
        raise e
    #average= (sample[0]+sample[1]+sample[2])/3
    global accelData
    accelData.append(sample)

def getGyroData():
    try:
        global gyroStream
        inlet = StreamInlet(gyroStream[0])
        # get a new sample (you can also omit the timestamp part if you're not
        # interested in it)
        sample, timestamp = inlet.pull_sample()
        # print(timestamp, sample)
    except KeyboardInterrupt as e:
        print("Ending program")
        raise e
    #average= (sample[0]+sample[1]+sample[2])/3
    global gyroData
    gyroData.append(sample)

# Einfachste standardmethode. Spielt einen Ton Alle "sleep" Sekunden -> Spielbare Töne: 0-127, alle Werte > 127 = 127 und unter 0 *-1 -> Wenig Bandbreite der Daten genutzt.
# FUnktioniert ganz gut mit Keys oder Streichinstrumenten o.ä.
def getNoteSmallSpec(sleep):
    while True:
        getEEGData()
        if medianEEGData[-1] < 0:
            medianEEGData[-1] = medianEEGData[-1] * -1
        if medianEEGData[-1] > 127:
            medianEEGData[-1] = 127

        if len(medianEEGData) > 1:
            msg = mido.Message('note_off', note=int(medianEEGData[-2]))
            port.send(msg)

        msg = mido.Message('note_on', note=int(medianEEGData[-1]))
        port.send(msg)
        time.sleep(sleep)


def getNoteOneOctave(sleep, octave):
    lastPlayed = -1
    while True:
        octavePitch = octave * 12
        getEEGData()
        if medianEEGData[-1] < 0:
            medianEEGData[-1] = medianEEGData[-1] * -1
        if medianEEGData[-1] > 127:
            medianEEGData[-1] = 127

        if (lastPlayed != -1):
            msg = mido.Message('note_off', note=lastPlayed)
            port.send(msg)

        if (medianEEGData[-1] >= 20 and medianEEGData[-1] < 22.5):
            lastPlayed = 0 + octavePitch
            msg = mido.Message('note_on', note=lastPlayed)
            port.send(msg)
            time.sleep(sleep)
        elif (medianEEGData[-1] >= 22.5 and medianEEGData[-1] < 25):
            lastPlayed = 1 + octavePitch
            msg = mido.Message('note_on', note=lastPlayed)
            port.send(msg)
            time.sleep(sleep)
        elif (medianEEGData[-1] >= 25 and medianEEGData[-1] < 27.5):
            lastPlayed = 2 + octavePitch
            msg = mido.Message('note_on', note=2 + octavePitch)
            port.send(msg)
            time.sleep(sleep)
        elif (medianEEGData[-1] >= 27.5 and medianEEGData[-1] < 30):
            lastPlayed = 3 + octavePitch
            msg = mido.Message('note_on', note=3 + octavePitch)
            port.send(msg)
            time.sleep(sleep)
        elif (medianEEGData[-1] >= 30 and medianEEGData[-1] < 32.5):
            lastPlayed = 4 + octavePitch
            msg = mido.Message('note_on', note=4 + octavePitch)
            port.send(msg)
            time.sleep(sleep)
        elif (medianEEGData[-1] >= 35 and medianEEGData[-1] < 37.5):
            lastPlayed = 5 + octavePitch
            msg = mido.Message('note_on', note=5 + octavePitch)
            port.send(msg)
            time.sleep(sleep)
        elif (medianEEGData[-1] >= 40 and medianEEGData[-1] < 42.5):
            lastPlayed = 6 + octavePitch
            msg = mido.Message('note_on', note=6 + octavePitch)
            port.send(msg)
            time.sleep(sleep)
        elif (medianEEGData[-1] >= 45 and medianEEGData[-1] < 47.5):
            lastPlayed = 7 + octavePitch
            msg = mido.Message('note_on', note=7 + octavePitch)
            port.send(msg)
            time.sleep(sleep)
        elif (medianEEGData[-1] >= 47.5 and medianEEGData[-1] < 50):
            lastPlayed = 8 + octavePitch
            msg = mido.Message('note_on', note=8 + octavePitch)
            port.send(msg)
            time.sleep(sleep)
        elif (medianEEGData[-1] >= 52.5 and medianEEGData[-1] < 55):
            lastPlayed = 9 + octavePitch
            msg = mido.Message('note_on', note=9 + octavePitch)
            port.send(msg)
            time.sleep(sleep)
        elif (medianEEGData[-1] >= 57.5 and medianEEGData[-1] < 60):
            lastPlayed = 10 + octavePitch
            msg = mido.Message('note_on', note=10 + octavePitch)
            port.send(msg)
            time.sleep(sleep)
        elif (medianEEGData[-1] >= 62.5 and medianEEGData[-1] < 65):
            lastPlayed = 11 + octavePitch
            msg = mido.Message('note_on', note=11 + octavePitch)
            port.send(msg)
            time.sleep(sleep)


# Spielt nacheinander Töne bis vor dem anschlangen des 4. der 3. wieder gestoppt wird usw.
# Eignet sich sehr gut für Arpreggiator
def getChordSmallSpec(sleep):
    while True:
        getEEGData()
        if medianEEGData[-1] < 0:
            medianEEGData[-1] = medianEEGData[-1] * -1
        if medianEEGData[-1] > 127:
            medianEEGData[-1] = 127

        if (len(medianEEGData) > 3):
            msg = mido.Message('note_off', note=int(medianEEGData[-4]))
            port.send(msg)

        msg = mido.Message('note_on', note=int(medianEEGData[-1]))
        port.send(msg)
        time.sleep(sleep)


def getNoteChangingSpeed():
    while True:
        getEEGData()
        print(medianEEGData[-1])
        if medianEEGData[-1] < 0:
            medianEEGData[-1] = medianEEGData[-1] * -1

        if len(medianEEGData) > 1:
            msg = mido.Message('note_off', note=int(medianEEGData[-2]))
            port.send(msg)
        if medianEEGData[-1] > 0 and medianEEGData[-1] < 65:
            msg = mido.Message('note_on', note=int(medianEEGData[-1]))
            port.send(msg)
            time.sleep(2)
        elif medianEEGData[-1] >= 65 and medianEEGData[-1] < (65 * 2):
            medianEEGData[-1] -= 65
            msg = mido.Message('note_on', note=int(medianEEGData[-1]))
            port.send(msg)
            time.sleep(0.5)
        elif medianEEGData[-1] >= (65 * 2) and medianEEGData[-1] < (65 * 3):
            medianEEGData[-1] -= 65 * 2
            msg = mido.Message('note_on', note=int(medianEEGData[-1]))
            port.send(msg)
            time.sleep(0.1)
        elif medianEEGData[-1] >= (65 * 3) and medianEEGData[-1] < (65 * 4):
            medianEEGData[-1] -= 65 * 3
            msg = mido.Message('note_on', note=int(medianEEGData[-1]))
            port.send(msg)
            time.sleep(0.0001)
        elif medianEEGData[-1] >= (65 * 4):
            medianEEGData[-1] = 60


""" Doppelte Notenreichweite

    if medianData[-1] > 0 and medianData[-1] < 128:
        msg = mido.Message('note_on', note=int(medianData[-1]))
        port.send(msg)
        time.sleep(1)
    elif medianData[-1] >= 128 and medianData[-1] < (128*2):
        medianData[-1]-=128
        msg = mido.Message('note_on', note=int(medianData[-1]))
        port.send(msg)
        time.sleep(0.75)
    elif medianData[-1] >= (128*2) and medianData[-1] < (128*3):
        medianData[-1]-=128*2
        msg = mido.Message('note_on', note=int(medianData[-1]))
        port.send(msg)
        time.sleep(0.5)
    elif medianData[-1] >= (128*3) and medianData[-1] < (128*4):
        medianData[-1]-=128*3
        msg = mido.Message('note_on', note=int(medianData[-1]))
        port.send(msg)
        time.sleep(0.25)
    elif medianData[-1] >= (128*4):
        medianData[-1] = 60
"""


def playByGyro():
    while(True):
        getGyroData()
        print(gyroData[-1])
        msg = mido.Message('note_off', note=60)
        port.send(msg)
        if(gyroData[-1][0] <1 or gyroData[-1][0] >3):
            msg = mido.Message('note_on', note=60)
            port.send(msg)

aktuelleNote = 0
def getScale():
    global aktuelleNote
    while(True):
        getEEGData()
        medianEEGData[-1] = medianEEGData[-1] + 1000
        getGyroData()

        if aktuelleNote != 0:
            msg = mido.Message('note_off', note=aktuelleNote-12)
            port.send(msg)

        velocity = 64
        if(gyroData[-1][0] <1):
            velocity = 64
        elif gyroData[-1][0] >3:
            velocity = 127

        #Start 900 range 200
        start = 1000
        steps = 7
        range = 100
        steps = range/steps

        if (medianEEGData[-1] <= start + steps):
            aktuelleNote=62
            msg = mido.Message('note_on', note=62-12, velocity=velocity)
        elif (medianEEGData[-1] <= start + steps * 2):
            aktuelleNote = 64
            msg = mido.Message('note_on', note=64-12, velocity=velocity)
        elif (medianEEGData[-1] <= start + steps * 3):
            aktuelleNote = 65
            msg = mido.Message('note_on', note=65-12, velocity=velocity)
        elif (medianEEGData[-1] <= start + steps * 4):
            aktuelleNote = 67
            msg = mido.Message('note_on', note=67-12, velocity=velocity)
        elif (medianEEGData[-1] <= start + steps * 5):
            aktuelleNote = 69
            msg = mido.Message('note_on', note=69-12, velocity=velocity)
        elif (medianEEGData[-1] <= start + steps * 6):
            aktuelleNote = 70
            msg = mido.Message('note_on', note=70-12, velocity=velocity)
        elif """(medianData[-1] <= start+steps*7)""":
            aktuelleNote = 72
            msg = mido.Message('note_on', note=72-12, velocity=velocity)

        print(aktuelleNote)
        print(medianEEGData[-1])
        #print(velocity)
        if(gyroData[-1][0] <1 or gyroData[-1][0] >3):
            port.send(msg)
        #time.sleep(sleep)


def getScaleOctaves():
    global aktuelleNote
    while(True):
        getEEGData()
        medianEEGData[-1] = medianEEGData[-1] + 1000
        getGyroData()

        if aktuelleNote != 0:
            msg = mido.Message('note_off', note=aktuelleNote)
            port.send(msg)

        velocity = 64
        if(gyroData[-1][0] <1):
            velocity = 64
        elif gyroData[-1][0] >3:
            velocity = 127

        #Start 900 range 200
        start = 990
        steps = 14
        range = 110
        steps = range/steps

        if (medianEEGData[-1] <= start + steps):
            aktuelleNote=62-12
        elif (medianEEGData[-1] <= start + steps * 2):
            aktuelleNote = 64-12
        elif (medianEEGData[-1] <= start + steps * 3):
            aktuelleNote = 65-12
        elif (medianEEGData[-1] <= start + steps * 4):
            aktuelleNote = 67-12
        elif (medianEEGData[-1] <= start + steps * 5):
            aktuelleNote = 69-12
        elif (medianEEGData[-1] <= start + steps * 6):
            aktuelleNote = 70-12
        elif (medianEEGData[-1] <= start+steps*7):
            aktuelleNote = 72-12
        elif (medianEEGData[-1] <= start + steps*8):
            aktuelleNote=62
        elif (medianEEGData[-1] <= start + steps * 9):
            aktuelleNote = 64
        elif (medianEEGData[-1] <= start + steps * 10):
            aktuelleNote = 65
        elif (medianEEGData[-1] <= start + steps * 11):
            aktuelleNote = 67
        elif (medianEEGData[-1] <= start + steps * 12):
            aktuelleNote = 69
        elif (medianEEGData[-1] <= start + steps * 13):
            aktuelleNote = 70
        elif """(medianData[-1] <= start+steps*7)""":
            aktuelleNote = 72

        msg = mido.Message('note_on', note=aktuelleNote, velocity=velocity)

        print(aktuelleNote)
        print(medianEEGData[-1])
        print(gyroData[-1])
        #print(velocity)

        if(gyroData[-1][1] <-4 or gyroData[-1][1] >5):
            port.send(msg)
        #time.sleep(sleep)

notes=[]
def getScaleOctavesChords():
    global aktuelleNote
    while(True):
        getEEGData()
        medianEEGData[-1] = medianEEGData[-1] + 1000
        getGyroData()

        velocity = 64
        if(gyroData[-1][0] <1):
            velocity = 64
        elif gyroData[-1][0] >3:
            velocity = 127

        #Start 900 range 200
        start = 950
        steps = 14
        range = 210
        steps = range/steps

        if (medianEEGData[-1] <= start + steps):
            aktuelleNote=62-12
            msg = mido.Message('note_on', note=62-12, velocity=velocity)
        elif (medianEEGData[-1] <= start + steps * 2):
            aktuelleNote=64-12
            msg = mido.Message('note_on', note=64-12, velocity=velocity)
        elif (medianEEGData[-1] <= start + steps * 3):
            aktuelleNote=65-12
            msg = mido.Message('note_on', note=65-12, velocity=velocity)
        elif (medianEEGData[-1] <= start + steps * 4):
            aktuelleNote=67-12
            msg = mido.Message('note_on', note=67-12, velocity=velocity)
        elif (medianEEGData[-1] <= start + steps * 5):
            aktuelleNote=69-12
            msg = mido.Message('note_on', note=69-12, velocity=velocity)
        elif (medianEEGData[-1] <= start + steps * 6):
            aktuelleNote = 70-12
            msg = mido.Message('note_on', note=70-12, velocity=velocity)
        elif (medianEEGData[-1] <= start+steps*7):
            aktuelleNote = 72-12
            msg = mido.Message('note_on', note=72-12, velocity=velocity)
        elif (medianEEGData[-1] <= start + steps*8):
            aktuelleNote=62
            msg = mido.Message('note_on', note=62, velocity=velocity)
        elif (medianEEGData[-1] <= start + steps * 9):
            aktuelleNote = 64
            msg = mido.Message('note_on', note=64, velocity=velocity)
        elif (medianEEGData[-1] <= start + steps * 10):
            aktuelleNote = 65
            msg = mido.Message('note_on', note=65, velocity=velocity)
        elif (medianEEGData[-1] <= start + steps * 11):
            aktuelleNote = 67
            msg = mido.Message('note_on', note=67, velocity=velocity)
        elif (medianEEGData[-1] <= start + steps * 12):
            aktuelleNote = 69
            msg = mido.Message('note_on', note=69, velocity=velocity)
        elif (medianEEGData[-1] <= start + steps * 13):
            aktuelleNote = 70
            msg = mido.Message('note_on', note=70, velocity=velocity)
        elif """(medianData[-1] <= start+steps*7)""":
            aktuelleNote = 72
            msg = mido.Message('note_on', note=72, velocity=velocity)

        print(aktuelleNote)
        print(medianEEGData[-1])
        print(gyroData[-1])
        #print(velocity)
        if(gyroData[-1][1] <-4 or gyroData[-1][1] >5):
            port.send(msg)
            notes.append(aktuelleNote)
            if len(notes) >= 3 and notes[-2] != aktuelleNote:
                msg = mido.Message('note_off', note=int(notes[-2]))
                port.send(msg)

        #time.sleep(sleep)
# print(mido.get_output_names())
# msg.copy(channel=2)
# mido.Message('note_on', channel=2, note=60, velocity=64, time=0)

medianEEGData = []
accelData = []
gyroData = []
eegStream = initStream('EEG')  # Möglichkeiten: 'EEG' 'Accelerometer' 'Gyroscope'
accelStream = initStream('Accelerometer')
gyroStream = initStream('Gyroscope')
port = mido.open_output("loopMIDI Port 1")

# getNoteSmallSpec(1)
# getChordSmallSpec(1)
# getNoteChangingSpeed()
#getNoteOneOctave(1, 3)

getScaleOctaves()

#0.27  Z
#-0.07 X
#0.94 Y

