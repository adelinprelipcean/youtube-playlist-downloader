# 🎵 Play.listed — YouTube Playlist Downloader

![Version](https://img.shields.io/badge/version-2.0.0-blue?style=for-the-badge)
![Status](https://img.shields.io/badge/status-stable-brightgreen?style=for-the-badge)
![Python](https://img.shields.io/badge/python-3.11%20%7C%203.12-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/platform-Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-green?style=for-the-badge)

**Play.listed** is a modern, fast, and secure desktop application designed to automate the process of downloading and converting entire YouTube playlists. With an intuitive interface and an asynchronous processing engine, the app allows users to save media content in **MP3 (Audio)** and **MP4 (Video)** formats with a single click.

<img width="693" height="629" alt="image" src="https://github.com/user-attachments/assets/3dad18d3-45d3-4971-b16f-27d3b26225da" />

## 🚀 Key Features

- **Mass Download:** Paste a single link and instantly download the entire playlist.
- **Format Selector:** Total flexibility—easily choose between **Audio (MP3)** for music or **Video (MP4)** for clips directly from the UI.
- **High Performance:** Built on a **Multithreading** architecture, ensuring the interface remains responsive even during heavy processing tasks.
- **Auto-Conversion:** Integrated media engine (powered by _FFmpeg_ and _MoviePy_) that processes video streams and converts them to high-quality audio automatically.
- **Modern Design:** Clean, minimalist "Dark Mode" GUI built with the `CustomTkinter` framework.

---

## 🛡️ Security & Transparency

This is an **open-source** project. The source code is completely transparent and available for audit in this repository.

Because this application is developed independently ("Indie Software") and does not hold a commercial digital certificate (which costs hundreds of dollars annually), some antivirus engines may generate _False Positive_ alerts based on heuristics (e.g., _Generic.Malware_ or _Wacatac.B!ml_).

This is standard behavior for applications packaged with **PyInstaller**, as the structure of the generated `.exe` file (which bundles the Python interpreter and libraries) can resemble that of unauthorized programs.

**Antivirus Scan Result:**
✅ **[View VirusTotal Report Here](https://www.virustotal.com/gui/file/efc400ec7a4604e20470d92adbc18764d569f9944032240634d2346f4616b834/detection)**
_(File verified. Confirmed "Clean" by industry leaders: Microsoft, BitDefender, Kaspersky, Avast, Eset, etc.)_

> **Note:** If Windows Defender displays the _SmartScreen_ window ("Windows protected your PC") upon first run, this is strictly due to the lack of a digital signature, not because of any actual threat.

---

## 📥 Installation & Usage

The application is **portable** (no installation required).

1.  Download the latest version (`Playlisted.exe`) from the **[Releases](../../releases/latest)** section.
2.  Launch the downloaded file.
    - _If the SmartScreen warning appears:_ Click **More info** -> **Run anyway**.
3.  Paste the YouTube playlist link into the input box.
4.  Select your desired format (**MP3** or **MP4**) using the central switch.
5.  Click **Download** and watch the progress in the status bar.

---

## 🛠️ Build from Source (For Developers)

If you prefer running the application directly from the source code or building your own executable for maximum security, follow the steps below:

**1. Clone the repository**

```bash
git clone [https://github.com/adelinprelipcean/youtube-playlist-downloader.git](https://github.com/adelinprelipcean/youtube-playlist-downloader.git)
cd youtube-playlist-downloader
```

**2. Install dependencies**

```bash
pip install -r requirements.txt
```

**3. Run the application**

```bash
python main.py
```

**4. (Optional) Build your own .exe To repackage the application yourself:**

```bash
pyinstaller --noconsole --onefile --collect-all customtkinter --collect-all moviepy --collect-all pytubefix --copy-metadata imageio --name Playlisted main.py
```

---

## 📖 The Story Behind the Project

Play.listed originally started as a personal passion project before I started university, driven by my curiosity to explore Python's capabilities in automating file manipulation processes.

Recently, I decided to bring the project up to current professional standards (v2.0). I completely refactored the legacy code, transforming it from a simple CLI script into a robust GUI application. This iteration solved complex technical challenges, such as managing media dependencies (FFmpeg), implementing asynchronous multithreading, and correctly packaging the executable for Windows distribution.

---

## 💻 Tech Stack
- Core: Python 3.12

- GUI: CustomTkinter (Modern UI wrapper)

- API Wrapper: Pytubefix

- Media Processing: MoviePy, FFmpeg

- Deployment: PyInstaller

---
  © 2025 <strong>Adelin Prelipcean</strong>. Distributed under the MIT License.
