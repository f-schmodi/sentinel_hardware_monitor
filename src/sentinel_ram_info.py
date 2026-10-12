# ---------------------------------
# Sentinel Hardware Monitor / Projektarbeit zur Zertifizierung / Software Developer (IHK) 2024-2025
# ---------------------------------
# Florian Schimbold
#----------------------------------
# Modul Arbeitsspeicher
#----------------------------------

import tkinter as tk
import psutil
import wmi
# Wandelt Byte angaben in passende Einheit um
def einheit_byte(size):
    for einheit_daten_groesse in ['Bytes', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024 or einheit_daten_groesse == 'TB':
            return f"{size:.2f} {einheit_daten_groesse}"
        size /= 1024

def ausgabe_ram_herst_kapaz_serienn():
    schnittstelle_wmi = wmi.WMI()
    ram_info = []
    for ram_index, parameter in enumerate(schnittstelle_wmi.Win32_PhysicalMemory(), start=1):
        hersteller = parameter.Manufacturer if parameter.Manufacturer else "Unbekannt"
        kapazitaet   = int(parameter.Capacity) if parameter.Capacity else 0
        seriennummer= parameter.SerialNumber if parameter.SerialNumber else "Unbekannt"
        ram_info.append(
            f"RAM{ram_index}:\n"
            f"Hersteller    : {hersteller}\n"
            f"Kapazität     : {kapazitaet / (1024 ** 3):.2f} GB\n"
            f"Seriennummer  : {seriennummer}")

    return "\n\n".join(ram_info) or "Keine RAM-Herstellerinfo gefunden."

class ModulArbeitsspeicher(tk.Frame):
    def __init__(self, parent, bg="gray13", fg="white", **kwargs):
        super().__init__(parent, bg=bg, **kwargs)
        self.ram_label = tk.Label(
            self,
            font=("Consolas", 18),
            justify="left",
            anchor="nw",
            fg=fg,
            bg=bg)

        self.ram_label.pack(fill="both", expand=True, padx=20, pady=20)
        self._ram_update()

    def _ram_update(self):
        speicher_virtuell = psutil.virtual_memory()
        speicher_auslagerung = psutil.swap_memory()
        info_allgemein = ausgabe_ram_herst_kapaz_serienn()
        text = (
            "=== RAM Hersteller Infos ===\n"
            f"\n{info_allgemein}\n\n"
            "\n=== Hauptspeicher (RAM) ===\n"
            f"\nGesamt            : {einheit_byte(speicher_virtuell.total)}\n"
            f"Verfügbar         : {einheit_byte(speicher_virtuell.available)}\n"
            f"Benutzt           : {einheit_byte(speicher_virtuell.used)}\n"
            f"Frei              : {einheit_byte(speicher_virtuell.free)}\n" 
            f"Prozent genutzt   : {speicher_virtuell.percent}%\n\n"
            "\n=== Auslagerungsspeicher (Swap) ===\n"
            f"\nGesamt            : {einheit_byte(speicher_auslagerung.total)}\n"
            f"Benutzt           : {einheit_byte(speicher_auslagerung.used)}\n"
            f"Frei              : {einheit_byte(speicher_auslagerung.free)}\n"
            f"Prozent genutzt   : {speicher_auslagerung.percent}%\n"
            f"RAM in Auslagerung : {speicher_auslagerung.sout}\n" # Aus RAM in Auslagerungsspeicher
            f"Auslagerung in RAM : {speicher_auslagerung.sin}") # Von Auslagerungsspeicher in RAM

        self.ram_label.config(text=text)
        # Aktualisierung
        self.after(2000, self._ram_update)

if __name__ == "__main__":
    ram_fenster = tk.Tk()
    ram_fenster.title("Arbeitsspeicher (RAM)")
    ram_fenster.geometry("800x600")
    ram_frame = ModulArbeitsspeicher(ram_fenster)
    ram_frame.pack(expand=True, fill="both")
    ram_fenster.mainloop()