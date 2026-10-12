import unittest
import tkinter as tk
from sentinel_hardware_monitor_final import Hauptfenster  # passe den Importpfad an

class TestHauptfenster(unittest.TestCase):
    def setUp(self):
        # Ein unsichtbares Root-Fenster erstellen
        self.app = Hauptfenster()
        self.app.withdraw()  # verhindert, dass das Fenster sichtbar wird

    def tearDown(self):
        # Fenster wieder zerstören, um Ressourcen freizugeben
        self.app.destroy()

    def test_frames_initialization(self):
        # Arrange & Act done in setUp()
        # Assert: alle erwarteten Seiten sind im frames‑Dict
        expected = {
            "Startseite", "Mainboard", "CPU", "GPU",
            "Datenspeicher", "Arbeitsspeicher", "Information"
        }
        self.assertEqual(set(self.app.frames.keys()), expected,
                         "Alle sieben Seiten sollten initial vorhanden sein")

    def test_erstelle_frame_valid(self):
        # Spy auf das tkraise des GPU‑Frames
        gpu_frame = self.app.frames["GPU"]
        called = {"raised": False}
        def fake_raise():
            called["raised"] = True
        gpu_frame.tkraise = fake_raise
        # Act
        self.app.erstelle_frame("GPU")
        # Assert
        self.assertTrue(called["raised"], "tkraise() sollte für das GPU‑Frame aufgerufen werden")

    def test_erstelle_frame_invalid_raises(self):
        # Ein ungültiger Seitenname sollte einen KeyError werfen
        with self.assertRaises(KeyError):
            self.app.erstelle_frame("NichtExistierend")

    def test_window_properties(self):
        # Vor der Abfrage sicherstellen, dass Layout angewendet wird
        self.app.deiconify()  # Fenster sichtbar machen für korrekte Größe
        self.app.update_idletasks()
         # Act: Fenstergröße abfragen
        width = self.app.winfo_width()
        height = self.app.winfo_height()
        # Assert
        self.assertEqual((width, height), (1400, 1000),
                         f"Erwartete Fenstergröße 1400x1000, aber war {width}x{height}")
    def test_window_title(self):
        # Assert: Titel korrekt gesetzt
        self.assertEqual(self.app.title(), "Sentinel Hardware Monitor")

if __name__ == "__main__":
    unittest.main()
