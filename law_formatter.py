import re
import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
 
 
def resource_path(relative_name):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_name)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), relative_name)
 
 
def format_case(input_path):
    with open(input_path, "r", encoding="utf-8") as f:
        text = f.read()
 
    # Join all lines into one block
    text = text.replace("\n", " ")
 
    # Collapse multiple spaces into one
    text = re.sub(r' {2,}', ' ', text)
 
    # Replace "United States" with "US"
    text = re.sub(r'\bUnited States\b', 'US', text)
 
    # ── Protect tokens that must NOT trigger a sentence break ──────────────────
    # Longer/more-specific patterns must come first
    protections = [
        # Multi-word patterns first
        ("F. Supp. 2d",  "FSUPP2D_PROTECT"),
        ("F. Supp.",     "FSUPP_PROTECT"),
        ("L. Rev.",      "LREV_PROTECT"),
        ("L. Rev",       "LREVNP_PROTECT"),
        ("Fed. R.",      "FEDR_PROTECT"),
        # State/district court abbreviations
        ("N.D.",         "ND_PROTECT"),
        ("S.D.",         "SD_PROTECT"),
        ("E.D.",         "ED_PROTECT"),
        ("W.D.",         "WD_PROTECT"),
        ("D.C.",         "DC_PROTECT"),
        ("Ill.",         "ILL_PROTECT"),
        ("Cal.",         "CAL_PROTECT"),
        ("CAL.",         "CAL2_PROTECT"),
        ("Tex.",         "TEX_PROTECT"),
        ("TEX.",         "TEX2_PROTECT"),
        ("N.Y.",         "NY_PROTECT"),
        ("Fla.",         "FLA2_PROTECT"),
        # Federal rules
        ("Civ.",         "CIV_PROTECT"),
        ("Evid.",        "EVID_PROTECT"),
        ("Proc.",        "PROC_PROTECT"),
        # Existing
        ("Fed.",         "FED_PROTECT"),
        ("Cir.",         "CIR_PROTECT"),
        # Titles
        ("dr.",          "DR_PROTECT"),
        ("Dr.",          "DRCAP_PROTECT"),
        ("mr.",          "MR_PROTECT"),
        ("Mr.",          "MRCAP_PROTECT"),
        ("mrs.",         "MRS_PROTECT"),
        ("Mrs.",         "MRSCAP_PROTECT"),
        # Legal/legislative
        ("Pub.",         "PUB_PROTECT"),
        ("Rep.",         "REP_PROTECT"),
        ("H.R.",         "HR_PROTECT"),
        ("RES.",         "RES_PROTECT"),
        ("COLUM.",       "COLUM_PROTECT"),
        ("SCI.",         "SCI_PROTECT"),
        ("TECH.",        "TECH_PROTECT"),
        ("CONG.",        "CONG_PROTECT"),
        ("INTELL.",      "INTELL_PROTECT"),
        ("PROP.",        "PROP_PROTECT"),
        ("Cf.",          "CF_PROTECT"),
        ("CALIF.",       "CALIF_PROTECT"),
        ("FLA.",         "FLA_PROTECT"),
        # Standard legal citation
        ("v.",           "V_PROTECT"),
        ("U.S.",         "US_PROTECT"),
        ("F.3d",         "F3D_PROTECT"),
        ("F.2d",         "F2D_PROTECT"),
        ("F.4th",        "F4TH_PROTECT"),
        ("U.S.C.",       "USC_PROTECT"),
        ("No.",          "NO_PROTECT"),
        ("Sec.",         "SEC_PROTECT"),
        ("pp.",          "PP_PROTECT"),
        ("p.",           "P_PROTECT"),
        ("id.",          "ID_PROTECT"),
        ("Id.",          "IDCAP_PROTECT"),
        ("et al.",       "ETAL_PROTECT"),
        ("Inc.",         "INC_PROTECT"),
        ("Corp.",        "CORP_PROTECT"),
        ("Co.",          "CO_PROTECT"),
        ("Ltd.",         "LTD_PROTECT"),
        ("App.",         "APP_PROTECT"),
        ("Dist.",        "DIST_PROTECT"),
        ("Supp.",        "SUPP_PROTECT"),
        # Single uppercase letters used in citations like "R." "P." "A." "B."
        # We protect these only when preceded by a space (mid-citation)
    ]
 
    for token, placeholder in protections:
        text = text.replace(token, placeholder)
 
    # Protect single capital letters followed by period used in legal rules
    # e.g. "R." "P." "A." "B." when surrounded by spaces (not sentence-ending)
    text = re.sub(r'(?<= )([A-Z])\. ', lambda m: m.group(1) + '_LETTER_PROTECT ', text)
 
    # Protect ellipsis variants
    text = text.replace(". . . .", "ELLIPSIS4")
    text = text.replace(". . .",   "ELLIPSIS3")
    text = text.replace("...",     "ELLIPSIS3")
    text = text.replace("…",       "ELLIPSIS_U")
 
    # ── Insert sentence-break markers ─────────────────────────────────────────
    SEP = "\x00SPLIT\x00"
 
    # After: ). .) ." ? ; ellipsis — when followed by whitespace + uppercase/digit/[
    pattern = r'(\)\.|\.\"|\.\)|[?;]|ELLIPSIS4|ELLIPSIS3|ELLIPSIS_U)(\s+)(?=[A-Z\[\d])'
    text = re.sub(pattern, lambda m: m.group(1) + SEP, text)
 
    # After a plain period ending a sentence (uppercase next word, not a protected token)
    # This fires on whatever periods remain after protections
    text = re.sub(r'\.(\s+)(?=[A-Z])', lambda m: '.' + SEP, text)
 
    # ── Split and restore ──────────────────────────────────────────────────────
    sentences_raw = text.split(SEP)
    restored = []
    for s in sentences_raw:
        for token, placeholder in protections:
            s = s.replace(placeholder, token)
        # Restore single-letter protections
        s = re.sub(r'([A-Z])_LETTER_PROTECT', r'\1.', s)
        s = s.replace("ELLIPSIS4", ". . . .")
        s = s.replace("ELLIPSIS3", "...")
        s = s.replace("ELLIPSIS_U", "…")
        s = s.strip()
        if s:
            restored.append(s)
 
    # ── Write output ───────────────────────────────────────────────────────────
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    filename = os.path.splitext(os.path.basename(input_path))[0] + "_formatted.txt"
    output_path = os.path.join(desktop, filename)
 
    with open(output_path, "w", encoding="utf-8") as f:
        for s in restored:
            f.write(s + "\n")
 
    return output_path, len(restored)
 
 
def show_success_dialog(parent, sentence_count, output_path):
    dialog = tk.Toplevel(parent)
    dialog.title("Done!")
    dialog.resizable(False, False)
    dialog.grab_set()
 
    w, h = 340, 320
    sw = dialog.winfo_screenwidth()
    sh = dialog.winfo_screenheight()
    x = (sw - w) // 2
    y = (sh - h) // 2
    dialog.geometry(f"{w}x{h}+{x}+{y}")
    dialog.configure(bg="#ffffff")
 
    gif_path = resource_path("cat-yippe.gif")
    frames = []
    durations = []
    try:
        gif = Image.open(gif_path)
        idx = 0
        while True:
            try:
                gif.seek(idx)
                frame = gif.copy().convert("RGBA")
                frames.append(ImageTk.PhotoImage(frame))
                durations.append(max(gif.info.get("duration", 80), 20))
                idx += 1
            except EOFError:
                break
    except Exception:
        frames = []
        durations = []
 
    if frames:
        canvas = tk.Canvas(dialog, width=150, height=150, bg="#ffffff", highlightthickness=0)
        canvas.pack(pady=(18, 0))
        gif_img = canvas.create_image(75, 75, anchor="center", image=frames[0])
        frame_index = [0]
 
        def animate():
            idx = frame_index[0]
            canvas.itemconfig(gif_img, image=frames[idx])
            delay = durations[idx] if idx < len(durations) else 80
            frame_index[0] = (idx + 1) % len(frames)
            dialog.after(delay, animate)
 
        dialog.after(0, animate)
 
    tk.Label(
        dialog,
        text=f"✅  Formatted {sentence_count} sentences!",
        font=("Segoe UI", 12, "bold"),
        bg="#ffffff",
        fg="#2d6a2d"
    ).pack(pady=(10, 2))
 
    tk.Label(
        dialog,
        text=f"Saved to:\n{output_path}",
        font=("Segoe UI", 9),
        bg="#ffffff",
        fg="#555555",
        wraplength=300,
        justify="center"
    ).pack(pady=(0, 12))
 
    tk.Button(
        dialog,
        text="OK",
        font=("Segoe UI", 10, "bold"),
        bg="#4a90d9",
        fg="white",
        activebackground="#357abd",
        activeforeground="white",
        relief="flat",
        padx=28,
        pady=6,
        cursor="hand2",
        command=dialog.destroy
    ).pack(pady=(0, 16))
 
    dialog.wait_window()
 
 
def select_and_run():
    root = tk.Tk()
    root.withdraw()
 
    input_path = filedialog.askopenfilename(
        title="Select a law case .txt file",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
    )
 
    if not input_path:
        return
 
    try:
        output_path, sentence_count = format_case(input_path)
        show_success_dialog(root, sentence_count, output_path)
    except Exception as e:
        messagebox.showerror("Error", f"Something went wrong:\n{str(e)}")
 
 
if __name__ == "__main__":
    select_and_run()