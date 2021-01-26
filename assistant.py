## pip install pyttsx3-for converting text to speech.
## pip install speechRecognition-for speech recognition
## pip install pipwin + pipwin install pyaudio- for windows; sudo apt-get install portaudio19-dev python-pyaudio+pip3 install pyaudio-for ubuntu 18.04
## pip install wikipedia- for wiki defs
## pip install psutil-for checking cpu performance and battery
## pip install pyjokes-for telling jokes
## pip install pyautogui-for screenshots and other funcs
## pip install wolframalpha-for calculations
## pip install pyinstaller-for converting .py to .exe
from transform.transform import four_point_transform
from skimage.filters import threshold_local
import numpy as np
import argparse
import cv2
import imutils

import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import smtplib #for emails
import webbrowser as wb #for search purpose
import psutil
import pyjokes
import os
import pyautogui
import random
import json
import requests
from urllib.request import urlopen #for news go to newsapi.org, register and get api. There all the links for news headlines will be present in homepage after login.
import wolframalpha
import time

engine=pyttsx3.init()
wfa_id='9KQVKW-2JWA3T9AAQ'

def scandoc():
	# construct the argument parser and parse the arguments
	ap = argparse.ArgumentParser()
	ap.add_argument("-i", "--image", required = True,
		help = "Path to the image to be scanned")
	args = vars(ap.parse_args())
	
	# load the image and compute the ratio of the old height
	# to the new height, clone it, and resize it
	image = cv2.imread(args["image"])
	ratio = image.shape[0] / 500.0
	orig = image.copy()
	image = imutils.resize(image, height = 500)
	# convert the image to grayscale, blur it, and find edges
	# in the image
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (5, 5), 0)
	edged = cv2.Canny(gray, 75, 200)
	# show the original image and the edge detected image
	 ##############################################################################
	 ############### step-1 over ###################
	 #############################################################################
	 
	# find the contours in the edged image, keeping only the
	# largest ones, and initialize the screen contour
	cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)
	cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:5]

	screenCnt=None
	# loop over the contours
	for c in cnts:
		# approximate the contour
		peri = cv2.arcLength(c, True)
		approx = cv2.approxPolyDP(c, 0.02 * peri, True)
		# if our approximated contour has four points, then we
		# can assume that we have found our screen
		if len(approx) == 4:
			screenCnt = approx
			break
	# show the contour (outline) of the piece of paper

	 ##############################################################################
	 ############### step-2 over ###################
	 #############################################################################
	# apply the four point transform to obtain a top-down
	# view of the original image
	warped = four_point_transform(orig, screenCnt.reshape(4, 2) * ratio)
	# convert the warped image to grayscale, then threshold it
	# to give it that 'black and white' paper effect
	warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
	T = threshold_local(warped, 11, offset = 10, method = "gaussian")
	warped = (warped > T).astype("uint8") * 255
	# show the original and scanned images
	print("STEP 3: Apply perspective transform")
	cv2.imshow("Original", imutils.resize(orig, height = 650))
	cv2.imshow("Scanned", imutils.resize(warped, height = 650))
	cv2.waitKey(0)
	cv2.destroyAllWindows()


def sayjoke():
    speak(pyjokes.get_joke())

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

'''def screenshottaker(i):
    image=pyautogui.screenshot()
    image.save('D:/ML DL/JARVIS ASSISTANT/img[%d].png'%i)'''

def saytime():
    Time=datetime.datetime.now().strftime("%I:%M:%S") #for 24 hour- %H for 12 hour-%I 
    speak("The current time is")
    speak(Time)

def saydate():
    year=datetime.datetime.now().year
    month=datetime.datetime.now().month
    day=datetime.datetime.now().day
    speak("Today's date is")
    speak(day)
    speak(month)
    speak(year)

def sendemail(to,content):
    server=smtplib.SMTP('smtp.gmail.com',587) #port for gmail
    server.ehlo() #esmtp server
    server.starttls() #start connection between smtp server and tls
    server.login('rounakof1999@gmail.com','rounakiam')
    server.sendmail('rounakof1999@gmail.com',to,content)
    server.close()

def cpuusage():
    usage=str(psutil.cpu_percent())
    speak("The CPU is at"+usage)
    battery=psutil.sensors_battery()
    speak("Battery is at %d percentage"%battery.percent)

def wish():
    hour=datetime.datetime.now().hour
    if(hour>=6 and hour<12):
        speak("Good morning sir")
    elif(hour>=12 and hour<17):
        speak("Good afternoon sir")
    elif(hour>=17 and hour<23):
        speak("Good evening sir")
    else:
        speak("Good night sir")

    speak("Aatmanirbhar Insaan at your service. How can I help you?")

def TakeCommand():
    r=sr.Recognizer() #creating object of recognizer function
    with sr.Microphone() as source: #mentioning source of command
        print("Listening...")#log
        r.pause_threshold=1 #helps to determine how long machine will wait for user command   
        audio=r.listen(source) #stores audio from source

    try:
        print("Recognizing...")
        query=r.recognize_google(audio,language='en-US')
        print(query)
        #speak(query)
    
    except Exception as e:
        print(e)
        speak("Sorry say that again please")
        return "None"
    
    return query


if __name__ == "__main__":
    wish()
    i=0
    while True:
        query=TakeCommand().lower()

        if 'time' in query:
            saytime()
        elif 'date' in query:
            saydate()
        elif "email" in query:
            try:
                speak("What shall I say?")
                content=TakeCommand()
                speak("who is the receiver?")
                receiver=input("Enter receipient email address")
                #receiver='receiver_is_aritriknbpo@gmail.com'
                print(receiver)
                to=receiver
                sendemail(to,content)
                print(content)
                speak("Email has been sent successfully")
            except Exception as e:
                print(e)
                speak("Unable to send mail sir")
        elif 'wikipedia' in query or 'wiki' in query or 'define' in query:
            speak("Searching boss. Give me some time...")
            query=query.replace('wikipedia','')
            query=query.replace('define','')
            query=query.replace('wiki','')
            result=wikipedia.summary(query,sentences=3)
            speak("According to wikipedia,")
            print(result)
            speak(result)
        elif "search" in query:
            speak("Where to search sir? option1:google or option 2:youtube or option 3:chrome?")
            option=TakeCommand().lower()
            if 'two' in option or 'to' in option or 'too' in option or 'tu' in option:
                speak('What to search sir?')
                res=TakeCommand().lower()
                speak("Opening youtube for you sir...")
                wb.open('https://www.youtube.com/results?search_query='+res)
            elif 'three' in option or 'tree' in option or 'tee' in option or 't' in option:
                speak('What to search sir?')
                res=TakeCommand().lower()
                speak("Searching your query in google sir...")
                wb.open('https://www.google.com/search?q='+res)
            '''elif 'one' in option:
                path='C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
                search=TakeCommand().lower()
                wb.get(path).open_new_tab(search+'.com')'''
                 

        elif 'thank you' in query or 'bye' in query or 'good night' in query:
            speak('bye sir')
            break

        elif 'cpu' in query:
            cpuusage()

        elif 'joke' in query or 'jokes' in query:
            sayjoke()

        elif 'scan' in query:
            scandoc()
			
        '''elif 'open' in query:
            op=r'D:/Microsoft Teams/Teams_windows_x64.exe'
            speak("Opening the requested file for you")
            os.startfile(op)''' 

        '''elif 'take note' in query:
            speak('What to note down sir?')
            notes=TakeCommand()
            time=str(datetime.datetime.now())
            f=open('D:/ML DL/JARVIS ASSISTANT/NOTES/abc.txt','a+')
            f.write(time)
            f.write(':-')
            f.write(notes+'\n')
            f.close()
            speak("Done taking notes!!")
        
        elif 'read note' in query:
            speak("Reading the notes..")
            f=open("D:/ML DL/JARVIS ASSISTANT/NOTES/abc.txt",'r')
            print(f.read())
            speak(f.read())'''

        '''elif 'screenshot' in query:
            speak("Taking screenshot..")
            screenshottaker(i)
            i+=1'''

        '''elif 'play' in query:
            mdir='D:/MOVIES/FRESH NEW MOVIES/Ab/AB/DOWNLOADED'
            sdir='D:/SERIES/Mr. Robot/Season 1'
            speak("What to play sir? movie or tv show?")
            choice=TakeCommand().lower()
            while('movie' not in choice and 'tv show' not in choice):
                speak("Cannot understand your choice sir. Please state clearly?")
                choice=TakeCommand().lower()
            if 'movie' in choice:
                dir=mdir
            elif 'tv show' in choice:
                dir=sdir
            mov=os.listdir(dir)
            speak("Which one shall I play sir? State a number.")
            c=TakeCommand().lower()
            while('number' not in c and 'random' not in c and 'any' not in c):
                speak("Not clear sir. Please choose a number.")
                c=TakeCommand().lower()
            if 'number' in c: 
                n=int(c.replace('number',''))
            elif 'random' in c or 'any' in c:
                n=random.randint(0,len(mov))
            os.startfile(os.path.join(mdir,mov[n]))

        elif 'remember' in query:
            speak("What to remember sir?")
            f=open('D:/ML DL/JARVIS ASSISTANT/NOTES/remember.txt','a+')
            mem=TakeCommand().lower()
            if('none' not in mem and 'nan' not in mem):
                speak("Memory saved sir..")
                print(mem)
                f.write(mem)
                f.close()
            else:
                f.write('')
                f.close()

        elif 'remind' in query:
            speak("Checking memory sir....")
            f=open('D:/ML DL/JARVIS ASSISTANT/NOTES/remember.txt','r')
            filesize = os.path.getsize("D:/ML DL/JARVIS ASSISTANT/NOTES/remember.txt")
            if(filesize!=0):
                speak("You asked me to remember that-"+f.read())
                print(f.read())
            else:
                speak("Nothing to remeber sir")'''

        '''elif 'news' in query:
            try:
                jst=urlopen("http://newsapi.org/v2/top-headlines?sources=techcrunch&apiKey=dd6ece3e0a5f40bc934ad7b7f6f50a2a")
                jsb=urlopen("http://newsapi.org/v2/top-headlines?country=in&category=business&apiKey=dd6ece3e0a5f40bc934ad7b7f6f50a2a")
                jsj=urlopen("http://newsapi.org/v2/everything?domains=wsj.com&apiKey=dd6ece3e0a5f40bc934ad7b7f6f50a2a")
                speak("Select one category please; Entertainment, technology, business or journal")
                ct=TakeCommand().lower()
                while('business' not in ct and 'technology' not in ct and "journal" not in ct):
                    speak("Please select a proper news category..")
                    ct=TakeCommand().lower()
                if('technology' in ct):
                    d=json.load(jst)
                elif('business' in ct):
                    d=json.load(jsb)
                elif('journal' in ct):
                    d=json.load(jsj)
                j=1
                speak("Here are some headlines from news industry..")
                for item in d['articles']:
                    print(str(j)+'. '+item['title'])
                    print(item['description'])
                    speak(item['title'])
                    j+=1
            except Exception as e:
                print(str(e))
                speak("Unable to fetch news right now sir.")

        elif 'where is' in query:
            query=query.replace("where is ","")
            speak("Showing location for"+query)
            wb.open_new_tab("https:/google.com/maps/place/"+query)

        elif 'calculate' in query:
            client=wolframalpha.Client(wfa_id)
            ind=query.split().index('calculate')
            query=query.split()[ind+1:]
            res=client.query(''.join(query))
            ans=next(res.results).text
            speak("The answer to your query is-"+str(ans))
            print("The answer to your query is-"+str(ans))

        elif 'what is' in query or 'who is' in query:
            client=wolframalpha.Client(wfa_id)
            res=client.query(query)
            try:
                print(next(res.results).text)
                speak(next(res.results).text)
            except Exception as e:
                print(e)
                speak("I dont know the answer to your question sir...")

        elif 'rest' in query:
            speak("for how many seconds sir?")
            ans=int(TakeCommand())
            time.sleep(ans)
            print(ans)

        elif 'ok' in query:
            speak('Anything else I can do for you sir?')
            z=TakeCommand().lower()
            if 'yes' in z:
                speak("At your service")
            else:
                speak("Bye sir..")
                break

        elif 'log out' in query:
            os.system("shutdown -l")
        elif 'restart' in query:
            os.system("shutdown /r /t 1")
        elif 'shutdown' in query or 'shut down' in query:
            os.system("shutdown /s /t 1")'''


        

        

            
        

        
