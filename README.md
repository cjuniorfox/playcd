# 🎵 playcd

`playcd` is a simple **CD audio player** written in Python.  
It can be controlled via:

- ⌨️ **Keyboard shortcuts** (`a`, `d`, `w`, `s`, `space`)  
- 📡 **Named pipe (FIFO)** commands (for scripting and automation)  

The backend uses:

- [pycdio](https://pypi.org/project/pycdio/) for CD drive access  
- [sounddevice](https://python-sounddevice.readthedocs.io/) for audio playback (PortAudio)  

---

## 🚀 Features

- Play, pause, stop, next, and previous track controls  
- Keyboard listener for interactive use  
- Pipe listener for external control (`echo "pause" > /tmp/playcd.fifo`)  
- Runs on **Linux** (NixOS, Debian, Fedora, etc.) and experimental **Windows** support  

---

## 📦 Installation

### Python dependencies

Install the package with `pip`:

```bash
pip install .
````

Or install from source:

```bash
git clone https://github.com/cjuniorfox/playcd.git
cd playcd
pip install -e .
```

---

## ⚙️ System dependencies

`playcd` requires **libcdio** and **PortAudio** to be available on your system.

### NixOS

```nix
environment.systemPackages = with pkgs; [
  portaudio
  libcdio
];
```

### Debian / Ubuntu

```bash
sudo apt install libcdio-dev portaudio19-dev
```

### Fedora

```bash
sudo dnf install libcdio-devel portaudio-devel
```

### Windows

- Install [PortAudio](http://www.portaudio.com/download.html) and make sure `portaudio.dll` is in your PATH.
- Install [libcdio](https://www.gnu.org/software/libcdio/).
- Then install Python dependencies with `pip install -e .`.

⚠️ Note: Windows support is experimental and not guaranteed to work out of the box.

---

## 🎹 Usage

### Keyboard mode

Run `playcd` in a terminal and control playback with keys:

| Key      | Action      |
| -------- | ------------|
| `w`      | Play        |
| `s`      | Stop        |
| `space`  | Pause       |
| `a`      | Previous    |
| `d`      | Next        |
| `q`      | Rewind      |
| `e`      | Fast Forward|
| `Ctrl+C` | Quit        |

---

### 📡 API Mode

`playcd` listen commands over a Rest API on port `8001`.

Requests:

| URI                   | Command      |
|-----------------------|--------------|
|`POST /commands/play`  | Play         |
|`POST /commands/stop`  | Stop         |
|`POST /commands/pause` | Pause        |
|`POST /commands/prev`  | Previous     |
|`POST /commands/next`  | Next         |
|`POST /commands/rew`   | Rewind       |
|`POST /commands/ff`    | Fast Forward |

Display Information:

Information about the current disc, track, and playback state can be retrieved at:

#### GET /display

```json
{
  "status" : "ok",
  "display" : {
    "disc": {
        "operaton": "disc",
        "icon": "",
        "time": { "current": "01:00", "total": "55:00" }
    },
    "track": {
       "operation" : "play",
       "icon" : "",
       "track" : 1,
       "time" : { "current" : "01:00", "total" : "04:30" }
    }
  }
}
```

You can integrate this into scripts or other applications.

---

## 🐍 Embedding in Python

You can use the **listeners** directly in your own Python applications.

### Keyboard listener

```python
import logging
from playcd.keyboard_listener import KeyboardListener

logging.basicConfig(level=logging.INFO)
listener = KeyboardListener(logging)

listener.start()

print("Press keys (w/s/a/d/space)...")
while True:
    cmd = listener.get_command()
    if cmd:
        print("Received command:", cmd)
        if cmd == "quit":
            listener.stop()
            break
```

## 🛠 Development

Clone the repo and install in editable mode:

```bash
git clone https://github.com/cjuniorfox/playcd.git
cd playcd
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

---

## 🧾 License

MIT License – see [LICENSE](LICENSE) for details.
