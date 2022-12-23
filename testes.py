import tkinter as tk
from tkinter import *
from tkinter import filedialog
import pandas as pd
import numpy as np
import interface as i


def notString(file, string): # Delete all string values
   file[string] = file[string].str.replace('\D+', '')
   
def intoNumber(file, string, string1):
   file = file.dropna(how='all') # drop all the rows with null values
   file = file.fillna({string:0, string1 :0}).fillna(0) # replace the values NaN to 0 in columns ''
   file[[string, string1]] = file[[string, string1]].apply(pd.to_numeric)
   file[string] = file[string] *(-1)# change the type of columns
   
   return file
     

def openFile(): # function open 
   filepath = filedialog.askopenfilename() #select file path
   csv_df = pd.read_csv(filepath, encoding='latin-1', sep=';')   # read csv 
   notString(csv_df, 'Histórico')   
   notString(csv_df, 'Débito')
   notString(csv_df, 'Crédito') 
   csv_df = intoNumber(csv_df, 'Crédito', 'Débito')    
   csv_df.eval('variance = Crédito + Débito' ,inplace=True)  
   csv_dfClean = csv_df.drop(['Crédito', 'Débito'], axis=1)
   newIndex = csv_dfClean.sort_values(by=['variance'])
   newIndexNoDuplicates = newIndex.drop_duplicates()  
   print(newIndexNoDuplicates)
   #136115
   
  #newIndexNoDuplicates.to_csv('D:/Rodrigo/Documents/teste1.csv', encoding='utf-8', header=True, sep=';')
  #csv_dfClean.to_csv(filepath, encoding='utf-8', header=True, sep='\t') #save file

window = Tk() 
button = Button(text="Open", command=openFile) 
button.pack()
window=mainloop() 

