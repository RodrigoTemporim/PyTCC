from sys import displayhook
import tkinter as tk
from tkinter import *
from tkinter import filedialog
import pandas as pd


def openFile():
   filepath = filedialog.askopenfilename()
   dinheiro_df = pd.read_excel(filepath)  
   print(dinheiro_df) 
   print(dinheiro_df.describe())
   # file = open(filepath, 'r')   
   # print(file.read())
   # file.close()
   

window = Tk()
button = Button(text="Open", command=openFile)
button.pack()
window=mainloop()