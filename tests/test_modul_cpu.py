import unittest
from unittest.mock import patch, MagicMock
import tkinter as tk

from sentinel_cpu_info import ModulCpu

# Dummy-Klasse, um WMI-Daten zu simulieren
class DummyProcessor:
    Manufacturer = 'Intel'
    Name = 'Core i7'
    NumberOfCores = 4
    NumberOfLogicalProcessors = 8
    MaxClockSpeed = 3500

class TestModulCpu(unittest.TestCase):
    def setUp(self):
        # Kopflose Tk-Root instanziieren
        self.root = tk.Tk()
        self.root.withdraw()

        # WMI patchen
        patcher_wmi = patch('sentinel_cpu_info.wmi.WMI')
        self.mock_wmi_class = patcher_wmi.start()
        self.addCleanup(patcher_wmi.stop)
        mock_wmi_instance = MagicMock()
        mock_wmi_instance.Win32_Processor.return_value = [DummyProcessor()]
        self.mock_wmi_class.return_value = mock_wmi_instance

        # platform patchen
        patcher_machine = patch('sentinel_cpu_info.platform.machine', return_value='x86_64')
        patcher_machine.start()
        self.addCleanup(patcher_machine.stop)
        patcher_version = patch('sentinel_cpu_info.platform.version', return_value='10.0.19041')
        patcher_version.start()
        self.addCleanup(patcher_version.stop)

        # psutil patchen
        patcher_freq = patch('sentinel_cpu_info.psutil.cpu_freq', return_value=MagicMock(current=2000.0))
        patcher_freq.start()
        self.addCleanup(patcher_freq.stop)
        patcher_percent = patch('sentinel_cpu_info.psutil.cpu_percent', return_value=[10, 20, 30, 40])
        patcher_percent.start()
        self.addCleanup(patcher_percent.stop)

        # ModulCpu ohne wiederholende after-Timer
        self.modul = ModulCpu(self.root, refresh_interval=999999)
        self.modul.after = lambda interval, func: None

    def tearDown(self):
        self.modul.destroy()
        self.root.destroy()

    def test_ausgabe_cpu_info(self):
        info = self.modul.ausgabe_cpu_info()
        expected_keys = {
            'Hersteller', 'Modell', 'Kerne (physisch)', 'Kerne (logisch)',
            'Max-Takt (MHz)', 'Architektur', 'OS-Version', 'Takt aktuell (MHz)'
        }
        self.assertEqual(set(info.keys()), expected_keys)
        self.assertEqual(info['Hersteller'], 'Intel')
        self.assertEqual(info['Modell'], 'Core i7')
        self.assertEqual(info['Kerne (physisch)'], 4)
        self.assertEqual(info['Kerne (logisch)'], 8)
        self.assertEqual(info['Max-Takt (MHz)'], 3500)
        self.assertEqual(info['Architektur'], 'x86_64')
        self.assertEqual(info['OS-Version'], '10.0.19041')
        self.assertEqual(info['Takt aktuell (MHz)'], '2000.00')

    def test_update_info_updates_text_widget(self):
        # Nach Aufruf sollte das Text-Widget CPU-Infos enthalten
        self.modul.update_info()
        content = self.modul.cpu_info_text.get('1.0', 'end')
        self.assertIn('=== CPU Infos ===', content)
        self.assertIn('Hersteller: Intel', content)
        # Gesamt-Auslastung = (10+20+30+40)/4 = 25.0
        self.assertIn('Gesamt-Auslastung : 25.0 %', content)
        self.assertIn('Kern 1 Auslastung : 10.0 %', content)
        self.assertIn('Kern 4 Auslastung : 40.0 %', content)

if __name__ == '__main__':
    unittest.main()
