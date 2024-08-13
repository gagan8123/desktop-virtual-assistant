from decimal import InvalidOperation
import win32com.client
import sqlite3 
import speech_recognition as sr
import os
import pandas
import google.generativeai as genai
from IPython.display import display
from IPython.display import Markdown
import time





genai.configure(api_key="")
speaker = win32com.client.Dispatch("SAPI.SpVoice")
conn = sqlite3.connect("personal.db")
cursor = conn.cursor()
model = genai.GenerativeModel('gemini-1.5-flash')
# model = genai.GenerativeModel('gemini-pro-vision')
# model = genai.GenerativeModel(model_name="gemini-pro-vision")
# response = model.generate_content(["What's in this photo?", img])

#prints the text letter by letter




def show_login_history():
    cursor = conn.cursor()
    res = cursor.execute("select * from history;").fetchall()
    dat = []
    login_time = []
    logout_time = []
    for i in res:
        dat.append(i[0])
        login_time.append(i[1])
        logout_time.append(i[2])
    output = pandas.DataFrame({"date":dat,"login time":login_time,"logout time":logout_time})
    print(output) 

def takecmd(repeat:bool=True)->str:
    print("Listening.....................")
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            r.pause_threshold = 0.5
            r.adjust_for_ambient_noise(source, duration=1)
            audio = r.listen(source,timeout=4)
            text = r.recognize_google(audio,language="en-in")
        print(text,type(text))
        if  text : 
            print(f"\"{text}\"")
            return f"{text}"
    except  Exception as e:  
        
        os.system("cls")
        print(e)
        if(repeat):
            if(len(str(e))):
                print(e)
                speaker.Speak("Sorry  could not get that, Please say again.")
                return takecmd(repeat)
            
# def to_markdown(text):
#   text = text.replace('•', '  *')
#   return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))    

def formate_message(mesge):
    try:
        messages = [
        {'role':'user',
        'parts': [f"correct the grammar and modify the sentence, - \" {mesge}\" .  just describe without explanation "]}
        ]
        response = model.generate_content(messages)
        return response.text
    except Exception as e:
        return mesge
    

def checktable():
    conn.execute("create table  if not exists history (datee varchar(20) not null,start_time varchar(30),end_time varchar(20),sino INTEGER PRIMARY KEY autoincrement)")
    
    conn.execute("create table  if not exists emails(name varchar(30) primary key, email varchar(100) not null,emergency varchar(20))")
    
    conn.execute("create table  if not exists contact(name varchar(30) primary key, mob_number varchar(10) not null,emergency varchar(20));")
    conn.commit()
    
def get_message_info(mesge):
    mesge = str(mesge).replace("gemini","",1)
    try:
        messages = [
        {'role':'user',
        'parts': [f" '{mesge}'  ,\n note: no explanation needed , just give only 2 sentence and dont even explain anything \nand  just give a reply back messages"]}
        ]
        response = model.generate_content(messages).text
        print(response)
        
       
        return response

        
    except Exception as e:
        return "irrelavent questions"