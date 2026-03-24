# ⚖️ Law Formatter

A simple Windows desktop tool that takes messy legal case `.txt` files and formats them into clean, one-sentence-per-line text — so you can actually read them.

---

## 📥 Download

> No Python, no setup. Just download and run!

1. Go to the [**Releases**](../../releases) page
2. Download the latest `law_formatter.exe`
3. Double-click it, pick your file, and you're done ✅

Your formatted file saves automatically to your Desktop as `filename_formatted.txt`.

---

## ✨ What It Does

- **One sentence per line** — splits on `).` `.)` `."` `?` `;` `...` `…`
- **Smart abbreviation protection** — citations like `F. Supp. 2d`, `9th Cir.`, `Fed. R. Civ. P.`, `N.D. Ill.` never get broken apart
- **"United States" → "US"** for cleaner citation style
- **Removes double spaces** automatically

---

## 🛠️ Build From Source

**Install dependencies:**
```
pip install pillow pyinstaller
```

**Run the script directly:**
```
python law_formatter.py
```

**Build the .exe:**
```
python -m PyInstaller --onefile --noconsole --add-data "cat-yippe.gif;." --icon "law_formatter.ico" law_formatter.py
```

Output will be at `dist\law_formatter.exe`.

---

## 📁 Repo Files

| File | What it is |
|---|---|
| `law_formatter.py` | Main script |
| `cat-yippe.gif` | The very important success animation |
| `law_formatter.ico` | App icon |
| `README.md` | You are here |
