import requests
import bs4
import tkinter as tk
import plyer
import time
import datetime
import threading
from time import strftime 
from PIL import ImageTk
import regex as re
def get_html_data(url):
    data = requests.get(url)
    return data

def get_corona_detail():
    url = "https://www.mohfw.gov.in/"
    html_data = get_html_data(url)
    bs = bs4.BeautifulSoup(html_data.text,'html.parser')
    info_div = bs.find("div",class_="site-stats-count").find_all("li",class_=re.compile("bg-."))
    all_details = ""
    for block in info_div:
        # print(block)
        count = block.find("strong").get_text()
        text = block.find("span").get_text()
        # print(f'{text} : {count}')
        all_details = all_details + text + " : " + count + "\n"
    return all_details

def refresh():
    newdata = get_corona_detail()
    print('Refreshing..')
    mainLabel['text'] = newdata

#notification
def notify():
    while True:
        plyer.notification.notify(
            title='COVID 19 cases of INDIA',
            message=get_corona_detail(),
            timeout=10
            # app_icon = 'covid.jpg'
        )
        time.sleep(20)

def time():
    string = strftime('%H:%M:%S %p')
    lbl.config(text = string)
    lbl.after(1000, time)

# get_corona_detail()
root = tk.Tk()
root.geometry("700x600")
# root.iconbitmap("icon.ico")
root.title("COVID Data Tracker - INDIA")
root.configure(background ="black")
f = ("Comic Sans MS",25,"bold")
banner = ImageTk.PhotoImage(file="images.jpg")
bannerLabel = tk.Label(root,image=banner)
bannerLabel.pack()
mainLabel = tk.Label(root,text = get_corona_detail(),font=f,bg='black',foreground='white')
mainLabel.pack()

rebtn = tk.Button(root,text='Refresh',font=f,relief='solid',command=refresh)
rebtn.pack()

lbl = tk.Label(root, font = f,bg='black',fg='white')
lbl.pack(pady=20)
time()
#create new thread
th1 = threading.Thread(target=notify)
th1.setDaemon(True)
th1.start()
root.mainloop()