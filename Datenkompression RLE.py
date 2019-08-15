#Autor: Stefan Chalupka (6037666), Marcel Brück (6192721)
#Seminar Datenkompression 2018
#Dozent: Dr.Vuong

from copy import deepcopy
from tkinter import *
from tkinter import filedialog
from functools import partial
import time, math, random, sys, getpass, os

sys.setrecursionlimit(50000)                    #Rekursionslimit sonst nicht hoch genug
user = getpass.getuser()                        #Feststellung von Systemuser
solution_path ='C:/Users/'+user+'/Desktop/ProgramRLE/Ergebnis.txt' #legt Pfad zu den Daten auf dem Desktop fest

if not os.path.exists('C:/Users/'+user+'/Desktop/ProgramRLE/'):
    os.makedirs('C:/Users/'+user+'/Desktop/ProgramRLE/')    
if not os.path.isfile('C:/Users/'+user+'/Desktop/ProgramRLE/Ergebnis.txt'):         #prüft ob verzeichnisse angelegt sind und erstellt sie wenn nötig
    open(solution_path, "w").write("")

letter = ["A","B"]#,"C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T"]    #Dies sind die entgültigen Farben die benutz werden
                                                                                                #geben auch ausschluss über die auftrittswahrscheinlichkeit

colordic= {"A":'cyan',
         "B":'black',
         "C":'gold',
         "D":'deep pink',
         "E":'lawn green',
         "F":'red2',
         "G":'grey29',
         "H":'dark green',
         "I":'deep sky blue',
         "J":'yellow2',
         "K":'brown4',
         "L":'dark slate gray',
         "M":'violet',
         "N":'navy',
         "O":'orange',
         "P":'purple',
         "Q":'dark violet',
         "R":'red',
         "S":'snow',
         "T":'chartreuse2'}             #Angaben der verschiedenen Farben 
columns = 12                            #spaltenanzahl
rows = 17                               #reihenanzahl
limit = 70                              #Grenze gegen überlastung des programms
equalizing = 0                          #"Radius" der Fläche in der Alle Felder angegleicht werden
auswerten = False                       #Buttons müssen beim auswerten nicht berechnet werden (Zeile 60)
count = 0                               #Counter des Namen zum Speichern der Daten fürs Auswerten
newcolor = 'B'                          #Farbe zum einstellen einer Farbe (setcolor)
tmplist = []                            #Wird benutzt um aus dem kompriermierten String die TempMatrix zu ertsellen
trigger = True                          #beendet den durchlauf der schleife (Wir wissen nicht warum sie weiter läuft und die Ergebisse verfälscht)
ColorMatrix = [[random.choice(letter) for x in range(columns)] for y in range(rows)]    #Initialisierung von Matrix (dort sind die Farben gespeichert)
########################################################################
def NewFile(randomize):                 #Erstellen einer neuen Matrix (Bild)
    if randomize:
        global ColorMatrix
        ColorMatrix = [[random.choice(letter) for x in range(columns)] for y in range(rows)]
    if not auswerten:                   #Wird nur ausgeführt, wenn auswerten auf False steht
        for row_index in range(rows)    :
             Grid.rowconfigure(root, row_index, weight=1)   
             for col_index in range(columns):
                 Grid.columnconfigure(root, col_index, weight=1)
                 tmpcolor = str(colordic[ColorMatrix[row_index][col_index]])
                 btn = Button(root, bg=tmpcolor, command=partial(changecolor, row_index, col_index))
                 btn.grid(row=row_index, column=col_index, sticky=N+S+E+W)

def OpenFile():                         #Öffnen eines bereits gespeicherten Textdokuments
    global ColorMatrix, columns, rows
    newfile_list = []
    img = filedialog.askopenfilename()
    data = open(img)
    for line in data:
        newfile_list.append(line.rstrip())
    data.close()
    newfile_list.reverse()
    columns = int(newfile_list.pop())
    rows = int(newfile_list.pop())
    ColorMatrix = [[newfile_list.pop() for x in range(columns)] for y in range(rows)]
    NewFile(False)
    

def SaveFile():                         #Speichern der Matrix als Textdokument
    img = filedialog.asksaveasfilename(filetypes = (("All files", "*.*")
                                                    ,("Text", "*.txt")))
    print("File wird unter " + img +" gespeichert")
    datei = open(img +".txt", "w")
    b= ""
    datei.write(str(columns)+"\n")
    datei.write(str(rows)+"\n")
    for row_index in range(rows):
        for col_index in range(columns):
            b = str(ColorMatrix[row_index][col_index]) + "\n" 
            datei.write(b)
    datei.close()
#####################################################################
def Compress(string):                   #Kompriemieren der Matrix 
    if not string:
    	return ""
    else:
        last_char = string[0]
        max_index = len(string)
        i = 1
        while i < max_index and last_char == string[i]:
                i += 1
        return last_char + str(i) + Compress(string[i:])
        
def Decompress(string):                 #Dekomprimieren der komprimierten Matrix
    if not string:
        return("")
    else:
        char = string[0]
        if len(string) > 4:
            if string[1].isdigit() and string[2].isdigit() and string[3].isdigit() and string[4].isdigit():
                quantity = string[1] + string[2] + string[3] + string[4]
                return char * int(quantity) + Decompress(string[5:])
        if len(string) > 3:
            if string[1].isdigit() and string[2].isdigit() and string[3].isdigit():
                quantity = string[1] + string[2] + string[3]
                return char * int(quantity) + Decompress(string[4:])
            
        if len(string) > 2:        
            if string[1].isdigit() and string[2].isdigit(): 
                quantity = string[1] + string[2]
                return char * int(quantity) + Decompress(string[3:])
        if len(string) > 1:                
            if string[1].isdigit():
                quantity = string[1]
                return char * int(quantity) + Decompress(string[2:])

def Window_decompress(string):          #Für die Anzeige der komprimierten Matrix
                                        #zu achten ist das der abgeschnittene string in tmplist eingefugt wird
                                        #wenn der string leer ist wird die Liste kopiert um nur die nötigen Werte zu benutzen
    global tmplist, trigger, txplist
    if not string:                                
        if trigger == True:             
            txplist = deepcopy(tmplist)
            trigger = False
        
    else:
        char = string[0]
        if len(string) > 4:
            if string[1].isdigit() and string[2].isdigit() and string[3].isdigit()and string[4].isdigit():
                quantity = string[1] + string[2] + string[3] + string[4]
                tmplist.insert(0, char+str(quantity))
                Window_decompress(string[5:])

        if len(string) > 3:
            if string[1].isdigit() and string[2].isdigit() and string[3].isdigit():
                quantity = string[1] + string[2] + string[3]
                tmplist.insert(0, char+str(quantity))
                Window_decompress(string[4:])

        if len(string) > 2:        
            if string[1].isdigit() and string[2].isdigit(): 
                quantity = string[1] + string[2]
                tmplist.insert(0, char+str(quantity))
                Window_decompress(string[3:])

        if len(string) > 1:
            if string[1].isdigit():
                quantity = string[1]
                tmplist.insert(0, char+str(quantity))
                Window_decompress(string[2:])
                                       
##########################################################################

def setcolor(row_index, col_index, letter):     #Setzt die Farbe eines Buttons
    if row_index >= 0 and col_index >= 0:
        ColorMatrix[row_index][col_index] = letter
        btn = Button(root, bg=str(colordic[ColorMatrix[row_index][col_index]]), command=partial(changecolor, row_index, col_index))
        btn.grid(row=row_index, column=col_index, sticky=N+S+E+W)

def changecolor(row_index, col_index):          #Änderung der Farbe eines Buttons (zufällig) wenn Equalizer == 0
        if equalizing == 0:
            ColorMatrix[row_index][col_index] = random.choice(letter)
            btn = Button(root, bg=str(colordic[ColorMatrix[row_index][col_index]]), command=partial(changecolor, row_index, col_index))
            btn.grid(row=row_index, column=col_index, sticky=N+S+E+W)
        if equalizing == 5:                     #Veränderung der Farbe der umliegenden Buttons mit Hilfe eines vordefinierten Radius (Equalizing = Radius) 
            setcolor(row_index, col_index, newcolor)
        else:
            tmpcolor = str(ColorMatrix[row_index][col_index])
            for i in range(2*equalizing+1):
                for j in range(2*equalizing+1):
                    try:
                        setcolor((row_index-equalizing)+i, (col_index-equalizing)+j, tmpcolor)                       
                    except:
                        pass
def Fenstergröße():                             #Anpssung der Fenstergröße inkl angegeben Limit
    def show_entry_fields():
        global columns, rows, limit
        columns = int(x1.get())
        rows = int(y1.get())
        if columns > limit:
            columns = limit
        if rows > limit:
            rows = limit
        NewFile(True)

    master = Tk()
    master.title("Größe")
    Label(master, text="Columns").grid(row=0)
    Label(master, text="Rows").grid(row=1)
    x1 = Entry(master)
    y1 = Entry(master)
    x1.grid(row=0, column=1)
    y1.grid(row=1, column=1)
    x1.insert(10,str(columns))
    y1.insert(10,str(rows))
    Button(master, text='Set', command=show_entry_fields).grid(row=3, column=1, sticky=W, pady=4)
    mainloop( )
 
def Equalizer():            #Änderung des Equalizers (Radius)
    global equalizing
    equalizing+= 1
    if equalizing >= 5:
        equalizing= 0    
    print("Equalizer ist "+ str(equalizing))

def Farbenwunsch():         #Manuelle Einstellung der Farbe (SetColor)
    global newcolor
    def show_entry_fields():
        global newcolor, equalizing
        newcolor = z1.get()
        equalizing = 5

    master = Tk()
    master.title("Farbenwunsch?")
    Label(master, text="Wunschfarbe").grid(row=0)
    z1 = Entry(master)
    z1.grid(row=0, column=1)
    z1.insert(10,str(newcolor))
    Button(master, text='Set', command=show_entry_fields).grid(row=3, column=1, sticky=W, pady=4)
    master.mainloop( )

############################################################################
def Anleitung():            #is logisch was hier is oder?
    manual = Tk()
    manual.title("Anleitung")

    Label(manual, justify=LEFT, text="""


 Hallo User! Hier erfährtst du wie du dieses Programm nutzen kannst.
 Zu sehen ist ein Feld, bestehend aus Buttons verschiedener Farben. 
 Die Farbe der Buttons kannst du durch anklicken verändern.
 Zudem findest du unter dem Feld Edit die Möglichkeit dir eine Farbe auszusuchen.
 Hier ist die Liste der möglichen Farben:
         "A":'cyan'             "B":'black'
         "C":'gold'             "D":'deep pink'
         "E":'lawn green'       "F":'red2'
         "G":'grey29'           "H":'dark green'
         "I":'deep sky blue'    "J":'yellow2'
         "K":'brown4'           "L":'dark slate gray'
         "M":'violet'           "N":'navy'
         "O":'orange'           "P":'purple'
         "Q":'dark violet'      "R":'red'
         "S":'snow'             "T":'chartreuse2'
 Bitte nutze hier nur die Buchstaben, die bei den gewünschten Farben stehen.
 Mit dem Equalizer kannst du die Farbe mehrerer Buttons gleichzeitig angleichen. 
 Dieser hat mehrere Größeneinstellungen von 1 - 4.
 Desweiteren kannst du im Feld Edit auch auswählen, wie groß du dein Fenster haben möchtest.

 Unter dem Feld "File" kannst du deine Matrix speichern, öffnen oder eine Neue erstellen lassen.
 
 Unter RLE findest du Die Möglichkeit dein Bild zu kompriermieren (RLE compress), dir verschiedene Kompressiongüten
 unter verschiednen Startparametern berechnen zu lassen und diese anzugucken und
 dir davon danach die Mittelwerte und Standartabweichungen anzeigen zu lassen. 
 
""").grid(row=0)
    manual.mainloop( )




def About():
    print("Pythonscript für Datenkompression 2018\nPrüfer: Dr.Vuong\nThema: RLE \n\nAuthor: Stefan Chalupka  (6037666)\nAuthor: Marcel Brück "\
          "    (6192721) \nAuthor: Felix  Landsiedel(5285778)")

def Auswertung():           #wertet die Matrizen mit 50 verschiedenen Parametern 100 mal aus
    global auswerten, letter
    letter = ["A","A","A","A","A","A","A","A","A","A","A","A","A","A","A","A","A","A","A","A","A","A","A","A","A","A","A","A","A","A","A","A",\
              "A","A","A","A","A","A","A","A","A","A","A","A","A","A","A","A","A","A",\
              "B","B","B","B","B","B","B","B","B","B","B","B","B","B","B","B","B","B","B","B","B","B","B","B","B","B","B","B","B","B","B","B",\
              "B","B","B","B","B","B","B","B","B","B","B","B","B","B","B","B","B","B"] #50*A, 50*B

    auswerten = True
    for j in range(50):
        print("A:" + str(letter.count("A")))
        print("B:" + str(letter.count("B")))
        letter.pop()
        letter.insert(0, "A")
        for i in range(100):
            NewFile(True)
            Tester()
            
        data = open(solution_path)      #schreibt die Ergebnisse in den solution_path (siehe Desktop)
        string =""
        for line in data:
            string = string + line
        data.close()
        open(solution_path, "w").write(string+"\n")

    
    auswerten = False

def MW_SA():        #Berechnung des Mittelwerts und der Standartabweichung von den Ergebnissen der Auswertung
    datalist=open(solution_path,"r")
    for line in datalist:
        liste=(line.rstrip()).split(", ")
        k, j, l, m,  = 0, 0, 0, 0
        print(liste)
        for i in liste:
            j = j + 1
            k = float(k) + float(str(i[:-1]))
        mittelwert = k / len(liste)
        print("Mittelwert:        " + str(mittelwert))
        for i in liste:
            m = m + 1
            Value = (float(i[:-1]) - mittelwert)**2
            l = l + Value
            Result = math.sqrt(l/(len(liste)-1))
        print("Standartabweichung MW: " + str(Result/(math.sqrt(len(liste)))) + "\n")
        


def Tester():       #wertet das aktuelle Bild/Matrix aus und gibt die Effizents der Komprimierung an
    global daten, count
    daten= ""
    user = getpass.getuser()
    for row_index in range(rows):
        for col_index in range(columns):
            daten = daten +str(ColorMatrix[row_index][col_index])
    timestamp = time.strftime("%H_%M_%S")
    komprimiert = Compress(daten)
    angabe= "%.2f" % (((1-len(komprimiert)/len(daten))*100))
    if (len(daten) < len(komprimiert)):
        text = ('Daten:\n'+daten+'\nLänge:\n'+str(len(daten))+'\n\nKomprimiert:\n'+komprimiert+\
                '\nLänge:\n'+str(len(komprimiert))+'\n\n\nKomprimierte String ist nun '+str(float(angabe)*-1)+'% größer')
    else:
        text = ('Daten:\n'+daten+'\nLänge:\n'+str(len(daten))+'\n\nKomprimiert:\n'+komprimiert+\
                '\nLänge:\n'+str(len(komprimiert))+'\n\n\nKomprimierte String ist nun '+angabe+'% kleiner')
    print(text)
    
    open('C:/Users/'+user+'/Desktop/ProgramRLE/Datei'+ str(count)+ '__' + str(timestamp) +'.txt', "w").write(text)
    count = count + 1
    string = ""
    data = open(solution_path)
    for line in data:
        string = string + line
    data.close()
    open(solution_path, "w").write(string+angabe+", ")



############################################################################
def Mainwindow():           #erstellen des Hauptfensters mit tkinter
    global root, ColorMatrix
    root = Tk()
    root.title("Datenkompression - Run length encoding (RLE)")
    #root.geometry(str(20*columns)+"x"+str(20*rows))
    root.geometry("640x640")
    #root.resizable(0,0)
    menu = Menu(root)
    root.config(menu=menu)
    filemenu = Menu(menu, tearoff=0)
    menu.add_cascade(label="File", menu=filemenu)
    filemenu.add_command(label="New", command=partial(NewFile, True))
    filemenu.add_command(label="Open", command=OpenFile)
    filemenu.add_command(label="Save", command=SaveFile)
    filemenu.add_command(label="Exit", command=root.quit)
    

    editmenu = Menu(menu, tearoff=0)
    menu.add_cascade(label="Edit", menu=editmenu)
    editmenu.add_command(label="Fenstergröße X*Y", command=Fenstergröße)
    editmenu.add_command(label="Equalize", command=Equalizer)
    editmenu.add_command(label="Farbenwunsch", command=Farbenwunsch)

    rlemenu = Menu(menu, tearoff=0)
    menu.add_cascade(label="RLE", menu=rlemenu)
    rlemenu.add_command(label="RLE compress", command=RLEwindow)
    rlemenu.add_command(label="Auswertung", command=Auswertung)
    rlemenu.add_command(label="Mittelwert & SA", command=MW_SA)
    rlemenu.add_command(label="Tester", command=Tester)
    


    helpmenu = Menu(menu, tearoff=0)
    menu.add_cascade(label="Help", menu=helpmenu)
    helpmenu.add_command(label="Anleitung", command=Anleitung)
    helpmenu.add_command(label="About", command=About)

    for row_index in range(rows):
        Grid.rowconfigure(root, row_index, weight=1)
        for col_index in range(columns):
            Grid.columnconfigure(root, col_index, weight=1)
            tmpcolor = str(colordic[ColorMatrix[row_index][col_index]])
            btn = Button(root, bg=tmpcolor, command=partial(changecolor, row_index, col_index))
            btn.grid(row=row_index, column=col_index, sticky=N+S+E+W)           #Erstellung der Pixelbuttons mit Hilfe der ColorMatrix
    root.mainloop()

def RLEwindow():            #erstellen des Fensters für das komprimierte Bild (komprimierte Matrix)
    daten= ""
    for row_index in range(rows):
        for col_index in range(columns):
            daten = daten +str(ColorMatrix[row_index][col_index])       #Matrix auslesen und in string schreiben
                                                                        
    komprimiert = Compress(daten)                                       #komprimiert diesen String
    Window_decompress(komprimiert)                                      #ließt die Daten aus dem komprimierten String und schreibt sie in die Liste tmplist => txplist
    columns2= math.ceil(math.sqrt(len(txplist)))                        
    rows2= math.ceil(math.sqrt(len(txplist)))
    CompMatrix = [["" for x in range(columns2)] for y in range(rows2)]
    for i in range(len(txplist)):    
        CompMatrix[i // columns2][i % columns2] = txplist.pop()
    root = Tk()
    root.title("Datenkompression - Run length encoding (RLE)")
    root.geometry(str(20*columns2)+"x"+str(20*rows2))
    root.resizable(0,0)
    menu = Menu(root)
    root.config(menu=menu)
    editmenu = Menu(menu, tearoff=0)
    editmenu.add_command(label="RLE decompress", command=None)
    helpmenu = Menu(menu, tearoff=0)
    menu.add_cascade(label="Tester", menu=helpmenu)
    helpmenu.add_command(label="Start", command=Tester)
    
    for row_index in range(rows2):
        Grid.rowconfigure(root, row_index, weight=1)
        for col_index in range(columns2):
            Grid.columnconfigure(root, col_index, weight=1)
            try:
                field = str(CompMatrix[row_index][col_index])
                btn = Button(root, bg=str(colordic[field[0]]), text=str(field[1:]), command = None)
                btn.grid(row=row_index, column=col_index, sticky=N+S+E+W)
            except:
                pass
    root.mainloop()

Mainwindow()
