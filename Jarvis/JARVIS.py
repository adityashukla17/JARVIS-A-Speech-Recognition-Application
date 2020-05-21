# AUTHOR : ADITYA SHUKLA

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~DEFINFING JARVIS~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import datetime
import time

import cv2
import pyowm
import pyttsx
import speech_recognition as JARVIS_LISTEN
import math
import numpy as np

sp_engine = pyttsx.init()
now = datetime.datetime.now()
run = 0
record = ""
API = '47e7bee798265c1ad2bfe92183950d01'
owm = pyowm.OWM(API)
observation = owm.weather_at_place('Ahmadabad,IN')
weather = observation.get_weather()
Temperature = weather.get_temperature('celsius')

'''img_file = "JARVIS_UI.gif"
animation = pyglet.resource.animation(img_file)
sprite = pyglet.sprite.Sprite(animation)
# create a window and set it to the image size
win = pyglet.window.Window(width=sprite.width, height=500)
# set window background color = r, g, b, alpha
# each value goes from 0.0 to 1.0
black = 1, 1, 1, 1
pyglet.gl.glClearColor(*black)


@win.event
def on_draw():
    win.clear()
    sprite.draw()

pyglet.app.run()
'''


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~END PROGRAM~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# noinspection PyTypeChecker
def JARVIS_SPEAK(text):
    sp_engine.say(text)
    sp_engine.runAndWait()  # starting datetime variable
    global record


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~INITIALIZE~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# noinspection PyTypeChecker
def initialize():
    global Temperature
    JARVIS_SPEAK("Initiating Launch Sequence......Please wait!")
    temp = str(Temperature)
    temp = temp[13:15]
    print(time.strftime("%A %d %B %Y"))
    print(temp)
    JARVIS_SPEAK("Welcome back Sir! Let\'s pick up from where you left.")
    JARVIS_SPEAK("Today is ")
    JARVIS_SPEAK(time.strftime("%A"))
    JARVIS_SPEAK(time.strftime("%B %d %Y"))
    JARVIS_SPEAK("The current temperature in Ahmedabad is ")
    JARVIS_SPEAK(temp)
    JARVIS_SPEAK("degree celsius")
    JARVIS_SPEAK("It is ")
    JARVIS_SPEAK(time.strftime("%I %M %p"))


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~TAKE COMMAND~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# noinspection PyTypeChecker
def command():
    JARVIS_SPEAK("What can I do for you Sir?")
    # Getting audio from the microphone
    print("listening...")
    mic = JARVIS_LISTEN.Recognizer()
    with JARVIS_LISTEN.Microphone() as source:
        mic.adjust_for_ambient_noise(source)
        audio = mic.listen(source)
    print("audio taken...")
    # recognition using Google Speech Recognition
    try:
        print("in try block")
        recognition = mic.recognize_google(audio)
        record = str(recognition)
        print(record)
    except JARVIS_LISTEN.UnknownValueError:
        print("in except 1")
        JARVIS_SPEAK("Sorry sir couldn't really get you?")
        JARVIS_SPEAK("Can you repeat?")
        command()
    except JARVIS_LISTEN.RequestError as err:
        print("in except 2")
        JARVIS_SPEAK('Sir we are offline as it seems.....; {0}'.format(err))


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~GESTURE CONTROL~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# noinspection PyTypeChecker
def jarvis_gesture():
    # opening jarvis' eye ---> WebCAM open
    JARVIS_SEE = cv2.VideoCapture(0)

    while JARVIS_SEE.isOpened():
        ret, img = JARVIS_SEE.read()
        cv2.rectangle(img, (300, 300), (100, 100), (0, 255, 0), 0)
        crop_img = img[100:300, 100:300]
        grey = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
        value = (35, 35)
        blurred = cv2.GaussianBlur(grey, value, 0)
        _, thresh1 = cv2.threshold(blurred, 127, 255,
                                   cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        cv2.imshow('Thresholded', thresh1)
        _, contours, hierarchy = cv2.findContours(thresh1.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        max_area = -1
        for i in range(len(contours)):
            cnt = contours[i]
            area = cv2.contourArea(cnt)
            if area > max_area:
                max_area = area
                ci = i
        cnt = contours[ci]
        x, y, w, h = cv2.boundingRect(cnt)
        cv2.rectangle(crop_img, (x, y), (x + w, y + h), (0, 0, 255), 0)
        hull = cv2.convexHull(cnt)
        drawing = np.zeros(crop_img.shape, np.uint8)
        cv2.drawContours(drawing, [cnt], 0, (0, 255, 0), 0)
        cv2.drawContours(drawing, [hull], 0, (0, 0, 255), 0)
        hull = cv2.convexHull(cnt, returnPoints=False)
        defects = cv2.convexityDefects(cnt, hull)
        count_defects = 0
        cv2.drawContours(thresh1, contours, -1, (0, 255, 0), 3)
        for i in range(defects.shape[0]):
            s, e, f, d = defects[i, 0]
            start = tuple(cnt[s][0])
            end = tuple(cnt[e][0])
            far = tuple(cnt[f][0])
            a = math.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
            b = math.sqrt((far[0] - start[0]) ** 2 + (far[1] - start[1]) ** 2)
            c = math.sqrt((end[0] - far[0]) ** 2 + (end[1] - far[1]) ** 2)
            angle = math.acos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c)) * 57
            if angle <= 90:
                count_defects += 1
                cv2.circle(crop_img, far, 1, [0, 0, 255], -1)
            # dist = cv2.pointPolygonTest(cnt,far,True)
            cv2.line(crop_img, start, end, [0, 255, 0], 2)
            # cv2.circle(crop_img,far,5,[0,0,255],-1)
        if count_defects == 1:
            inp = "God is great"
            cv2.putText(img, inp, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
        elif count_defects == 2:
            inp = "Pose for a selfie"
            cv2.putText(img, inp, (5, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, 2)
        elif count_defects == 3:
            inp = "Opening program of choice"
            cv2.putText(img, inp, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
        elif count_defects == 4:
            inp = "F O U R"
            cv2.putText(img, inp, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
        elif count_defects == 5:
            inp = "Hello Sir!!"
            cv2.putText(img, inp, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
        else:
            inp = "Waiting for gesture..."
            cv2.putText(img, inp, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
        cv2.imshow('Gesture', img)
        all_img = np.hstack((drawing, crop_img))
        cv2.imshow('Contours', all_img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything is done, release the capture
    JARVIS_SEE.release()
    cv2.destroyAllWindows()


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~END PROGRAM~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# noinspection PyTypeChecker
def terminate():
    if 6 <= now.hour < 12:
        JARVIS_SPEAK("Good Morning Sir! Have a good day.........Bye......")
    elif 12 <= now.hour < 16:
        JARVIS_SPEAK("Good Afternoon Sir!........Bye......")
    elif 16 <= now.hour < 19:
        JARVIS_SPEAK("Good Evening Sir! Enjoy.......Bye......")
    elif now.hour >= 19 or now.hour < 6:
        JARVIS_SPEAK("Good Night Sir! Happy sleeping.....Bye.....")

    JARVIS_SPEAK("Terminating Jarvis....3.....2......1.....")


# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!*******MAIN*******!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
initialize()
command()
if record is "open your eyes" or "jarvis see":
    jarvis_gesture()
else:
    terminate()
