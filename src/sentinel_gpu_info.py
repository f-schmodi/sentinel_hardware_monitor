# ---------------------------------
# Sentinel Hardware Monitor / Projektarbeit zur Zertifizierung / Software Developer (IHK) 2024-2025
# ---------------------------------
# Florian Schimbold
#----------------------------------
# Modul GPU
#----------------------------------
import tkinter as tk
import wmi

class ModulGpu(tk.Frame):
    def __init__(self, parent, bg="gray13", fg="white", refresh_interval=5000, **kwargs):
        super().__init__(parent, **kwargs)
        self.aktualisierungsrate = refresh_interval
        self.gpu_info_label = tk.Label(
            self,
            anchor='nw',
            justify="left",
            bg=bg,
            fg=fg,
            font=("Consolas", 18))
        self.gpu_info_label.pack(fill="both", expand=True)

        # WMI‑Anbindung
        self.wmi_info_statisch  = wmi.WMI(namespace="root\\CIMV2")
        self.wmi_info_dynamisch = wmi.WMI(namespace="root\\CIMV2")
        # Aktualisierung starten
        self.ausgabe_gpu_info_mit_update()
    # Abfrage GPU Daten und Aktualisierung
    def ausgabe_gpu_info_mit_update(self):
        gpus            = self.wmi_info_statisch.Win32_VideoController()
        auslastung      = self.wmi_info_dynamisch.Win32_PerfFormattedData_GPUPerformanceCounters_GPUEngine()
        gpu_speicher    = self.wmi_info_dynamisch.Win32_PerfFormattedData_GPUPerformanceCounters_GPUAdapterMemory()

        zeilen = []
        for gpu_index, gpu in enumerate(gpus):
            modell              = gpu.Name
            ram_in_mb           = int(gpu.AdapterRAM or 0) // (1024 ** 2)
            treiber             = gpu.DriverVersion or "–"
            auslastung_prozent  = next((objekt.UtilizationPercentage for objekt in auslastung
                                        if f"luid_{gpu_index}_"
                                        in objekt.Name
                                        and "_3D"
                                        in objekt.Name), 0)

            speicher_status     = next((objekt for objekt in gpu_speicher
                                        if f"luid_{gpu_index}_" in objekt.Name), None)

            speicher_genutzt_in_mb = int(speicher_status.LocalUsageBytes) // (1024 ** 2) if speicher_status else 0

            zeilen.append(f"=== GPU Infos ===")
            zeilen.append(f"\nGPU{gpu_index+1}:")
            zeilen.append(f"\nModell               : {modell}")
            zeilen.append(f"Gesamtspeicher       : {ram_in_mb} MB")
            zeilen.append(f"Treiberversion       : {treiber}")
            zeilen.append(f"3D-Auslastung        : {auslastung_prozent} %")
            zeilen.append(f"Genutzter Speicher   : {speicher_genutzt_in_mb} MB")
            zeilen.append("")

        content = "\n".join(zeilen).strip()
        self.gpu_info_label.config(text=content, padx=20, pady=20)
        self.after(self.aktualisierungsrate, self.ausgabe_gpu_info_mit_update)

if __name__ == "__main__":
    gpu_fenster = tk.Tk()
    gpu_fenster.title("Grafikkarten (GPU)")
    gpu_fenster.geometry("800x600")
    gpu_frame = ModulGpu(gpu_fenster, refresh_interval=5000)
    gpu_frame.pack(expand=True, fill="both")
    gpu_fenster.mainloop()
