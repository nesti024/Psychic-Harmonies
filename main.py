import mido
import time

from pylsl import StreamInlet, resolve_stream, StreamInfo

# Verbindungsaufbau zum EEG stream


inletEEG = StreamInlet(resolve_stream('type', 'EEG')[0])
inletACC = StreamInlet(resolve_stream('type', 'Accelerometer')[0])
inletGYR = StreamInlet(resolve_stream('type', 'Gyroscope')[0])


# Aktuelle Daten des Streams abrufen (im Durchschnitt)
def getEEGData():
    try:
        global inletEEG
        # get a new sample (you can also omit the timestamp part if you're not
        # interested in it)
        sample, timestamp = inletEEG.pull_sample()
        average = (sample[0] + sample[1] + sample[2] + sample[3] + sample[4]) / 5
        # print(timestamp, sample)
    except KeyboardInterrupt as e:
        print("Ending program")
        raise e
    global medianEEGData
    medianEEGData.append(average)


def getAccelData():
    try:
        global inletACC
        # get a new sample (you can also omit the timestamp part if you're not
        # interested in it)
        sample, timestamp = inletACC.pull_sample()
        # print(timestamp, sample)
    except KeyboardInterrupt as e:
        print("Ending program")
        raise e
    # average= (sample[0]+sample[1]+sample[2])/3
    global accelData
    accelData.append(sample)


def getGyroData():
    try:
        global inletGYR
        # get a new sample (you can also omit the timestamp part if you're not
        # interested in it)
        sample, timestamp = inletGYR.pull_sample()
        # print(timestamp, sample)
    except KeyboardInterrupt as e:
        print("Ending program")
        raise e
    # average= (sample[0]+sample[1]+sample[2])/3
    global gyroData
    gyroData.append(sample)





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




def getScale():
    aktuelleNote = 0
    while (True):
        getEEGData()
        medianEEGData[-1] = medianEEGData[-1] + 1000
        getGyroData()

        if aktuelleNote != 0:
            msg = mido.Message('note_off', note=aktuelleNote - 12)
            port.send(msg)

        velocity = 64
        if (gyroData[-1][0] < 1):
            velocity = 64
        elif gyroData[-1][0] > 3:
            velocity = 127

        # Start 900 range 200
        start = 1000
        steps = 7
        range = 100
        steps = range / steps

        if (medianEEGData[-1] <= start + steps):
            aktuelleNote = 62
            msg = mido.Message('note_on', note=62 - 12, velocity=velocity)
        elif (medianEEGData[-1] <= start + steps * 2):
            aktuelleNote = 64
            msg = mido.Message('note_on', note=64 - 12, velocity=velocity)
        elif (medianEEGData[-1] <= start + steps * 3):
            aktuelleNote = 65
            msg = mido.Message('note_on', note=65 - 12, velocity=velocity)
        elif (medianEEGData[-1] <= start + steps * 4):
            aktuelleNote = 67
            msg = mido.Message('note_on', note=67 - 12, velocity=velocity)
        elif (medianEEGData[-1] <= start + steps * 5):
            aktuelleNote = 69
            msg = mido.Message('note_on', note=69 - 12, velocity=velocity)
        elif (medianEEGData[-1] <= start + steps * 6):
            aktuelleNote = 70
            msg = mido.Message('note_on', note=70 - 12, velocity=velocity)
        elif """(medianData[-1] <= start+steps*7)""":
            aktuelleNote = 72
            msg = mido.Message('note_on', note=72 - 12, velocity=velocity)

        print(aktuelleNote)
        print(medianEEGData[-1])
        # print(velocity)
        if (gyroData[-1][0] < 1 or gyroData[-1][0] > 3):
            port.send(msg)
        # time.sleep(sleep)


def getScaleOctaves(gyro, base):
    velocity = 64
    aktuelleNote = 0
    gehalteneNote = 0
    while (True):
        getEEGData()
        medianEEGData[-1] = medianEEGData[-1] + 1000
        getGyroData()

        if aktuelleNote != 0:
            msg = mido.Message('note_off', note=aktuelleNote)
            port.send(msg)

        if(gyro==True):
            if (gyroData[-1][0] < 1):
                velocity = 64
            elif gyroData[-1][0] > 3:
                velocity = 127


        if(velocity>127):
            velocity=127
        elif(velocity<0):
            velocity=0

        aktuelleNote = getNote(medianEEGData[-1], base)

        msg = mido.Message('note_on', note=aktuelleNote, velocity=velocity)

        print(aktuelleNote)
        print(medianEEGData[-1])
        print(gyroData[-1])
        print("velocity: %d"%velocity)
        # print(velocity)

        if(gyro==True):
            if (gyroData[-1][1] < -4 or gyroData[-1][1] > 5):
                port.send(msg)
                time.sleep(1)

        elif(gyro == False):
            port.send(msg)
            time.sleep(1)


notes = []

def getNote(eegData, base):
    noteSteps = [0,2,1,2,2,1,2,2,2,1,2,2,1,2]
    ranges = []
    start = 990
    notes = 14
    end = 110
    steps = end / notes
    for x in range(1, notes+1):
        ranges.append(start+steps*x)

    print(ranges)
    counter = 1
    for ran in ranges:
        if(eegData <= ran):
            add = 0
            for x in range(counter):
                add+=noteSteps[x]

            return base + add

        counter+=1



def abraxas():
    global aktuelleNote
    while (True):
        getEEGData()
        medianEEGData[-1] = medianEEGData[-1] + 1000
        getGyroData()

        velocity = 64
        if (gyroData[-1][0] < 1):
            velocity = 64
        elif gyroData[-1][0] > 3:
            velocity = 127

        # Start 900 range 200
        start = 1000
        steps = 5
        range = 50
        steps = range / steps

        if (medianEEGData[-1] <= start + steps):
            aktuelleNote = 24 + 12
            msg = mido.Message('note_on', note=aktuelleNote, velocity=velocity)
        elif (medianEEGData[-1] <= start + steps * 2):
            aktuelleNote = 25 + 12
            msg = mido.Message('note_on', note=aktuelleNote, velocity=velocity)
        elif (medianEEGData[-1] <= start + steps * 3):
            aktuelleNote = 26 + 12
            msg = mido.Message('note_on', note=aktuelleNote, velocity=velocity)
        elif (medianEEGData[-1] <= start + steps * 4):
            aktuelleNote = 27 + 12
            msg = mido.Message('note_on', note=aktuelleNote, velocity=velocity)
        else:
            aktuelleNote = 28 + 12
            msg = mido.Message('note_on', note=aktuelleNote, velocity=velocity)

        print(aktuelleNote)
        print(medianEEGData[-1])
        print(gyroData[-1])
        # print(velocity)
        if (gyroData[-1][1] < -4 or gyroData[-1][1] > 5):
            port.send(msg)
            notes.append(aktuelleNote)

            if len(notes) >= 3 and notes[-2] != aktuelleNote:
                msg = mido.Message('note_off', note=int(notes[-2]))
                port.send(msg)


# print(mido.get_output_names())
# msg.copy(channel=2)
# mido.Message('note_on', channel=2, note=60, velocity=64, time=0)


medianEEGData = []
accelData = []
gyroData = []
port = mido.open_output("loopMIDI Port 1")


# getNoteSmallSpec(1)
# getChordSmallSpec(1)
# getNoteChangingSpeed()
# getNoteOneOctave(1, 3)

getScaleOctaves(False, 50)
