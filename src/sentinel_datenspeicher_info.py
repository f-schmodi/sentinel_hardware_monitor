# ---------------------------------
# Sentinel Hardware Monitor / Projektarbeit zur Zertifizierung / Software Developer (IHK) 2024-2025
# ---------------------------------
# Florian Schimbold
#----------------------------------
# Modul Datenspeicher
#----------------------------------

import os
import time
import tempfile
import tkinter as tk
import wmi

class ModulDatenspeicher(tk.Frame):
    def __init__(self, parent, bg="gray13", fg="white", **kwargs):
        super().__init__(parent, bg=bg, **kwargs)
        self.datenspeicher_text = tk.StringVar()
        self.datenspeicher_info_label = tk.Label(
            self,
            textvariable=self.datenspeicher_text,
            anchor='nw',
            justify=tk.LEFT,
            bg=bg,
            fg=fg,
            font=("Consolas", 18))

        self.datenspeicher_info_label.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        # Test Button
        self.test_button = tk.Button(
            self,
            text="Geschwindigkeit testen",
            command=self.geschwindigkeitstest_datenspeicher,
            bg=bg,
            fg=fg,
            font=("Consolas", 18),
            activebackground="gray43",
            relief=tk.FLAT)

        self.test_button.pack(pady=(0, 10))
        # SSD Info bei Start
        self.ausgabe_datenspeicher_info()

    def ausgabe_datenspeicher_info(self):
        zeilen = []
        try:
            schnittstelle_wmi = wmi.WMI()
            for disk in schnittstelle_wmi.Win32_DiskDrive():
                modell        = disk.Model or "Unbekannt"
                hersteller    = disk.Manufacturer or "Unbekannt"
                seriennummer  = disk.SerialNumber.strip() if disk.SerialNumber else "Unbekannt"
                firmware      = disk.FirmwareRevision or "Unbekannt"
                groesse_gb    = int(disk.Size) / (1024 ** 3) if disk.Size else 0
                interface     = disk.InterfaceType or "Unbekannt"

                zeilen.append(f" === SSD Infos ===\n")
                zeilen.append(f"Gerät           : {disk.DeviceID}")
                zeilen.append(f"Modell          : {modell}")
                zeilen.append(f"Seriennummer    : {seriennummer}")
                zeilen.append(f"Firmware        : {firmware}")
                zeilen.append(f"Schnittstelle   : {interface}")
                zeilen.append(f"Größe           : {groesse_gb:.2f} GB")


        except Exception as fehler:
            zeilen.append(f"Fehler beim Auslesen: {fehler}")

        self.datenspeicher_text.set("\n".join(zeilen))

    def geschwindigkeitstest_datenspeicher(self):                           #Test wurde mit Hilfe von KI generiert!!!
        self.ausgabe_datenspeicher_info()
        test_liste = self.datenspeicher_text.get().splitlines()

        test_liste.append("")
        test_liste.append("Geschwindigkeitstest:\n")

        # Schreibtest
        test_groesse_mb = 100 * 1024 ** 2
        parameter_byte_string = b'0' * 1024 ** 2
        temp_verzeichnis = os.path.join(tempfile.gettempdir(), "speedtest.tmp")

        start_testzeit = time.perf_counter()
        with open(temp_verzeichnis, 'wb') as datei:
            for iteration in range(100):
                datei.write(parameter_byte_string)

        ende_testzeit = time.perf_counter()
        schreibe_megabyte_pro_sekunde = test_groesse_mb / (ende_testzeit - start_testzeit) / 1024 ** 2
        test_liste.append(f"Schreibgeschwindigkeit  : {schreibe_megabyte_pro_sekunde:.2f} MB/s")

        # Lesetest
        start_testzeit = time.perf_counter()
        with open(temp_verzeichnis, 'rb') as datei: # rb damit Datei binär geöffnet wird, nicht als Text
            while datei.read(1024**2):
                pass
        ende_testzeit = time.perf_counter()
        lese_mb_pro_sekunde = test_groesse_mb / (ende_testzeit - start_testzeit) / 1024 ** 2
        test_liste.append(f"Lesegeschwindigkeit     : {lese_mb_pro_sekunde:.2f} MB/s")

        # Löschung der geschriebenen Daten
        try:
            os.remove(temp_verzeichnis)
        except OSError:
            pass

        self.datenspeicher_text.set("\n".join(test_liste))

if __name__ == "__main__":
    datenspeicher_fenster = tk.Tk()
    datenspeicher_fenster.title("Datenspeicher (SSD)")
    datenspeicher_fenster.geometry("800x600")
    datenspeicher_frame = ModulDatenspeicher(datenspeicher_fenster, borderwidth=1, relief=tk.FLAT)
    datenspeicher_frame.pack(fill="both", expand=True)
    datenspeicher_fenster.mainloop()
