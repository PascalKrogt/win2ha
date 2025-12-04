
# MQTT Windows Bridge

A lightweight Python service that connects a Windows PC to [Home Assistant](https://www.home-assistant.io) via [MQTT](https://mqtt.org).  
It uses MQTT Discovery to automatically create a switch entity in Home Assistant and runs predefined safe commands when toggled ON or OFF.

---

## ✨ Features
- 🔗 Native **Home Assistant MQTT Discovery**
- ⚙️ **Predefined, safe command mapping** (no arbitrary execution)
- 🪶 **Lightweight** – single Python script using `paho-mqtt`
- 🖥️ **Runs quietly in background** via Task Scheduler or as a Windows service

---

## 🧩 Requirements
- Windows 10 or 11
- Python 3.9+ (with `pip`)
- MQTT broker accessible from the host (e.g. Mosquitto)
- Home Assistant MQTT integration enabled

---

## ⚙️ Installation

1. **Clone or download this repository**
   ```bash
   git clone https://github.com/<youruser>/mqtt-windows-bridge.git
   cd mqtt-windows-bridge
   ```

2. **Install dependencies**
   ```bash
   pip install paho-mqtt
   ```

3. **Edit configuration**
   Open `mqtt_windows_bridge.py` in a text editor and set:
   ```python
   BROKER = "your.mqtt.broker"
   USERNAME = "mqtt_user"
   PASSWORD = "mqtt_password"
   COMMAND_ON  = ["C:\\Path\\to\\wsds.exe", "tv.on"]
   COMMAND_OFF = ["C:\\Path\\to\\wsds.exe", "tv.dis"]
   ```

4. **Test manually**
   ```bash
   python mqtt_windows_bridge.py
   ```
   You should see a switch appear in Home Assistant under MQTT entities.

---

## 🔄 Make it start automatically

### Option A – Task Scheduler (recommended)

1. Open **Task Scheduler** → *Create Task …*
2. **General tab**
   - Name: `MQTT Windows Bridge`
   - Run whether user is logged on or not
   - Run with highest privileges
3. **Triggers tab**
   - New → *At startup* (or *At log on*)
4. **Actions tab**
   - Start a program:  
     ```
     C:\Path\To\Python\pythonw.exe
     ```
   - *Add arguments*:  
     ```
     "C:\Path\To\mqtt_windows_bridge.py"
     ```
   - *Start in*:  
     ```
     C:\Path\To\
     ```
5. Save and, if requested, enter your user password.

---

### Option B – Startup Folder (user‑only)

1. Press `Win + R`, run `shell:startup`
2. Create shortcut:
   ```
   pythonw.exe "C:\Path\To\mqtt_windows_bridge.py"
   ```
3. The script will start each time you log in.

---

## 🪶 Logging (optional)

Add this snippet near the top of your script to record output:
```python
import sys, os
sys.stdout = open(os.path.join(os.path.dirname(__file__), "mqtt_windows_bridge.log"), "a", buffering=1)
sys.stderr = sys.stdout
```

---

## 📜 License
This project is released under the [MIT License](LICENSE).


