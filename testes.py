from sys import displayhook
import tkinter as tk
from tkinter import *
from tkinter import filedialog
import pandas as pd



def openFile(): # função pra de abrir a janela
   filepath = filedialog.askopenfilename() #vai selecionar o path do arquivo selecionado
   dinheiro_df = pd.read_csv(filepath, encoding='latin-1', sep=';')   # vai ler o excel no path encontrado no anterior
   dinheiro_df['Histórico'] = dinheiro_df['Histórico'].str.replace('\D+', '')   # vai limnpar a coluna historico  mantendo apenas o codigo das contas
   seleta = dinheiro_df.dropna(how='all') # vai limpar a coluna historico eliminando todos as linhas completamente vazias 
   print(seleta)
    

window = Tk() # coisa do tkinter pra abrir a janela
button = Button(text="Open", command=openFile) # ela abre aqui quando apertar o botão no command!!!!
button.pack()
window=mainloop() # mantém em loop