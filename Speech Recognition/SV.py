import numpy as np
# library for speech_recognition (imitated API)
import speech_recognition
# for read/write of all the wav files
import wave
# to carry out the dummy system operations
import sys
# python text-to-speech offline assistant
import matplotlib.pyplot as plt
# import the inbuilt array library
from array import array
from struct import pack
# from sys import byteorder class
from sys import byteorder
# to copy data byte/sector/page wise on secondary memory
import copy
# enhanced for all audio related hardware functionalities
import pyaudio
import Tkinter
from Tkinter import *

# $$$$$$$$$$$ GLOBAL VARIABLE DECLARATION $$$$$$$$$$$$$$
# declare a recognizer which calls the method of the package Recognizer
recognizer = speech_recognition.Recognizer()
# variable string to parse the understood audio input
recognition = ""
# the actual testing boolean variable
test = False
# number of times it will run
run_time = 0
# created to compare next time  user speaks
temp = []
# initialize data lena
start = 0
improper_count = 0.00
hit = 0.00
result_length = 0.00


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  GUI ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def gui():
    base = Tkinter.Tk()
    label1 = Label(base, text="Hello jarvis!")
    label1.pack()
    img = PhotoImage(file="jarvis.gif", format="gif - {}".format(0))
    label2 = Label(base, image=img)
    label2.pack()
    button1 = Button(base, text="Button", bg="red")
    button1.pack()
    base.mainloop()


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ AUTHENTICATING ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def u_authenticate():
    # it is the threshold decided after checking surrounding noise
    THRESHOLD = 29100
    # audio levels not normalised.
    # used 10-bit sequencing of one package
    CHUNK_SIZE = 1024
    # Defines a silent period,i.e no data for around 3 seconds
    SILENT_CHUNKS = 3 * 44100 / 1024  # about 3sec
    # 16-bit integer
    FORMAT = pyaudio.paInt16
    FRAME_MAX_VALUE = 2 ** 15 - 1
    NORMALIZE_MINUS_ONE_dB = 10 ** (-1.0 / 20)
    # normal sampling voice rate for humans
    RATE = 44100
    CHANNELS = 1
    TRIM_APPEND = RATE / 4

    def is_silent(data_chunk):
        """Returns 'True' if below the 'silent' threshold"""
        return max(data_chunk) < THRESHOLD

    def normalize(data_all):
        """Amplify the volume out to max -1dB"""
        # MAXIMUM = 16384
        normalize_factor = (float(NORMALIZE_MINUS_ONE_dB * FRAME_MAX_VALUE)
                            / max(abs(i) for i in data_all))
        r = array('h')
        for i in data_all:
            r.append(int(i * normalize_factor))
        return r

    def trim(data_all):
        _from = 0
        _to = len(data_all) - 1
        for i, b in enumerate(data_all):
            if abs(b) > THRESHOLD:
                _from = max(0, i - TRIM_APPEND)
                break

        for i, b in enumerate(reversed(data_all)):
            if abs(b) > THRESHOLD:
                _to = min(len(data_all) - 1, len(data_all) - 1 - i + TRIM_APPEND)
                break

        return copy.deepcopy(data_all[_from:(_to + 1)])

    def authenticate(inp_data, length):
        global result_length, start, temp, run_time, test, improper_count
        thresh = 29100
        compare = []
        for i in range(0, length):
            if inp_data[i] > thresh:
                start = 1
            if start == 1:
                case = abs((inp_data[i]) / 5000)
                compare.append(case)
        start = 0
        if run_time == 0:
            temp = compare
            print "First voice : "
            print temp
        if run_time == 1:
            result = []
            for i in range(0, len(temp) - 1):
                while len(compare) < len(temp):
                    compare.append(0)
                if compare[i] > 0 and temp[i] > 0:
                    result.append(abs(compare[i] - temp[i]))
                    if abs(compare[i] - temp[i]) > 0:
                        improper_count += 1.00
                result_length += 1.00
            print "Second voice : "
            print compare
            print "Compared Result : "
            print result

    def record():
        """Record a word or words from the microphone and
        return the data as an array of signed shorts."""
        global run_time
        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, output=True,
                        frames_per_buffer=CHUNK_SIZE)
        silent_chunks = 0
        audio_started = False
        data_all = array('h')

        while True:
            # little endian, signed short
            data_chunk = array('h', stream.read(CHUNK_SIZE))
            if byteorder == 'big':
                data_chunk.byteswap()
            data_all.extend(data_chunk)
            silent = is_silent(data_chunk)
            if audio_started:
                if silent:
                    silent_chunks += 1
                    if silent_chunks > SILENT_CHUNKS:
                        break
                else:
                    silent_chunks = 0
            elif not silent:
                audio_started = True

        sample_width = p.get_sample_size(FORMAT)
        stream.stop_stream()
        stream.close()
        p.terminate()

        data_all = trim(data_all)
        # we trim before normalize as threshold applies to un-normalized wave (as well as is_silent() function)
        data_all = normalize(data_all)
        authenticate(data_all, len(data_all))
        return sample_width, data_all

    def record_to_file(path):
        # Records from the microphone and outputs the resulting data to 'path'
        sample_width, data = record()
        data = pack('<' + ('h' * len(data)), *data)
        wave_file = wave.open(path, 'wb')
        wave_file.setnchannels(CHANNELS)
        wave_file.setsampwidth(sample_width)
        wave_file.setframerate(RATE)
        wave_file.writeframes(data)
        wave_file.close()

    if __name__ == '__main__':
        print("Wait in silence to begin recording; wait in silence to terminate")
        if run_time == 0:
            record_to_file('sample.wav')
            print("done - result written to sample.wav")
        elif run_time == 1:
            record_to_file('sample1.wav')
            print("done - result written to sample1.wav")

    if run_time == 0:
        spf1 = wave.open('sample.wav', 'r')
        signal1 = spf1.readframes(-1)
        signal1 = np.fromstring(signal1, 'Int16')
        plt.figure(2)
        plt.title('VOICE SAMPLE 1')
        plt.plot(signal1)
        plt.savefig('fig 1')
        # plt.show()
        print("First Voice print stored.")
    elif run_time == 1:
        spf1 = wave.open('sample1.wav', 'r')
        signal1 = spf1.readframes(-1)
        signal1 = np.fromstring(signal1, 'Int16')
        plt.figure(2)
        plt.title('VOICE SAMPLE 2')
        plt.plot(signal1)
        plt.savefig('fig 2')
        # plt.show()
        print("Second Voice print stored.")
    return


# ```````MAIN``````

print("Hi there! New Face.")
print("Identify yourself!!")
while run_time != 2:
    u_authenticate()
    run_time += 1
print improper_count
print result_length
hit = 100 * (1 - (improper_count / result_length))
print("Accuracy is :-")
print hit
if hit > 70.00:
    print("Welcome back Aditya!!")
elif run_time:
    print("Sorry, you are unidentified.")
# gui()
sys.exit(0)
# !!!!!! END !!!!!!
