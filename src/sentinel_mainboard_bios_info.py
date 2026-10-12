# ---------------------------------
# Sentinel Hardware Monitor / Projektarbeit zur Zertifizierung / Software Developer (IHK) 2024-2025
# ---------------------------------
# Florian Schimbold
#----------------------------------
# Modul Mainboard/BIOS
#----------------------------------

import tkinter as tk
import wmi           # ----> Windows Management Instrumentaion

class ModulMainboardBios(tk.Frame):
    def __init__(self, parent,bg="gray13", fg="white", *args, **kwargs):
        super().__init__(parent,bg=bg, *args, **kwargs)
        # Informationen Mainboard/BIOS
        mainboard_bios_info = self._ausgabe_mainboard_bios_info()
        # Anzeige Information
        self.label = tk.Label(
            self,
            text=mainboard_bios_info,
            bg=bg,
            fg=fg,
            font=("Consolas", 18),
            justify=tk.LEFT,
            anchor="nw",
            wraplength=1000)

        self.label.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)
    # WMI Anbindung
    def _ausgabe_mainboard_bios_info(self):
        schnittstelle_wmi = wmi.WMI()
        zeilen = ["=== Mainboard ==="," "]

        for mainboard in schnittstelle_wmi.Win32_BaseBoard():
            zeilen += [
                f"Hersteller    : {mainboard.Manufacturer}",
                f"Produkt       : {mainboard.Product}",
                f"Seriennummer  : {mainboard.SerialNumber}",
                f"Version       : {mainboard.Version}"
            ]
        zeilen.append("\n\n=== BIOS ===",)
        for bios in schnittstelle_wmi.Win32_BIOS():
            zeilen += [
                f"\nBIOS Version  : {bios.SMBIOSBIOSVersion}",
                f"Hersteller    : {bios.Manufacturer}",
                f"Release Datum : {bios.ReleaseDate}"
            ]
        return "\n".join(zeilen)

if __name__ == "__main__":
    mainboard_bios_fenster = tk.Tk()
    mainboard_bios_fenster.title("Mainboard/BIOS")
    mainboard_bios_fenster.geometry("800x600")
    mainboard_bios_frame = ModulMainboardBios(mainboard_bios_fenster)
    mainboard_bios_frame.pack(expand=True, fill="both")
    mainboard_bios_fenster.mainloop()