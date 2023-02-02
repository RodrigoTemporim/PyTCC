import tkinter as tk
from tkinter import filedialog,ttk
import pandas as pd



root = tk.Tk()
root.geometry('700x700')
root.pack_propagate(False)
root.resizable(0, 0)


# icon photo
root.iconbitmap('SC-S-BRANCO.ico')

# tittle
root.title('SC Contabilidade')


# Frame for Treeview
frame1 = tk.LabelFrame(root, text="Excel Data", font='Gothan')
frame1.place(height=400, width=400)

# Filtros
file_frame = tk.LabelFrame(root, text='Fitros', font='Gothan 20 italic bold')
file_frame.place(height=300, width=200, rely=0.100, relx=0.6)

# Buttons3
button3 = tk.Button(file_frame, text='Negativo',
                    font='Gothan',activebackground="#f00", activeforeground="#fff", command=lambda: filter_neg())
button3.place(rely=0.100, relx=0.100)

button4 = tk.Button(file_frame, text='Positivo',
                    font='Gothan',activebackground="#f00", activeforeground="#fff", command=lambda: filter_posi())
button4.place(rely=0.300, relx=0.100)

button5 = tk.Button(file_frame, text='Conciliado',
                    font='Gothan',activebackground="#f00", activeforeground="#fff", command=lambda: filter_conc())
button5.place(rely=0.500, relx=0.100)

# open file
file_frame = tk.LabelFrame(root, text='Open File',font='Gothan 20 italic bold')
file_frame.place(height=160, width=400, rely=0.65, relx=0.2)

# Buttons
button1 = tk.Button(file_frame, text='Selecionar Arquivo',
                    font='Gothan', command=lambda: File_dialog())
button1.place(rely=0.65, relx=0.50)

button2 = tk.Button(file_frame, text='Calcular',
                    font='Gothan',activebackground="#f00", activeforeground="#fff", command=lambda: view_Excel(Excel_cals()))
button2.place(rely=0.65, relx=0.20)

button6 = tk.Button(file_frame, text='Exportar',
                    font='Gothan',activebackground="#f00", activeforeground="#fff", command=lambda: export())
button6.place(rely=0.220, relx=0.20)

label_file = ttk.Label(file_frame, text='No file Selected', font='Gothan')
label_file.place(relx=0, rely=0)

tv1 = ttk.Treeview(frame1)
tv1.place(relheight=1, relwidth=1)

treescrolly = tk.Scrollbar(frame1, orient='vertical', command=tv1.yview)
treescrollx = tk.Scrollbar(frame1, orient='horizontal', command=tv1.xview)
tv1.configure(xscrollcommand=treescrollx.set, yscrollcommand=treescrolly.set)
treescrollx.pack(side='bottom', fill='x')
treescrolly.pack(side='right', fill='y')


data_frame = pd.DataFrame()

def newColumnString(file, string, string1):  # Delete all string values
    file[string1] = file[string].str.split('-', n=1).str.get(0)
    file[string1] = file[string1].str.replace('\D+', '')


def notString(file, string):  # Delete all string values
    file[string] = file[string].str.replace('\D+', '')


def intoNumber(file, string, string1):
    # drop all the rows with null values
    file = file.dropna(how='all', subset=['Saldo'])
    file = file.fillna({string: 0, string1: 0}).fillna(
        0)  # replace the values NaN to 0 in columns ''
    file[[string, string1]] = (file[[string, string1]].apply(pd.to_numeric)).astype(
        float)  # converter todos as nossas colunas desejadas no tipo float
    return file


def File_dialog():
    filepath = filedialog.askopenfilename(title='Selecione o arquivo')

    label_file['text'] = filepath
    return None

def view_Excel(df):      
    try:        
        print('a')
    except ValueError:
        tk.messagebox.showerror(
            'Information', 'the file you have choose is invalid')
        return None
    except FileNotFoundError:
        tk.messagebox.showerror(
            'Information', f'no suck file as {Excel_cals()}')
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


def Excel_cals():
    global data_frame
    file_path = label_file['text']
    csv_df = pd.read_csv(file_path, encoding='latin-1',
                         sep=';', decimal=',')   # read csv
    newColumnString(csv_df, 'Histórico', 'Nº da Nota')
    notString(csv_df, 'Débito')
    notString(csv_df, 'Crédito')
    csv_df = intoNumber(csv_df, 'Crédito', 'Débito')
    csv_df.eval('Conciliação = Débito - Crédito', inplace=True, target=csv_df)
    csv_dfClean = csv_df.drop(['Crédito', 'Débito'], axis=1)
    novo_csvdf = csv_dfClean.groupby(['Nº da Nota'])[
        'Conciliação'].sum().reset_index()
    novo_csvdf['Conciliação'] = (novo_csvdf['Conciliação'] * 0.01).round(2)
    newIndex = novo_csvdf.sort_values(by=['Conciliação'])
    newIndexNoDuplicates = newIndex.drop_duplicates()
    data_frame = newIndexNoDuplicates
    return newIndexNoDuplicates
    
    
def filter_neg():    
    df_negativo = (Excel_cals().query(' Conciliação < 0'))
    
    global data_frame
    data_frame = df_negativo
    
    view_Excel(df_negativo)
    
    
    
 
def filter_posi():    
    df_positivo = (Excel_cals().query(' Conciliação > 0'))
   
    global data_frame
    data_frame = df_positivo
    
    view_Excel(df_positivo)
    
    
    
    
def filter_conc():    
    df_conciliado = (Excel_cals().query(' Conciliação == 0'))    
    
    global data_frame
    data_frame = df_conciliado
    
    view_Excel(df_conciliado)
    

def export():      
    
    files = [('Csv', '*.csv'), 
             ('Excel', '*.xls'),
             ('Text Document', '*.txt')]    
    file = filedialog.asksaveasfile(filetypes = files, defaultextension = files)  
    data_frame.to_csv(file, index=False, encoding='utf-16', sep=';')
    



def clear_data():
    tv1.delete(*tv1.get_children())


root.mainloop()
