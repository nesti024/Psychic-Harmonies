from matplotlib import pyplot
from matplotlib.animation import FuncAnimation
from pylsl import StreamInlet, resolve_stream
import matplotlib

# Von Pycharm benötigt um live-plots zu zeichnen
matplotlib.use("TkAgg")

# globale Variablen für die Daten des Plots
x_data, y_data = [], []

# iterationen des Plots
iterations = 0

# Verbindungsaufbau zum EEG stream
def initStream():
    try:
        # first resolve an EEG stream on the lab network
        print("looking for an EEG stream...")
        streamss = resolve_stream('type', 'EEG')
        # create a new inlet to read from the stream

    except KeyboardInterrupt as e:
        print("Ending program")
        raise e
    return streamss


# globale stream Variable
streams = initStream()


# Aktuelle Daten des Streams abrufen (im Durchschnitt)
def getData():
    try:
        global streams
        inlet = StreamInlet(streams[0])
        # get a new sample (you can also omit the timestamp part if you're not
        # interested in it)
        sample, timestamp = inlet.pull_sample()
        average = (sample[0] + sample[1] + sample[2] + sample[3] + sample[4]) / 5
        # print(timestamp, sample)
    except KeyboardInterrupt as e:
        print("Ending program")
        raise e
    global y_data
    y_data.append(average)

# plot vorbereiten
figure = pyplot.figure()
line, = pyplot.plot(x_data, y_data, '-')


# callback update funktion für den plot
def updateAverage(frame):
    global iterations
    global x_data

    x_data.append(iterations)
    getData()
    line.set_data(x_data, y_data)
    figure.gca().relim()
    figure.gca().autoscale_view()
    iterations += 1
    return line,

# animation ausführen
animation = FuncAnimation(figure, updateAverage, interval=200)
pyplot.show()