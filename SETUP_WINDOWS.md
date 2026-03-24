# PathPilot AI — Windows Setup Guide

## Prerequisites

**Install these before anything else:**


2. **Ollama** — https://ollama.com/download/windows
   - Run the installer, then open a new Command Prompt and verify:
     ```
     ollama --version
     ```

---

## Step 1 — Download Ollama Model

Open Command Prompt and run:

```
ollama pull tinyllama
```

This downloads the TinyLlama AI model (~600 MB). Keep Ollama running in the background — it starts automatically on Windows after install.

---

## Step 2 — Get the Project Files

Either clone the repo or copy the project folder to your Windows machine. You should have a folder called `kvay` (or your project folder name) that contains `app.py`.

---

## Step 3 — Install Dependencies

Open Command Prompt, navigate into the project folder:

```
cd path\to\kvay project 
```

Install all required packages globally witht`:

```
pip install -r requirements.txt
```

> **If `faiss-cpu` fails on Windows**, try:
> ```
> pip install faiss-cpu --no-deps
> pip install faiss-cpu
> ```
> Or install the pre-built wheel:
> ```
> pip install faiss-cpu==1.7.4
> ```

---

## Step 4 — Set Up Environment File

In the project folder, create a file called `.env` (copy from `.env.example`):

```
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=tinyllama
SECRET_KEY=your-random-secret-key-here
```

You can create this in Notepad — just save it as `.env` (not `.env.txt`). In Notepad, choose **"All Files"** as the file type when saving.

---

## Step 5 — Run the App

Make sure Ollama is running (it should be in the system tray), then in the project folder:

```
python app.py
```

Open your browser and go to:

```
http://localhost:5000
```

---

