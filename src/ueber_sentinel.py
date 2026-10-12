# ---------------------------------
# Sentinel Hardware Monitor / Projektarbeit zur Zertifizierung / Software Developer (IHK) 2024-2025
# ---------------------------------
# Florian Schimbold
#----------------------------------
# Modul Über Sentinel
#----------------------------------
import tkinter as tk

class ModulInformation(tk.Frame):
    def __init__(self, parent, bg="gray13", fg="white", **kwargs):
        super().__init__(parent, bg=bg, **kwargs)

        self.ram_label = tk.Label(
            self,
            font=("Consolas", 18),
            justify="center",
            anchor="n",
            fg=fg,
            bg=bg,
            wraplength=760,
            text=("Willkommen bei Sentinel!\n"
                               "\nDieses Programm ist Teil meiner Projektprüfung und Zertifizierung, "
                               "im Rahmen des Kurses: Software Developer (IHK)"
                               "\n\nOktober 2024 - Juli 2025"
                               "\n\nEntwickler: Florian Schimbold"
                               "\n\nVersion: 0.1.1 "))

        self.ram_label.pack(fill="both", expand=True, padx=20, pady=20)

if __name__ == "__main__":
    ram_fenster = tk.Tk()
    ram_fenster.title("Über Sentinel")
    ram_fenster.geometry("800x600")
    ram_frame = ModulInformation(ram_fenster)
    ram_frame.pack(expand=True, fill="both")
    ram_fenster.mainloop()

