import tkinter as tk
import os, sys, time

def aktuelleTemperatur():
    #GPIO Pin4 = Pin 7 
    # 1-wire Slave Datei lesen
    file = open('/sys/bus/w1/devices/28-3cd1f64863d3/w1_slave')
    filecontent = file.read()
    file.close()
 
    # Temperaturwerte auslesen und konvertieren
    stringvalue = filecontent.split("\n")[1].split(" ")[9]
    temperature = float(stringvalue[2:]) / 1000
 
    # Temperatur ausgeben
    rueckgabewert = '%6.2f' % temperature 
    return(rueckgabewert)

# Funktion für die GUI-Aktualisierung
def update_gui():
    temperature = aktuelleTemperatur()

    if temperature is not None:
        #current_temp_label.config(text="Aktuelle Temperatur: {:.2f} °C".format(temperature))
        
        # Füge die Temperatur in Ausgabefeld 3 ein
        #output_field3.config(text="Temperatur in Feld 3: {:.2f} °C".format(temperature))
        ausgabefeld3.insert(text="Temperatur in Feld 3: {:.2f} °C".format(temperature)) 
        
    root.after(1000, update_gui)  # Aktualisiert die GUI alle 1000 Millisekunden (1 Sekunde)

def validate_input(value, widget_name):
    try:
        if value.strip() == "":
            return True  # Erlaube leere Eingabe
        float(value)
        return True
    except ValueError:
        print("Ungültige Eingabe in {widget_name}")
        return False
    
def senden(eingabe_var, ausgabe_var, sensor_text, block_num):
    if eingabe_var.get().strip() != "":
        #ausgabe_var.set(eingabe_var.get())
        sensor_text.insert(tk.END,"Block{} - Sensorwert empfangen:{}\n".format(block_num, eingabe_var.get()))
        # Speichern der eingegebenen Werte in der Konfigurationsdatei
        save_config(block_num, eingabe_var.get())
    else:
        print("Eingabefeld ist leer!")

def save_config(block_num, value):
    with open("config.txt", "a") as file:
        file.write("Block" + str(block_num) + "=" + str(value)+ "\n")

def load_config():
    config = {}
    try:
        with open("config.txt", "r") as file:
            for line in file:
                key, value = line.strip().split("=")
                config[key] = value
    except FileNotFoundError:
        pass
    return config
        
# Hauptfenster erstellen
root = tk.Tk()
root.title("GUI mit Tkinter")

# Funktion für das Senden erstellen
eingabe_var1 = tk.StringVar()
ausgabe_var1 = tk.StringVar()

eingabe_var2 = tk.StringVar()
ausgabe_var2 = tk.StringVar()

eingabe_var3 = tk.StringVar()
ausgabe_var3 = tk.StringVar()

# Konfiguration laden
config = load_config()
eingabe_var1.set(config.get("Block1", ""))
eingabe_var2.set(config.get("Block2", ""))
eingabe_var3.set(config.get("Block3", ""))

# Block 1
block1_frame = tk.Frame(root)
block1_frame.pack(padx=10, pady=10)

tk.Label(block1_frame, text="Eingabe Eingangsdruck:").grid(row=0, column=0)
eingabefeld1 = tk.Entry(block1_frame, textvariable=eingabe_var1)
eingabefeld1.grid(row=0, column=1)

tk.Label(block1_frame, text="Ausgabe Eingangsdruck:").grid(row=1, column=0)
ausgabefeld1 = tk.Entry(block1_frame, textvariable=ausgabe_var1, state='readonly')
ausgabefeld1.grid(row=1, column=1)

senden_button1 = tk.Button(block1_frame, text="Senden", command=lambda: senden(eingabe_var1, ausgabe_var1, sensor_text,1))
senden_button1.grid(row=2, column=0, columnspan=2, pady=5)

# Block 2
block2_frame = tk.Frame(root)
block2_frame.pack(padx=10, pady=10)

tk.Label(block2_frame, text="Eingabe Ausgangsdruck:").grid(row=0, column=0)
eingabefeld2 = tk.Entry(block2_frame, textvariable=eingabe_var2)
eingabefeld2.grid(row=0, column=1)

tk.Label(block2_frame, text="Ausgabe Ausgangsdruck:").grid(row=1, column=0)
ausgabefeld2 = tk.Entry(block2_frame, textvariable=ausgabe_var2, state='readonly')
ausgabefeld2.grid(row=1, column=1)

senden_button2 = tk.Button(block2_frame, text="Senden", command=lambda: senden(eingabe_var2, ausgabe_var2, sensor_text,2))
senden_button2.grid(row=2, column=0, columnspan=2, pady=5)

# Block 3
block3_frame = tk.Frame(root)
block3_frame.pack(padx=10, pady=10)

tk.Label(block3_frame, text="Eingabe Temperatur:").grid(row=0, column=0)
eingabefeld3 = tk.Entry(block3_frame, textvariable=eingabe_var3)
eingabefeld3.grid(row=0, column=1)

tk.Label(block3_frame, text="Ausgabe Temperatur:").grid(row=1, column=0)
ausgabefeld3 = tk.Entry(block3_frame, textvariable=ausgabe_var3, state='readonly')
ausgabefeld3.grid(row=1, column=1)

senden_button3 = tk.Button(block3_frame, text="Senden", command=lambda: senden(eingabe_var3, ausgabe_var3, sensor_text,3))
senden_button3.grid(row=2, column=0, columnspan=2, pady=5)

# Block 4 (Sensorwert-Textbox)
sensor_text = tk.Text(root, height=10, width=30)
sensor_text.pack(padx=10, pady=10)

# Starten Sie die GUI-Aktualisierung
update_gui()

# Starte die Tkinter-Schleife
root.mainloop()

# Aufräumen nachdem die GUI geschlossen wurde
GPIO.cleanup()
