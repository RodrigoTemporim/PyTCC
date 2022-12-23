import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
import numpy as np

root = tk.Tk()
root.geometry('1200x700')
root.pack_propagate(False)
root.resizable(0, 0)


#icon photo
root.iconbitmap('SC-S-BRANCO.ico')


#tittle
root.title('SC Contabilidade')


# Frame for Treeview
frame1 = tk.LabelFrame(root, text="Excel Data", font='Georgia')
frame1.place(height=400, width=1200)


#open file
file_frame = tk.LabelFrame(root, text='Open File', font='Georgia 20 italic bold')
file_frame.place(height=140, width=400, rely=0.65, relx=0.2)

#Buttons
button1 = tk.Button(file_frame, text='Selecionar Arquivo', font='Georgia', command=lambda: File_dialog())
button1.place(rely=0.65, relx=0.50)

button2 = tk.Button(file_frame, text='x1', font='Georgia', command=lambda: view_Excel())
button2.place(rely=0.65, relx=0.20)

label_file = ttk.Label(file_frame, text='No file Selected', font='Georgia')
label_file.place(relx=0, rely=0)

tv1 = ttk.Treeview(frame1)
tv1.place(relheight=1, relwidth=1)

treescrolly = tk.Scrollbar(frame1, orient='vertical', command=tv1.yview)
treescrollx = tk.Scrollbar(frame1, orient='horizontal', command=tv1.xview)
tv1.configure( xscrollcommand= treescrollx.set, yscrollcommand= treescrolly.set)
treescrollx.pack(side='bottom', fill='x')
treescrolly.pack(side='right', fill='y')


def notString(file, string): # Delete all string values
   file[string] = file[string].str.replace('\D+', '')
   
def intoNumber(file, string, string1):
   file = file.dropna(how='all') # drop all the rows with null values
   file = file.fillna({string:0, string1 :0}).fillna(0) # replace the values NaN to 0 in columns ''
   file[[string, string1]] = file[[string, string1]].apply(pd.to_numeric)
   file[string] = file[string] *(-1)# change the type of columns
   
   return file

def File_dialog():
    filepath = filedialog.askopenfilename(title='Selec a File')
    
    label_file['text'] = filepath
    return None    

def view_Excel():
    file_path = label_file['text']
    csv_df = pd.read_csv(file_path, encoding='latin-1', sep=';')   # read csv 
    notString(csv_df, 'Histórico')   
    notString(csv_df, 'Débito')
    notString(csv_df, 'Crédito') 
    csv_df = intoNumber(csv_df, 'Crédito', 'Débito')    
    csv_df.eval('variance = Crédito + Débito' ,inplace=True)  
    csv_dfClean = csv_df.drop(['Crédito', 'Débito'], axis=1)
    newIndex = csv_dfClean.sort_values(by=['variance'])
    newIndexNoDuplicates = newIndex.drop_duplicates()       
    try:
       df = newIndexNoDuplicates
       print(df)      
    except ValueError:
        tk.messagebox.showerror('Information', 'the file you have choose is invalid')
        return None
    except FileNotFoundError:
        tk.messagebox.showerror('Information', f'no suck file as {newIndexNoDuplicates}')
        return None
    
    clear_data()
    tv1['column'] = list(df.columns)
    tv1['show'] = 'headings'
    for column in tv1['column']:
        tv1.heading(column, text=column) 
             
    df_rows = df.to_numpy().tolist()
    for row in df_rows:
        tv1.insert('', 'end', values=row)
    return None


def clear_data():
    tv1.delete(*tv1.get_children())

root.mainloop()