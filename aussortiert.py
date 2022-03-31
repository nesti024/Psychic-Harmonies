#Aussortierte Modi, diese Datei ist aufgrund von Änderungen in der main nicht lauffähig.


# Einfachste Methode. Spielt einen Ton Alle "sleep" Sekunden -> Spielbare Töne: 0-127, alle Werte > 127 = 127 und < 0 = *-1 -> Wenig Bandbreite der Daten genutzt.
# Funktioniert ganz gut mit Keys oder Streichinstrumenten.
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


#Spielt Noten aus einer Oktave. If-else könnte wie in der main durch loops ersetzt werden, dafür fehlte aber die Zeit.
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


# Spielt in einer Moll Tonleiter so lange neue Töne bis 3 gleichzeitig laufen, dann wird der älteste Ton ausgelassen.
# Funktioniert mit Gyroskop.
def getScaleOctavesChords():
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
        start = 950
        steps = 14
        range = 210
        steps = range / steps

        if (medianEEGData[-1] <= start + steps):
            aktuelleNote = 62 - 12
            msg = mido.Message('note_on', note=62 - 12, velocity=velocity)
        elif (medianEEGData[-1] <= start + steps * 2):
            aktuelleNote = 64 - 12
            msg = mido.Message('note_on', note=64 - 12, velocity=velocity)
        elif (medianEEGData[-1] <= start + steps * 3):
            aktuelleNote = 65 - 12
            msg = mido.Message('note_on', note=65 - 12, velocity=velocity)
        elif (medianEEGData[-1] <= start + steps * 4):
            aktuelleNote = 67 - 12
            msg = mido.Message('note_on', note=67 - 12, velocity=velocity)
        elif (medianEEGData[-1] <= start + steps * 5):
            aktuelleNote = 69 - 12
            msg = mido.Message('note_on', note=69 - 12, velocity=velocity)
        elif (medianEEGData[-1] <= start + steps * 6):
            aktuelleNote = 70 - 12
            msg = mido.Message('note_on', note=70 - 12, velocity=velocity)
        elif (medianEEGData[-1] <= start + steps * 7):
            aktuelleNote = 72 - 12
            msg = mido.Message('note_on', note=72 - 12, velocity=velocity)
        elif (medianEEGData[-1] <= start + steps * 8):
            aktuelleNote = 62
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
        # print(velocity)
        if (gyroData[-1][1] < -4 or gyroData[-1][1] > 5):
            port.send(msg)
            notes.append(aktuelleNote)
            if len(notes) >= 3 and notes[-2] != aktuelleNote:
                msg = mido.Message('note_off', note=int(notes[-2]))
                port.send(msg)

        # time.sleep(sleep)

# Wurde genutzt um ein Sample im Ableton Simpler in 5 Stücke aufzuteilen und diese Stücke spielen zu können.
# Funktioniert mit Gyroskop.
def abraxas(inletEEG, inletGYR, port):
    aktuelleNote = 0
    medianEEGData = []
    gyroData = []
    notes = []
    while (True):
        medianEEGData.append(getData(inletEEG, Type.EEG))

        medianEEGData[-1] = medianEEGData[-1] + 1000

        gyroData.append(getData(inletGYR, Type.GYRO))

        velocity = 64
        if (gyroData[-1][0] < 1):
            velocity = 64
        elif gyroData[-1][0] > 3:
            velocity = 127

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
