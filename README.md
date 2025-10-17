# RHLunch

A simple command-line tool to get lunch menus from Gourmedia.

## 🧩 Installation

Follow these steps to set up **Python**, **pip**, and a **virtual environment** on your system.  
These instructions cover **macOS**, **Windows**, and **Linux**.

---

### 🐍 1. Check if Python is already installed

Open a terminal (or PowerShell on Windows) and run:

```bash
python --version
```

or

```bash
python3 --version
```

If the version is **3.8+**, you can skip to **step 2** or **step 3**, depending on your preferred way of running python apps.

---

### 🍎 macOS

#### Option A — Recommended (using Homebrew)

1. [Install Homebrew](https://brew.sh) if you don’t already have it:
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```
2. Install Python:
   ```bash
   brew install python
   ```
3. Confirm installation:
   ```bash
   python3 --version
   pip3 --version
   ```

#### Option B — Direct download

You can also download the latest Python installer from [python.org/downloads](https://www.python.org/downloads/).

---

### 🪟 Windows

1. Go to [python.org/downloads](https://www.python.org/downloads/windows/).
2. Download the latest **Windows installer**.
3. Run the installer and **check the box** that says:
   ```
   Add Python to PATH
   ```
4. Confirm installation:
   ```powershell
   python --version
   pip --version
   ```

---

### 🐧 Linux (Debian/Ubuntu)

1. Update your package list:
   ```bash
   sudo apt update
   ```
2. Install Python and pip:
   ```bash
   sudo apt install -y python3 python3-pip
   ```
3. Confirm installation:
   ```bash
   python3 --version
   pip3 --version
   ```

*(For Fedora or Arch, use `dnf` or `pacman` accordingly.)*

---

### 🧱 2. Create a Virtual Environment

It’s good practice to isolate project dependencies in a virtual environment.

From your project root:

```bash
python3 -m venv .venv
```

Activate it:

- **macOS / Linux:**
  ```bash
  source .venv/bin/activate
  ```

- **Windows (PowerShell):**
  ```powershell
  .venv\Scripts\Activate
  ```

When active, your prompt should look like this:
```
(.venv) $
```

To deactivate:
```bash
deactivate
```

---

### 📦 3. Clone/Install project from Github

### From GitHub

```bash
pip install git+https://github.com/engdahl/rhlunch.git
```

### From source

```bash
git clone https://github.com/engdahl/rhlunch.git
cd rhlunch
pip install -e .
```

This installs the `lunch` command globally on your system.

### 🍽️ 4. Usage

Get today's lunch menu:

```bash
lunch
```

Show only vegetarian options:

```bash
lunch -v
```

Show only meat options:

```bash
lunch -m
```

Show the whole week menu:

```bash
lunch -w
```

## Example Output

```
🍽️  Lunch Menu for Today
==================================================

🥬 Vegetarian Options:
  • Vegetariskt Moussaka på vegofärs,aubergine,potatis,serveras med tzatziki

🥩 Meat Options:
  • Ärtsoppa Ärtsoppa/Vegan Fläskbog,timjan,mejram,senap
  • Pannkaka Yessufs goda pannkisar med drottningsylt och vispad grädde
```

## License

MIT License - see LICENSE file for details.
