#!/usr/bin/python

####This file will add a GUI to the Raspberry Pi Touch Screen to control the screen brightness without
####the need to manually enter values to Terminal. It also reads to make sure there is a Raspberry Pi
####Touch Screen available and that the OS is correct. After running this for the first time it will copy its
####self to the home directory (/home/pi) as a hidden file and add its self to the menu under 'Settings'
####so it can be easily called.

##Writen By Lynton Brown

##      ##      ##      ##      ##      ##      ##      ##      ##      ##      ##      ##      ##      ##      ##      ##
from Tkinter import Tk , mainloop, Scale, Label, HORIZONTAL, DISABLED
from os import path, system
##      ##      ##      ##      ##      ##      ##      ##      ##      ##      ##      ##      ##      ##      ##      ##
brightness = '/sys/class/backlight/rpi_backlight/brightness'
text = ""
currentSetting = 255
newSetting = 0
##      ##      ##      ##      ##      ##      ##      ##      ##      ##      ##      ##      ##      ##      ##      ##
def writeBrightness(newSetting):
        brightness = '/sys/class/backlight/rpi_backlight/brightness'
        system('sudo chmod 777 %s'%(brightness))
        with open(brightness,"w") as brightness:
                brightness.write(newSetting)
                brightness.flush()
                brightness.close()
                system('sudo chmod 755 %s'%(brightness))
##      ##      ##      ##      ##      ##      ##      ##      ##      ##      ##      ##      ##      ##      ##      ##
master = Tk()
master.title ("RPi Screen Brightness")
master.resizable (width = False, height = False)
master.geometry("350x100")
sliderBar = Scale(master, from_=10, to_=255, orient=HORIZONTAL, length= 250, width=20)
sliderBar.set(currentSetting)
sliderBar.pack()
label = Label(master, text = text)
##      ##      ##      ##      ##      ##      ##      ##      ##      ##      ##      ##      ##      ##      ##      ##
if path.isdir('/home/pi'):
        sliderBar.configure(command = writeBrightness)
        menuItem = '/home/pi/.BrightnessSettings.py'
##      ##      ##      ##      ##      ##      ##      ##      ##      ##      ##      ##      ##      ##      ##      ##        
        if path.isfile(menuItem):
                pass
##      ##      ##      ##      ##      ##      ##      ##      ##      ##      ##      ##      ##      ##      ##      ##        
        else:
                print"Writing File"
                with open('./BrightnessSettings.py', 'r') as src, open ('/home/pi/.BrightnessSettings.py', 'w') as dst:
                        dst.write(src.read())
                with open('/home/pi/.local/share/applications/BrightnessSettings.desktop', 'w') as dsktp:
                        dsktp.writelines('[Desktop Entry] \nComment=Change Brightness on 7inch Touchscreen'+
                                                        '\nTerminal=false \nName=Brightness Setting\nExec=/home/pi/.BrightnessSettings.py'+
                                                        '\nType=Application\nIcon=preferences-desktop-display\nNoDisplay=false\nCategories=System')
                system('chmod +x /home/pi/.BrightnessSettings.py')
##      ##      ##      ##      ##      ##      ##      ##      ##      ##      ##      ##      ##      ##      ##      ##                
        if path.isfile(brightness):
                with open(brightness, "r") as brightness:
                        currentSetting = brightness.readline()
                        brightness.close()
##      ##      ##      ##      ##      ##      ##      ##      ##      ##      ##      ##      ##      ##      ##      ##                        
        else:
                label.configure(text = "Offical Raspberry Pi Touch Screen \nNot Found")
                label.pack()
##      ##      ##      ##      ##      ##      ##      ##      ##      ##      ##      ##      ##      ##      ##      ##                
else:
        label.configure(text = "This is Not a \nRaspberry Pi")
        label.pack()
        sliderBar.configure(state = DISABLED)
##      ##      ##      ##      ##      ##      ##      ##      ##      ##      ##      ##      ##      ##      ##      ##
mainloop()
