from sys import displayhook
import tkinter as tk
from tkinter import *
from tkinter import filedialog
import pandas as pd


def openFile():
   filepath = filedialog.askopenfilename()
   dinheiro_df = pd.read_excel(filepath)   
   dinheiro_df['Histórico'] = dinheiro_df['Histórico'].str.replace('\D+', '')   
   seleta = dinheiro_df.dropna(how='all')
   print(seleta)
    
   
   
#    notas = dinheiro_df['Histórico']
#    # file = open(filepath, 'r')   
#    # print(file.read())
#    # file.close()
   

window = Tk()
button = Button(text="Open", command=openFile)
button.pack()
window=mainloop()