import RPi.GPIO as GPIO
import time
import tkinter as tk
from tkinter import Label, Entry, Button

# GPIO-Pin für PWM
en = 25

# GPIO-Pins für enable (Beispiel: GPIO-Pin 17 und GPIO-Pin 22)
enable_pin1 = 23
enable_pin2 = 24

# Setup für GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(enable_pin1,GPIO.OUT)
GPIO.setup(enable_pin2,GPIO.OUT)
GPIO.setup(en,GPIO.OUT)
GPIO.output(enable_pin1,GPIO.LOW)
GPIO.output(enable_pin2,GPIO.LOW)
p=GPIO.PWM(en,1000)
p.start(50)

# Verzeichnis, in dem die Temperatursensoren erkannt werden
sensor_directory = '/sys/bus/w1/devices/'

# ID des DS18B20-Temperatursensors (ersetzen Sie dies durch Ihre Sensor-ID)
sensor_id = '28-3cd1f64863d3'

# Funktion zum Lesen der Temperatur vom DS18B20-Sensor
def read_temperature(sensor_id):
    try:
        with open(sensor_directory + sensor_id + '/w1_slave', 'r') as file:
            lines = file.readlines()
            temperature_line = lines[1]
            temperature_data = temperature_line.split(' ')[9]
            temperature = float(temperature_data[2:]) / 1000.0
            return temperature
    except IOError:
        print("Fehler beim Lesen der Temperatur.")
        return None

# Funktion für den Aktualisieren-Button
def update_target_temperature():
    try:
        target_temperature = float(target_temp_entry.get())
    except ValueError:
        target_temperature = 20.0  # Standardwert, falls die Eingabe ungültig ist

    target_temp_label.config(text="Soll-Temperatur: {:.2f} °C".format(target_temperature))
    #control_heater(en, enable_pin1, enable_pin2, 50)

# Funktion zum Steuern des Heizelements mit PWM und enable
def control_heater(pwm_pin, enable_pin1, enable_pin2, duty_cycle):
    try:
        temp_aktuell= read_temperature(sensor_id)
        target_temperature = float(target_temp_entry.get())
        print(temp_aktuell)
        print(target_temperature)
    except ValueError:
        target_temperature = 20.0  # Standardwert, falls die Eingabe ungültig ist
        
    target_temp_label.config(text="Soll-Temperatur: {:.2f} °C".format(target_temperature))

    if target_temperature - temp_aktuell > 20:
        GPIO.output(enable_pin1, GPIO.HIGH)  # enable1 einschalten
        GPIO.output(enable_pin2, GPIO.LOW)  # enable2 ausschalten
        p.ChangeDutyCycle(100)
    elif target_temperature - temp_aktuell > 10:
        GPIO.output(enable_pin1, GPIO.HIGH)  # enable1 einschalten
        GPIO.output(enable_pin2, GPIO.LOW)  # enable2 ausschalten
        p.ChangeDutyCycle(75)

    elif target_temperature - temp_aktuell > 5:     
        GPIO.output(enable_pin1, GPIO.HIGH)  # enable1 ausschalten
        GPIO.output(enable_pin2, GPIO.LOW)  # enable2 ausschalten
        p.ChangeDutyCycle(50)
        
    elif target_temperature > temp_aktuell:     
        GPIO.output(enable_pin1, GPIO.HIGH)  # enable1 ausschalten
        GPIO.output(enable_pin2, GPIO.LOW)  # enable2 ausschalten
        p.ChangeDutyCycle(30)

    else:
        GPIO.output(enable_pin1, GPIO.LOW)  # enable1 ausschalten
        GPIO.output(enable_pin2, GPIO.LOW)  # enable2 ausschalten
        p.ChangeDutyCycle(0)
    
    
                    
# Funktion für die GUI-Aktualisierung
def update_gui():
    temperature = read_temperature(sensor_id)

    if temperature is not None:
        current_temp_label.config(text="Aktuelle Temperatur: {:.2f} °C".format(temperature))

        # Überprüfe ob heizer zugeschlten werden muss
        control_heater(en, enable_pin1, enable_pin2, 50)
        
    root.after(1000, update_gui)  # Aktualisiert die GUI alle 1000 Millisekunden (1 Sekunde)




# GUI erstellen
root = tk.Tk()
root.title("Temperaturanzeige")

# Label für aktuelle Temperatur
current_temp_label = Label(root, text="Aktuelle Temperatur: -", font=("Helvetica", 12))
current_temp_label.pack(pady=10)

# Eingabefeld für die Soll-Temperatur
target_temp_label = Label(root, text="Soll-Temperatur: -", font=("Helvetica", 12))
target_temp_label.pack(pady=10)

target_temp_entry = Entry(root, font=("Helvetica", 12))
target_temp_entry.pack(pady=10)


# Aktualisieren-Button
update_button = Button(root, text="Aktualisieren", command=update_target_temperature)
update_button.pack(pady=10)

# Starten Sie die GUI-Aktualisierung
update_gui()

# Starten Sie die Tkinter-Schleife
root.mainloop()

# Aufräumen nachdem die GUI geschlossen wurde
GPIO.cleanup()
