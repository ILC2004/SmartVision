import os
import tkinter as tk
from tkinter import messagebox
import cv2
import datetime
import threading
import winsound
from collections import deque

# ─── Project base directory and save path ─────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SAVE_DIR = os.path.join(BASE_DIR, "recordings")
os.makedirs(SAVE_DIR, exist_ok=True)

# ─── Icon file (relative to script) ───────────────────────────────────
ICON_PATH = os.path.join(BASE_DIR, "pi.ico")

# --- Take Photo ---
def take_photo():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        messagebox.showerror("Error", "Failed to access webcam.")
        return
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        cv2.putText(frame, "Press SPACE to capture, ESC to cancel", (10, 25),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        cv2.imshow("Take Photo", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == 27:
            break
        elif key == 32:
            ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            fname = os.path.join(SAVE_DIR, f"photo_{ts}.jpg")
            cv2.imwrite(fname, frame)
            messagebox.showinfo("Saved", f"Photo saved to:\n{fname}")
            break
    cap.release()
    cv2.destroyAllWindows()

# --- Record Standard Video (10s) ---
def record_video():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        messagebox.showerror("Error", "Webcam access failed.")
        return
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    fname = os.path.join(SAVE_DIR, f"video_{ts}.avi")
    out = cv2.VideoWriter(fname, fourcc, 20.0, (640, 480))
    start = datetime.datetime.now()
    while (datetime.datetime.now() - start).seconds < 10:
        ret, frame = cap.read()
        if not ret:
            break
        cv2.putText(frame, "Recording... ESC to stop", (10, 25),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        out.write(frame)
        cv2.imshow("Recording", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    messagebox.showinfo("Saved", f"Video saved to:\n{fname}")

# --- Live CCTV + Motion Detection (always highlight) ---
def start_cctv():
    def detect_and_record():
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            messagebox.showerror("Error", "Webcam access failed.")
            return
        fps = cap.get(cv2.CAP_PROP_FPS) or 20.0
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fourcc = cv2.VideoWriter_fourcc(*'XVID')

        buffer = deque(maxlen=int(fps * 0.5))
        motion_triggered = False
        writer = None
        start_time = None

        ret, prev = cap.read()
        ret, curr = cap.read()
        while ret:
            buffer.append(prev.copy())
            diff = cv2.absdiff(prev, curr)
            gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray, (5,5), 0)
            _, thr = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
            dil = cv2.dilate(thr, None, iterations=3)
            cnts, _ = cv2.findContours(dil, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            found = any(cv2.contourArea(c) >= 800 for c in cnts)
            if found and not motion_triggered:
                winsound.Beep(1000, 200)
                ts2 = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                fn = os.path.join(SAVE_DIR, f"motion_{ts2}.avi")
                writer = cv2.VideoWriter(fn, fourcc, fps, (width, height))
                motion_triggered = True
                start_time = datetime.datetime.now()
                for fbuf in buffer:
                    writer.write(fbuf)
            if motion_triggered:
                writer.write(prev)
                if (datetime.datetime.now() - start_time).total_seconds() >= 10:
                    writer.release()
                    motion_triggered = False
                    buffer.clear()

            display = prev.copy()
            # always draw bounding boxes on detected motion
            for c in cnts:
                if cv2.contourArea(c) >= 800:
                    x, y, w, h = cv2.boundingRect(c)
                    cv2.rectangle(display, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(display, "Live CCTV - Motion Detection | ESC to exit", (10,25),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1)
            cv2.imshow("Live CCTV", display)

            prev = curr
            ret, curr = cap.read()
            if cv2.waitKey(1) & 0xFF == 27:
                break
        cap.release()
        cv2.destroyAllWindows()

    threading.Thread(target=detect_and_record, daemon=True).start()

# --- GUI Setup ---
root = tk.Tk()
root.title("Smart Vision Toolkit")
root.geometry("480x480")
root.configure(bg="#003d3b")
root.iconbitmap(ICON_PATH)

FONT_TITLE = ("Helvetica", 18, "bold")
FONT_BUTTON = ("Helvetica", 12)
FG_COLOR = "#ffffff"
BUTTON_BG = "#caa169"
BUTTON_FG = "#000000"

# Title Label
tk.Label(root, text="Smart Vision Toolkit", font=FONT_TITLE, fg=FG_COLOR, bg="#003d3b").pack(pady=15)

# Buttons
for txt, cmd in [
    ("📸 Take Photo", take_photo),
    ("🎥 Record Video", record_video),
    ("🟢 Live CCTV", start_cctv)
]:
    tk.Button(root, text=txt, font=FONT_BUTTON, bg=BUTTON_BG, fg=BUTTON_FG,
              command=cmd, width=35, height=2).pack(pady=5)

if __name__ == "__main__":
    root.mainloop()
