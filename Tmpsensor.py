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
 
 

    
    
 
def main_loop():
    while True:
        messdaten = aktuelleTemperatur()
        print ("Aktuelle Temperatur : ", messdaten, "°C")
        time.sleep(1)

if __name__=="__main__":
    main_loop()
        
