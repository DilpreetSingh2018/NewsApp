#####################################################################
#   Authors:Dilpreet Singh                                          #
#   Version 1.1                                                     #
#   Minor Project - News App                                        #
#                                                                   #
#   Related files -                                                 #
#       > data.txt                                                  #
#       > NewsLogo.ico                                              #
#       > default-no-img.jpg                                        #
#       > patch.txt                                                 #
#                                                                   #
#   For any queries contact the below:                              #
#   cse9510dilpreet@gmail.com  (+91 9888042018)                     #
#                                                                   #
#####################################################################

from newsapi.newsapi_client import NewsApiClient # This module is required to fetch news
from tkinter import * # This module is used to develop the GUI for the code
from win32com.client import Dispatch # This module is used to give a voice output from the system
import webbrowser # This module is used to open a web browser
from urllib.request import urlopen # This module is used to work with URL's
from PIL import ImageTk,Image # This module is used for working with images
import json # This module is used for converting JSON to string
import io # Here we can store our data as bytes

# This function is used to give voice output for the string (news description) provided to it.
def speak(str):
    speak = Dispatch("SAPI.SpVoice")
    speak.Speak(str)

# This function helps us to attain the facility of storing the last fetched news in the file named "data.txt."
def updateDefaultFile(data):
    with open("data.txt", "w") as f:
        f.write(json.dumps(data)) # It re-writes the file with the new data provided to it.

# This is the main class that is used to make our app work
class NewsApp:
    def __init__(self): # Constructor

        # Fetching data
        self.flag = 0 # This flag suggests that the program is unable to fetch the news. It's default value is zero.
        
        try: # This try block tries to fetch the news.
            self.newsapi = NewsApiClient(api_key='ee0714fafee04e888856f536e15292fe') # This is the unique API key used to fetch the news
            self.data = self.newsapi.get_top_headlines(language="en") # Getting headlines!
            
            # Update default file
            updateDefaultFile(self.data)

        except: # In case the try block fails, we will come to this block
            self.flag = 1 # This flag is now set to one because we failed to fetch the news in the try block due to no internet connection. If this flag is set to one, we will initiate the process of retrieving the data from the "data.txt"
            with open("data.txt", "r") as f: # We are now opening this file in read mode to retrieve the data
                self.data = json.loads(f.read()) # Here we are converting string into JSON to process it again

        # Initial GUI load
        self.load_gui()
        # Loading the 1st news item
        self.load_news_item(0) # Zero here denotes the index value

    def load_gui(self):
        self.root = Tk() # Root here is the name of App window
        self.root.geometry('350x620') # Window size is 350 pixels height and 600 pixels width
        self.root.iconbitmap('NewsLogo.ico') # This is the app logo
        self.root.resizable(0,0) # This is used so that window doesn't get resized
        self.root.title('News App') # Title of the window
        self.root.configure(background='black') # Background colour of the window

    # This function is used to clear the screen for new news item.
    def clear(self):
        for i in self.root.pack_slaves():
            i.destroy() # Helps to destroy all the widgets

    # This function helps to display and output the fetched news.
    def load_news_item(self,index):
        self.clear() # Calling clear function

        # Trying to process images
        try:
            img_url = self.data['articles'][index]['urlToImage']
            raw_data = urlopen(img_url).read()
            im = Image.open(io.BytesIO(raw_data)).resize((350,250))
            photo = ImageTk.PhotoImage(im)
        
        except: # This block is used in cases where there is no image available for the news
            photo = ImageTk.PhotoImage(file='default-no-img.jpg')

        label = Label(self.root,image=photo)
        label.pack() # Placing the processed image on the window

        heading = Label(self.root,text=self.data['articles'][index]['title'],bg='black',fg='white',wraplength=350,justify='center') # Displays the title of the news
        heading.pack(pady=(10,20))
        heading.config(font=('verdana',15))

        details = Label(self.root, text=self.data['articles'][index]['description'], bg='black', fg='white', wraplength=350,justify='center') # Displays the description of the news
        details.pack(pady=(2, 20))
        details.config(font=('verdana', 12))

        frame = Frame(self.root,bg='black') # Creates frames on the window
        frame.pack(expand=True,fill=BOTH)

        if index != 0:
            prev = Button(frame,text='Previous',width=12,height=3,command=lambda :self.load_news_item(index-1))
            prev.pack(side=LEFT) # Button to go back to the previous news

        read = Button(frame, text='Read More', width=12, height=3,command=lambda :self.open_link(self.data['articles'][index]['url']))
        read.pack(side=LEFT) # Button to open the URL of the source of news
        speaknews = Button(frame, text='Read News', width=12, height=3,command=lambda :speak(self.data['articles'][index]['description']))
        speaknews.pack(side=LEFT) # This button is used to voice output the description of the news

        if index != len(self.data['articles'])-1:
            next = Button(frame, text='Next', width=12, height=3,command=lambda :self.load_news_item(index+1))
            next.pack(side=LEFT) # Button to show next news
        if self.flag == 1:
            no_internet = Label(self.root, text="No internet connection. Loading previously fetched news...", bg='red', fg='white', width=50)
            no_internet.pack() # Used to show the no internet connection message

        self.root.mainloop() # Main loop of the app window

    def open_link(self,url):
        webbrowser.open(url) # To open web browser when clicked the button "Read More"

obj = NewsApp() # Object of the NewsApp Class
