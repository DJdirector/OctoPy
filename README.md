<p align="center">
    DJdirector Presents:
</p>

<div align="center">
  <img src="LOGO.png" />
</div>

---

<p align="center">
    <img src="https://img.shields.io/badge/Engine-Python_3-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python Powered">
    <img src="https://img.shields.io/github/license/DJdirector/OctoPy?style=for-the-badge" alt="License">
</p>

<p align="center">
  <a href="#quick-start">Quick Start</a> •
  <a href="#how-it-works">How It Works</a> •
  <a href="#recent">Recent</a> •
  <a href="#customization--forking">Customization & Forking<a> •
  <a href="#configuration">Configuration</a> •
  <a href="#license">License</a>
</p>

<p align="center">
  <small><i><b>Note:</b> OctoPy is currently in early development. While we strive for stability, you may encounter bugs or breaking changes.</i></small>
</p>

<p align="center">
    OctoPy is a high-performance <b>python TUI</b> built with the Textual framework. It is designed to bring order to your terminal by serving as a universal dashboard for organizing, executing, and monitoring scripts in real-time.
    <br /><br />
    <i>Organize. Execute. Verify.</i>
    <br />
    Launch tasks through a sleek interface, monitor live output, and get instant 
    <b>success/fail validation</b> for every run.
</p>

## Quick Start

Navigate to the directory where you want **OctoPy** to live (we suggest your Home directory) and run the following:

```bash
$ git clone https://github.com/DJdirector/OctoPy.git
$ cd OctoPy
$ pip install -r requirements.txt
```
<p align="center"> <small><i><b>Note:</b> OctoPy is self-contained. Depending on your OS, you may need to use a <b>Python Virtual Environment (venv)</b> to install dependencies.</i></small> </p>

**Once installed, fire up the dashboard:**
```bash
$ python main.py
```

## How It Works

**OctoPy** is designed to be a plug-and-play. It dynamically builds your dashboard based on the contents of your `scripts/` directory inside OctoPy.

### Organization & Categories

You don't have to keep everything in one giant list. OctoPy turns subdirectories into logical categories within the TUI:
* **Standard Scripts:** Drop any file directly into `scripts/` for general access.
* **Custom Categories:** Create a folder (e.g., `scripts/Database` or `scripts/Python-Fixes/`). OctoPy will automatically group those scripts under that category header in the interface.

Visual Example:
```plaintext
scripts/
├── setup_git.sh         <-- (Standard Script)
├── Database/            <-- (Category Name)
│   ├── install_db.sh
│   └── migrate.py
└── Network/             <-- (Category Name)
    └── check_ports.sh
```

### Execution Engine

To remain universal, OctoPy executes files using **Bash**. This means you can run Python, Shell, Ruby, or even Node.js scripts as long as they are executable.

**Every Script must...**

**Have Shebang Lines** Every script must include a shebang line at the very top so the system knows which interpreter to use.
* **For Python:** `#!/usr/bin/env python3`
* **For Shell:** `#!/bin/bash`
* **For Node:** `#!/usr/bin/env node`

**Have Permissions** Scripts must be executable. If you encounter a permission error, run:
```bash
$ chmod +x scripts/your-script
```

## Recent

**✨ New in v0.1 (Experimental)**
* **Live Reactive UI:** Powered by Textual, featuring a responsive layout that adapts to your terminal size.
* **Real-time Output Streaming:** Watch script output character-by-character with an auto-scrolling log.
* **Interactive Input:** Send text back to your running scripts (e.g., answering y/n prompts) directly through the dashboard.
* **Hot-Reloading Folder Polling:** OctoPy monitors your scripts/ folder every 2 seconds. Add or remove files, and the sidebar updates automatically without a restart.
* **Cross-Platform Execution:** Smart logic handles .py scripts via the local Python interpreter and falls back to cmd (Windows) or bash (Unix) for other file types.

## Customization & Forking

Want to build your own ultimate dev-environment setup? OctoPy is designed to be forked!

1. **Fork this repository** to your own Github account.
2. **Add your personal scripts** to the `scripts/` directory.
3. **Commit and push** your changes to keep your personal setup portable and accesible on any machine.

Since OctoPy is licensed under the **MIT License**, you are free to modify the source code, change the TUI layout, or even build a specialized version for your team’s specific workflow.

## Configuration

Currently, **OctoPy** is designed for zero-config simplicity—just drop your scripts into the folder and go. However, the command center is evolving.

### Coming Soon

We are working on expanding the configuration options to give you total control over your automation:

* **Batch Execution:** The ability to run an entire category with a single click (perfect for "Full System Setup" folders).
* **Environment Variables:** Define custom variables within a config.json to be passed into your scripts at runtime.
* **Execution Ordering:** Use a prefix (like 01_, 02_) or a config file to determine the exact order in which scripts appear or run.
* **Custom Root Directory:** An option to point OctoPy at any folder on your system, not just the local `scripts/` directory.
* **Remote Root Directory:** An option to point OctoPy to a URL of a website in the cloud or on your local system.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.