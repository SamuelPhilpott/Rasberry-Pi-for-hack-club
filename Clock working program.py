import tkinter as tk
from datetime import datetime
import time

# ----------------------------
# COLOR THEMES
# ----------------------------
COLOR_SCHEMES = [
    ("#000000", "#FFFFFF"),
    ("#FFFFFF", "#000000"),
    ("#111111", "#00E0FF"),
    ("#202020", "#FF3366"),
    ("#0C0C0C", "#FFD700"),
]
scheme_index = 0

alarm_time = None
alarm_triggered = False
alarm_frame = None

# ----------------------------
# MAIN WINDOW
# ----------------------------
root = tk.Tk()
root.title("Apple-Style Flip Clock")
root.attributes("-fullscreen", True)
root.configure(bg="black")

width = root.winfo_screenwidth()
height = root.winfo_screenheight()
bg, fg = COLOR_SCHEMES[scheme_index]

# ----------------------------
# CLOCK LABELS
# ----------------------------
time_label = tk.Label(root,
                      font=("SF Pro Display", int(height * 0.25), "bold"),
                      fg=fg, bg=bg)
time_label.place(relx=0.45, rely=0.45, anchor="center")

ampm_label = tk.Label(root,
                      font=("SF Pro Display", int(height * 0.07), "bold"),
                      fg=fg, bg=bg)
ampm_label.place(relx=0.85, rely=0.45, anchor="center")

# ----------------------------
# ANIMATION HELPERS
# ----------------------------
current_hour = None
current_minute = None


def flip_animation(new_text):
    """Simulate a quick flip animation when hour changes."""
    for scale in [1.0, 0.7, 0.4, 0.7, 1.0]:
        time_label.config(font=("SF Pro Display", int(height * 0.25 * scale), "bold"))
        time_label.update()
        time.sleep(0.05)
    time_label.config(text=new_text)


def fade_animation(new_text):
    """Smooth fade animation for minute change."""
    for opacity in range(100, 30, -10):
        color = f"#{opacity:02x}{opacity:02x}{opacity:02x}"
        time_label.config(fg=color)
        time_label.update()
        time.sleep(0.02)
    time_label.config(text=new_text)
    time_label.config(fg=fg)


# ----------------------------
# MAIN LOOP
# ----------------------------
def update_time():
    global current_hour, current_minute, alarm_triggered

    now = datetime.now()
    hour_str = now.strftime("%I").lstrip("0")
    minute_str = now.strftime("%M")
    ampm_str = now.strftime("%p")

    full_time = f"{hour_str}:{minute_str}"

    # Flip animation for hour change
    if hour_str != current_hour:
        flip_animation(full_time)
        current_hour = hour_str
    # Fade for minute change
    elif minute_str != current_minute:
        fade_animation(full_time)
        current_minute = minute_str
    else:
        time_label.config(text=full_time)

    ampm_label.config(text=ampm_str)

    # Alarm trigger logic
    if alarm_time:
        current = now.strftime("%I:%M %p").lstrip("0")
        if current == alarm_time and not alarm_triggered:
            alarm_triggered = True
            show_alarm_alert()
        elif current != alarm_time:
            alarm_triggered = False

    root.after(1000, update_time)


# ----------------------------
# COLOR FUNCTIONS
# ----------------------------
def change_color(event=None):
    widget = event.widget
    if isinstance(widget, (tk.Button, tk.Spinbox, tk.Frame)):
        return
    global scheme_index, bg, fg
    scheme_index = (scheme_index + 1) % len(COLOR_SCHEMES)
    bg, fg = COLOR_SCHEMES[scheme_index]
    apply_colors()


def apply_colors():
    root.configure(bg=bg)
    time_label.configure(bg=bg, fg=fg)
    ampm_label.configure(bg=bg, fg=fg)
    set_alarm_btn.configure(bg=bg, fg=fg, activebackground=bg)
    if alarm_frame:
        alarm_frame.configure(bg=bg)
        for child in alarm_frame.winfo_children():
            try:
                child.configure(bg=bg, fg=fg)
            except tk.TclError:
                pass


# ----------------------------
# ALARM FUNCTIONS
# ----------------------------
def show_alarm_alert():
    alert = tk.Toplevel(root)
    alert.attributes("-fullscreen", True)
    alert.configure(bg="#FF4444")

    tk.Label(alert, text="⏰ ALARM!",
             font=("SF Pro Display", int(height * 0.2), "bold"),
             fg="white", bg="#FF4444").pack(expand=True)

    tk.Button(alert, text="Dismiss",
              font=("SF Pro Display", 50),
              bg="#111", fg="white",
              width=15, height=2,
              command=alert.destroy).pack(pady=50)


def open_alarm_menu():
    global alarm_frame
    if alarm_frame:
        return

    alarm_frame = tk.Frame(root, bg="#111111", width=width, height=height)
    alarm_frame.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(alarm_frame, text="Set Alarm",
             font=("SF Pro Display", 70, "bold"),
             bg="#111111", fg="#00FFAA").pack(pady=40)

    picker_frame = tk.Frame(alarm_frame, bg="#111111")
    picker_frame.pack(pady=20)

    hours = [str(h) for h in range(1, 13)]
    minutes = [f"{m:02}" for m in range(0, 60)]
    ampm_values = ["AM", "PM"]

    hour_var = tk.StringVar(value="6")
    minute_var = tk.StringVar(value="30")
    ampm_var = tk.StringVar(value="AM")

    font_size = int(height * 0.06)

    hour_spin = tk.Spinbox(picker_frame, values=hours,
                           font=("SF Pro Display", font_size, "bold"),
                           width=4, justify="center",
                           bg="#000000", fg="#00FFAA",
                           buttonbackground="#222222",
                           relief="flat", wrap=True,
                           textvariable=hour_var)
    minute_spin = tk.Spinbox(picker_frame, values=minutes,
                             font=("SF Pro Display", font_size, "bold"),
                             width=4, justify="center",
                             bg="#000000", fg="#00FFAA",
                             buttonbackground="#222222",
                             relief="flat", wrap=True,
                             textvariable=minute_var)
    ampm_spin = tk.Spinbox(picker_frame, values=ampm_values,
                           font=("SF Pro Display", font_size, "bold"),
                           width=4, justify="center",
                           bg="#000000", fg="#00FFAA",
                           buttonbackground="#222222",
                           relief="flat", wrap=True,
                           textvariable=ampm_var)

    hour_spin.grid(row=0, column=0, padx=30)
    minute_spin.grid(row=0, column=1, padx=30)
    ampm_spin.grid(row=0, column=2, padx=30)

    def confirm_alarm():
        global alarm_time, alarm_frame, alarm_triggered
        alarm_time = f"{hour_var.get()}:{minute_var.get()} {ampm_var.get()}"
        alarm_triggered = False
        alarm_frame.destroy()
        alarm_frame = None

    def cancel_alarm():
        global alarm_frame
        alarm_frame.destroy()
        alarm_frame = None

    btn_frame = tk.Frame(alarm_frame, bg="#111111")
    btn_frame.pack(pady=60)

    tk.Button(btn_frame, text="Cancel",
              font=("SF Pro Display", 50, "bold"),
              bg="#333333", fg="#FFFFFF",
              width=10, height=2,
              command=cancel_alarm).grid(row=0, column=0, padx=60)

    tk.Button(btn_frame, text="Set",
              font=("SF Pro Display", 50, "bold"),
              bg="#00CC66", fg="#FFFFFF",
              width=10, height=2,
              command=confirm_alarm).grid(row=0, column=1, padx=60)


def close_app(event):
    root.destroy()

# ----------------------------
# BUTTONS
# ----------------------------
set_alarm_btn = tk.Button(root,
                          text="Set Alarm",
                          font=("SF Pro Display", 30),
                          bg="#333333", fg="#FFFFFF",
                          activebackground="#555555",
                          relief="flat",
                          command=open_alarm_menu)
set_alarm_btn.place(relx=0.05, rely=0.9, anchor="w")

# ----------------------------
# BINDINGS
# ----------------------------
root.bind("<Button-1>", change_color)
root.bind("<Escape>", close_app)

# ----------------------------
# START
# ----------------------------
update_time()
root.mainloop()
