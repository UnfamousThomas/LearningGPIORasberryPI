import RPi.GPIO as GPIO
import time

#Board tüüpi channel numbrid
GPIO.setmode(GPIO.BOARD)

#Eemalda warningud (seoses varasema rasberrypi samade chanellite kasutusega)
GPIO.setwarnings(False)

#Defineeri auto foori pinnide numbrid
redPin_car = 22
yellowPin_car = 24
greenPin_car = 26

#Defineeri inimese foori pinnide ja sinise foori pinnide numbrid
green_person = 31
red_person = 29
blue_person  = 37

#Defineeri nuppu number
buttonPin = 40

#Defineeri kas jalakäija on schedulitud järgmiseks tsükkliks, alguses defaultina ei ole
scheduled = False

#Setupi auto fooride pinnid outputtidena
GPIO.setup(yellowPin_car, GPIO.OUT)
GPIO.setup(redPin_car, GPIO.OUT)
GPIO.setup(greenPin_car, GPIO.OUT)

#Defineeri jalakäija foorid ja sinine foor outputidena
GPIO.setup(green_person, GPIO.OUT)
GPIO.setup(red_person, GPIO.OUT)
GPIO.setup(blue_person, GPIO.OUT)

#Defineeri nupp inputina. Ma veel PUD_UPist 100% aru ei saa aga teoorias PUD_UP peaks tähendama seda et nuppu vajutusel eeldan et "voltage" tõmmatakse alla 0i peale. 
#Seda selle pärast et muidu defaultina võib see olla mingi float 0 ja 1 vahel.
GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#Utility method selleks et ei peaks kirjutama pikka rida et panna tööle tuld
def on(channel):
    GPIO.output(channel, GPIO.HIGH)
    
#Utility method selleks et ei peaks kirjutama pikka rida et tuld välja lülitada
def off(channel):
    GPIO.output(channel, GPIO.LOW)

#Lülita välja kõik auto foorid
def reset_car():
    off(redPin_car)
    off(greenPin_car)
    off(yellowPin_car)

#Lülita välja kõik jalakäija foorid
def reset_person():
    off(green_person)
    off(blue_person)
    off(red_person)

#Kuna vahel cleanup() ei resetti korralikult siis need meetodid teevad seda manuaalselt iga runni alguses (s.t lülitab kõik tuled välja)
reset_car()
reset_person()

#Loogika juhul kui on jalakäija nuppu vajutatud
def handleGreenWalk():
    #Lülita välja punane jalakäija ja sinine tuli
    off(red_person)
    off(blue_person)
    #Lülita sisse roheline jalakäija tuli
    on(green_person)
    #Oota 5 sekundit
    time.sleep(5)
    #Lülita välja roheline jalakäija tuli
    off(green_person)
    #Lülita sisse punane jalakäija tuli
    on(red_person)
    #Global siin tähendab seda et me ei muudaks seda väärtust ainult funktsiooni sees vaid terves programmis
    global scheduled
    #Muuda scheduled väärtus vääraks
    scheduled = False


#Kuidas reageerida nuppu vajutusele
def onClickEvent(channel):
    #Lülita sisse sinine tuli
    on(blue_person)
    #Global siin tähendab seda et me ei muudaks seda väärtust ainult funktsiooni sees vaid terves programmis
    global scheduled
    #Muuda scheduled väärtus tõeseks
    scheduled = True

#Event listener (ehk nn "Kuulame") nuppu vajutuse jaoks
GPIO.add_event_detect(buttonPin,GPIO.RISING,callback=onClickEvent,bouncetime=100)

#Meetod et kollane tuli vilguks
def handleYellowBlink():
    #Loopi muutuja
     i = 0
     #Loopi setup
     while i < 3:
         #Kollane autofoor sisse
         on(yellowPin_car)
         #Oota 3ndit sekundit
         time.sleep(1/3)
         #Kollane autofoor välja
         off(yellowPin_car)
         #Oota 3ndik sekundit
         time.sleep(1/3)
         #Loopi muutuja muutmine
         i += 1
        
#Seda võiks kutsuda ka nn "main methodiks", see käib lõpmatuseni kuni programm välja lülitub 
def defaultBehavior():
    #Korda koodi lõpmatuseni
    while True:
        #Kui on jalakäija nuppu vajutatud
        if scheduled:
            #Lülita sisse punane auto foor
            on(redPin_car)
            #Jalakäija foori loogika
            handleGreenWalk()
        #Kui ei ole jalakäija nuppu vajutatud
        else:
            #Lülita sisse punane auto foor
            on(redPin_car)
            #Lülita sisse punane tuli (igaks juhuks, et see oleks programmi alguses sees)
            on(red_person)
            #Oota 5 sekundit
            time.sleep(5)
        #Lülita punane auto foor välja
        off(redPin_car)
        #Lülita kollane foor sisse
        on(yellowPin_car)
        #Oota 1 sekund
        time.sleep(1)
        #Lülita kollane foor välja
        off(yellowPin_car)
        #Lülita sisse roheline auto foor
        on(greenPin_car)
        #Ooota 5 sekundit
        time.sleep(5)
        #Lülita roheline tuli välja
        off(greenPin_car)
        #Kollase tule vilkumise loogika funktsiooni kutsumine
        handleYellowBlink()
        
#Kutsu eelnevalt üles seadistatud funktsioon mis töötab lõpmatuseni
defaultBehavior()

#Cleanup peaks teoorias kõik tuled jne ära kustutama
GPIO.cleanup()
