from enum import Enum

import mido
import time

from pylsl import StreamInlet, resolve_stream, StreamInfo


# Enum für verschiedene stream types.
class Type(Enum):
    EEG = 1
    GYRO = 2
    ACC = 3

#Holt die Daten aus dem stream und speichert sie in ein array
def getData(inlet, type):
    sample, timestamp = inlet.pull_sample()
    if type == Type.EEG:
        average = (sample[0] + sample[1] + sample[2] + sample[3] + sample[4]) / 5
        return average
    else:
        return sample


#spielt beliebig viele Oktaven einer beliebigen moll-Tonleiter.
#gyro: Boolean ob noten per Gyroskop getriggert werden.
#base: Grundton der Tonleiter (integer midi Zahl).
#inletGYR: Objekt zum holen der Gyroskop Daten.
#inletEEG: Objekt zum holen der EEG Daten.
#port: Der Port an den das Midi Signal gesendet werden soll.
#sleep: Wie lange soll zwischen den Tönen gewartet werden?
#start: Der niedrigste Wert aus den EEG Daten der noch einen eigenen Ton hat (alles dadrunter ist der unterste Ton).
#end: Der höchste Wert.
#octaves: Wie viele Oktaven der Tonleiter sollen gespielt werden?
def getScaleOctaves(gyro, base, inletGYR, inletEEG, port, sleep, start, end, octaves):
    medianEEGData = []
    gyroData = []
    velocity = 64
    aktuelleNote = 0
    input("Press Enter to continue...")
    while (True):
        #Daten holen.
        medianEEGData.append(getData(inletEEG, Type.EEG))
        #0 als niedrigste Zahl.
        medianEEGData[-1] = medianEEGData[-1] + 1000

        #Alte Note loslassen.
        if aktuelleNote != 0:
            msg = mido.Message('note_off', note=aktuelleNote)
            port.send(msg)

        #Wenn Gyro: Velocity je nach vergangenem Gyro Wert.
        if (gyro == True):
            gyroData.append(getData(inletGYR, Type.GYRO))
            if (gyroData[-1][0] < 1):
                velocity = 64
            elif gyroData[-1][0] > 3:
                velocity = 127


        #Ausgaben zum Nachvollziehen der gespielten Töne:
        print(aktuelleNote)
        print(medianEEGData[-1])
        if len(gyroData) > 0:
            print(gyroData[-1])
        print("velocity: %d" % velocity)

        #Passende Note zum EEG ermitteln.
        # aktuelleNote = getNoteMinor(medianEEGData[-1], base, 990, 1100, 2)
        aktuelleNote = getNoteMinor(medianEEGData[-1], base, start, end, octaves)

        #Midi message erstellen.
        msg = mido.Message('note_on', note=aktuelleNote, velocity=velocity)



        #Wenn Gyro: Note nur spielen wenn bestimmte Gyro werte über- bzw. unterschritten wurden.
        if (gyro == True):
            if (gyroData[-1][1] < -4 or gyroData[-1][1] > 5):
                port.send(msg)
                time.sleep(sleep)
        #Sonst Note einfach spielen.
        elif (gyro == False):
            port.send(msg)
            time.sleep(sleep)

#Ermittelt den zu spielenden Ton.
#eegData: Die aktuellen EEG-Werte.
#base: Der Grundton.
#start: Der niedrigste Wert aus den EEG Daten der noch einen eigenen Ton hat (alles dadrunter ist der unterste Ton).
#end: Der höchste Wert.
#octaves: Wie viele Oktaven der Tonleiter sollen gespielt werden?
def getNoteMinor(eegData, base, start, end, octaves):
    #Die Schritte die für den nächsten Ton der Tonleiter gegangen werden müssen (1: Halbtonschritt, 2: Ganztonschritt).
    #Der Basiston ist teil der Folge.
    noteSteps = [0, 2, 1, 2, 2, 1, 2]

    #Falls mehr als eine Oktave gespielt wird sieht die Folge so aus:
    noteSteps2 = [2, 2, 1, 2, 2, 1, 2]
    if (octaves > 1):
        for x in range(octaves - 1):
            noteSteps += noteSteps2

    #Falls der Wert unter start oder über end liegt wird der höchste bzw. der niedrigste Ton gespielt.
    note = base
    if (eegData < start):
        return base
    elif (eegData > end):
        for x in noteSteps:
            note += x
        return note

    #Berechnung der gewünschten Schritte (siehe Lerntagebuch für Details).
    notes = octaves * 7
    rang = end - start
    steps = rang / notes

    data = eegData - start

    ds = data / steps

    for x in range(int(ds+1)):
        if(len(noteSteps) > x):
            note += noteSteps[x]

    #Die zu spielende Note als midi Integer.
    return note


# zum ausgeben der port namen
# print(mido.get_output_names())


def main():
    # Verbindungsaufbau zu den streams
    inletEEG = StreamInlet(resolve_stream('type', 'EEG')[0])
    inletACC = StreamInlet(resolve_stream('type', 'Accelerometer')[0])
    inletGYR = StreamInlet(resolve_stream('type', 'Gyroscope')[0])

    # Port öffnen
    port = mido.open_output("loopMIDI Port 1")

    sleep = 0.01
    #start = 990
    start = 1000
    #end = 1100
    end = 1050
    octaves = 2
    getScaleOctaves(False, 38, inletGYR, inletEEG, port, sleep, start, end, octaves)



main()