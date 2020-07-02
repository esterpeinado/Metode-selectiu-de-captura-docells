from tkinter import *
from tkinter import messagebox

# Definició de la pantalla principal
root = Tk()
root.title("Captura selectiva d'ocells")
root.resizable(0,0)
root.iconbitmap("logo-seo.ico")

# Definició del frame on es programaran els objectes
miFrame = Frame(root, width="650", height="350")
miFrame.pack(fill="both", expand="1")

varOpcion = IntVar()
ocell = ""

def avis():
    root.withdraw()     # Aquesta funció oculta la finestra principal "root"
    # Es mostra el missatge d'avís en una finestra emergent
    messagebox.showwarning("Captura realitzada", "S'ha capturat un exemplar de {}".format(ocell))

# Es guarda el nom de l'espècie seleccionada a la variable "ocell"
def seleccio():
    global ocell
    
    if varOpcion.get() == 1:
        ocell = "Cadernera"
    
    elif varOpcion.get() == 2:
        ocell = "Pinsa borroner"
        
    elif varOpcion.get() == 3:
        ocell = "Passerell comu"
    
    else:
        ocell = "Pardal comu"

    root.destroy()  # Es tanca la GUI


# Programació dels elements que es mostren al frame i inici del mainloop
#--------- Capçalera ---------
lblInici = Label(miFrame, text="Seleccioni l'espècie a capturar:", font=("Comic Sans MS", 18))
lblInici.grid(row=0, column=0, padx=20, pady=10, columnspan=4, sticky="w")

#--------- Cadernera ---------
# Imatge
imgCadernera = PhotoImage(file="cadernera.png")
lblimgCadernera= Label(miFrame, image=imgCadernera)
lblimgCadernera.grid(row=1, column=1, padx=20, pady=10)

#Botó de selecció
buttonCadernera = Radiobutton(miFrame, text="Cadernera", font=("Comic Sans MS", 14),
    variable=varOpcion, value=1, command=seleccion)
buttonCadernera.grid(row=1, column=0, sticky="w", padx=20, pady=10)

#--------- Pinsà Borroner ---------
# Imatge
imgPinsa = PhotoImage(file="pinsa.png")
lblimgPinsa= Label(miFrame, image=imgPinsa)
lblimgPinsa.grid(row=2, column=1, padx=20, pady=10)

#Botó de selecció
buttonPinsa = Radiobutton(miFrame, text="Pinsà Borroner", font=("Comic Sans MS", 14),
    variable=varOpcion, value=2, command=seleccion)
buttonPinsa.grid(row=2, column=0, sticky="w", padx=20, pady=10)

#--------- Passerell Comú ---------
# Imatge
imgPasserell = PhotoImage(file="passerell.png")
lblimgPasserell= Label(miFrame, image=imgPasserell)
lblimgPasserell.grid(row=1, column=3, padx=20, pady=10)

#Botó de selecció
buttonPasserell = Radiobutton(miFrame, text="Passerell Comú", font=("Comic Sans MS", 14),
    variable=varOpcion, value=3, command=seleccion)
buttonPasserell.grid(row=1, column=2, sticky="w", padx=20, pady=10)

#--------- Pardal Comú ---------
# Imatge
imgPardal = PhotoImage(file="pardal.png")
lblimgPardal= Label(miFrame, image=imgPardal)
lblimgPardal.grid(row=2, column=3, padx=20, pady=10)

#Botó de selecció
buttonPardal = Radiobutton(miFrame, text="Pardal Comú", font=("Comic Sans MS", 14),
    variable=varOpcion, value=4, command=seleccion)
buttonPardal.grid(row=2, column=2, sticky="w", padx=20, pady=10)

# Botó per comprobar el funcionament de la funció "avis"
buttonAvis = Radiobutton(root, text="avis", font=("Comic Sans MS", 14),
    variable=varOpcion, value=5, command=avis)
buttonAvis.pack()

root.mainloop()