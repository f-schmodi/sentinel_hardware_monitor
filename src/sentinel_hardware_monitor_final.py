# ---------------------------------
# Sentinel Hardware Monitor / Projektarbeit zur Zertifizierung / Software Developer (IHK) 2024-2025
# ---------------------------------
# Florian Schimbold
#----------------------------------

import os
import tkinter as tk
from PIL import Image, ImageTk
import tkinter.font as tkfont

from sentinel_datenspeicher_info import ModulDatenspeicher
from sentinel_mainboard_bios_info import ModulMainboardBios
from sentinel_ram_info import ModulArbeitsspeicher
from sentinel_cpu_info import ModulCpu
from sentinel_gpu_info import ModulGpu
from ueber_sentinel import ModulInformation


class Hauptfenster(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sentinel Hardware Monitor")
        self.configure(bg="gray26")
        self.geometry("1400x1000")
        self.resizable(width=0, height=0)

        farbe_hintergrund_menue = "gray8"
        farbe_hintergrund_container = "gray26"
        farbe_hintergrund_button = "gray26"
        farbe_button_klick = "gray43"
        farbe_schrift = "snow"
        # Sidebar zur Navigation
        self.sidebar = tk.Frame(self, width=800, bg=farbe_hintergrund_menue)
        self.sidebar.pack(side="left", fill="y")
        # Container für wechselnde Frames
        self.container = tk.Frame(self, bg=farbe_hintergrund_container)
        self.container.pack(side="right", fill="both", expand=True)
        # Dictionary um alle Frames zu speichern
        self.frames = {}
        for fenster in (Startseite, Mainboard, CPU, GPU, Datenspeicher, Arbeitsspeicher, Information):
            seiten_name = fenster.__name__
            frame = fenster(parent=self.container,
                            controller=self,
                            bg=farbe_hintergrund_container,
                            fg=farbe_schrift)

            self.frames[seiten_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        #
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # Einbindung Buttons Menü für jeden Frame in der sidebar
        for button, aufruf_frame in [("Startseite", "Startseite"),
                                     ("Mainboard/BIOS", "Mainboard"),
                                     ("Prozessor(CPU)", "CPU"),
                                     ("Grafikkarten(GPU)", "GPU"),
                                     ("Datenspeicher(HDD/SSD)", "Datenspeicher"),
                                     ("Arbeitsspeicher(RAM)", "Arbeitsspeicher"), ]:

            menue_buttons = tk.Button(self.sidebar,
                                      text=button,
                                      command=lambda erzeugung=aufruf_frame: self.erstelle_frame(erzeugung),
                                      bg=farbe_hintergrund_button, fg=farbe_schrift,
                                      activebackground=farbe_button_klick,
                                      activeforeground=farbe_schrift,
                                      relief="flat")
            menue_buttons.pack(fill="x", pady=5, padx=10)
        # Button Beenden
        menue_buttons = tk.Button(self.sidebar,
                                  text="Beenden",
                                  command=self.destroy,
                                  bg=farbe_hintergrund_button, fg=farbe_schrift,
                                  activebackground=farbe_button_klick,
                                  activeforeground=farbe_schrift,
                                  relief="flat")
        menue_buttons.pack(side="bottom", fill="x", pady=5, padx=10)
        # Button Information
        menue_buttons = tk.Button(self.sidebar,
                                  text="Über Sentinel",
                                  command=lambda: self.erstelle_frame("Information"),
                                  bg=farbe_hintergrund_button, fg=farbe_schrift,
                                  activebackground=farbe_button_klick,
                                  activeforeground=farbe_schrift,
                                  relief="flat")
        menue_buttons.pack(side="bottom", fill="x", pady=5, padx=10)
        # Frame bei Programmstart
        self.erstelle_frame("Startseite")

    def erstelle_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
# Klassen der jeweiligen Module die importiert werden
class Startseite(tk.Frame):
    def __init__(self, parent, controller, bg, fg):
        super().__init__(parent, bg=bg)
        logo_pfad = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs", "Sentinel_Logo_v2.jpg")
        sentinel_logo = Image.open(logo_pfad)
        bild_logo = ImageTk.PhotoImage(sentinel_logo)
        logo_label = tk.Label(self, image=bild_logo)
        logo_label.image = bild_logo
        logo_label.pack()

class Mainboard(tk.Frame):
    def __init__(self, parent, controller, bg, fg):
        super().__init__(parent, bg=bg)
        self.ueberschrift_font = tk.font.Font(family="Helvetica", size=24, weight="bold")
        frame_mainboard = tk.Label(self, text="Mainboard/BIOS", bg=bg, fg=fg, font=self.ueberschrift_font)
        frame_mainboard.pack(pady=20, padx=20)
        self.mainboard_bios_info = ModulMainboardBios(self)
        self.mainboard_bios_info.pack(fill="both", expand=True, padx=10, pady=10)

class CPU(tk.Frame):
    def __init__(self, parent, controller, bg, fg):
        super().__init__(parent, bg=bg)
        self.ueberschrift_font = tk.font.Font(family="Helvetica", size=24, weight="bold")
        frame_cpu = tk.Label(self, text="CPU", bg=bg, fg=fg, font=self.ueberschrift_font)
        frame_cpu.pack(pady=20, padx=20)
        self.cpu_info = ModulCpu(self, relief=tk.FLAT)
        self.cpu_info.pack(fill="both", expand=True, padx=10, pady=10)

class GPU(tk.Frame):
    def __init__(self, parent, controller, bg, fg):
        super().__init__(parent, bg=bg)
        self.überschrift_font = tk.font.Font(family="Helvetica", size=24, weight="bold")
        frame_gpu = tk.Label(self, text="GPU", bg=bg, fg=fg, font=self.überschrift_font)
        frame_gpu.pack(pady=20, padx=20)
        self.gpu_info = ModulGpu(self, relief=tk.FLAT)
        self.gpu_info.pack(fill="both", expand=True, padx=10, pady=10)

class Datenspeicher(tk.Frame):
    def __init__(self, parent, controller, bg, fg):
        super().__init__(parent, bg=bg)
        self.überschrift_font = tk.font.Font(family="Helvetica", size=24, weight="bold")
        frame_datenspeicher = tk.Label(self, text="Datenspeicher", bg=bg, fg=fg, font=self.überschrift_font)
        frame_datenspeicher.pack(pady=20, padx=20)
        self.ssd_info = ModulDatenspeicher(self, relief=tk.FLAT)
        self.ssd_info.pack(fill="both", expand=True, padx=10, pady=10)

class Arbeitsspeicher(tk.Frame):
    def __init__(self, parent, controller, bg, fg):
        super().__init__(parent, bg=bg)
        self.überschrift_font = tk.font.Font(family="Helvetica", size=24, weight="bold")
        frame_arbeitsspeicher = tk.Label(self, text="Arbeitsspeicher(RAM)", bg=bg, fg=fg, font=self.überschrift_font)
        frame_arbeitsspeicher.pack(pady=20, padx=20)
        self.ram_info = ModulArbeitsspeicher(self, relief=tk.FLAT)
        self.ram_info.pack(fill="both", expand=True, padx=10, pady=10)

class Information(tk.Frame):
    def __init__(self, parent, controller, bg, fg):
        super().__init__(parent, bg=bg)
        self.überschrift_font = tk.font.Font(family="Helvetica", size=24, weight="bold")
        frame_information = tk.Label(self, text="Über Sentinel", bg=bg, fg=fg, font=self.überschrift_font)
        frame_information.pack(pady=20, padx=20)
        self.sentinel_info = ModulInformation(self, relief=tk.FLAT)
        self.sentinel_info.pack(fill="both", expand=True, padx=10, pady=10)

if __name__ == "__main__":
    main_fenster = Hauptfenster()
    main_fenster.mainloop()

