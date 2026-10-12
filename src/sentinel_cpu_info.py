# ---------------------------------
# Sentinel Hardware Monitor / Projektarbeit zur Zertifizierung / Software Developer (IHK) 2024-2025
# ---------------------------------
# Florian Schimbold
#----------------------------------
# Modul CPU
#----------------------------------

import tkinter as tk
import psutil
import platform
import wmi
from tkinter.scrolledtext import ScrolledText

class ModulCpu(tk.Frame):
    def __init__(self, parent, bg="gray13", fg="white", refresh_interval=2000, **kwargs):
        super().__init__(parent, **kwargs)
        self.aktualisierungsrate = refresh_interval
        self.cpu_info_text = ScrolledText(
            self,
            bg=bg,
            fg=fg,
            font=("Consolas", 18),
            wrap="none"
        )
        self.cpu_info_text.pack(fill="both", expand=True)
        self.cpu_info_text.config(state="disabled")

        # WMI Anbindung
        self.wmi = wmi.WMI(namespace="root\\CIMV2")
        self.update_info()

    def ausgabe_cpu_info(self):
        prozessor = self.wmi.Win32_Processor()[0]
        info = {
            "Hersteller": prozessor.Manufacturer,
            "Modell": prozessor.Name,
            "Kerne (physisch)": prozessor.NumberOfCores,
            "Kerne (logisch)": prozessor.NumberOfLogicalProcessors,
            "Max-Takt (MHz)": prozessor.MaxClockSpeed,
            "Architektur": platform.machine(),
            "OS-Version": platform.version(),
        }
        # Aktuelle Frequenz
        try:
            cpu_taktfrequenz = psutil.cpu_freq()
            info["Takt aktuell (MHz)"] = f"{cpu_taktfrequenz.current:.2f}"
        except Exception:
            pass
        return info

    def update_info(self):
        # Statische und dynamische Daten
        info_statisch = self.ausgabe_cpu_info()
        cpu_auslastung_prozent = psutil.cpu_percent(interval=None, percpu=True)
        cpu_gesamtauslastung = sum(cpu_auslastung_prozent) / len(cpu_auslastung_prozent) if cpu_auslastung_prozent else 0

        zeilen = ["=== CPU Infos ===\n"]
        for bezeichner, inhalt in info_statisch.items():
            zeilen.append(f"{bezeichner}: {inhalt}")
        zeilen.append("")
        zeilen.append(f"Gesamt-Auslastung : {cpu_gesamtauslastung:.1f} %\n")

        for cpu_kern_index, usage in enumerate(cpu_auslastung_prozent):
            zeilen.append(f"Kern {cpu_kern_index + 1} Auslastung : {usage:.1f} %")
        content = "\n".join(zeilen)

        self.cpu_info_text.config(state="normal")
        self.cpu_info_text.delete("1.0", "end")
        self.cpu_info_text.insert("1.0", content)
        self.cpu_info_text.config(state="disabled", padx=20, pady=20)

        self.after(self.aktualisierungsrate, self.update_info)

if __name__ == "__main__":
    cpu_fenster = tk.Tk()
    cpu_fenster.title("CPU-Informationen")
    cpu_fenster.geometry("800x600")
    cpu_frame = ModulCpu(cpu_fenster, refresh_interval=1000)
    cpu_frame.pack(expand=True, fill="both")
    cpu_fenster.mainloop()




