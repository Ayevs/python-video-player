import tkinter as tk
from tkinter import filedialog
from screeninfo import get_monitors
import vlc
import os

# Get monitors
monitors = get_monitors()
main_monitor = monitors[0]
second_monitor = monitors[1] if len(monitors) > 1 else main_monitor  # fallback

# VLC setup
instance = vlc.Instance()
player = instance.media_player_new()
fullscreen_window = None


def play_video():
    global fullscreen_window

    if fullscreen_window:
        fullscreen_window.destroy()
        fullscreen_window = None

    file_path = filedialog.askopenfilename(
        filetypes=[("Video files", "*.mp4 *.mkv *.avi *.mov")]
    )
    if not file_path:
        return

    media = instance.media_new(file_path)
    player.set_media(media)

    # Create dummy fullscreen window on second monitor
    fullscreen_window = tk.Toplevel()
    fullscreen_window.overrideredirect(True)  # borderless
    fullscreen_window.geometry(
        f"{second_monitor.width}x{second_monitor.height}+{second_monitor.x}+{second_monitor.y}"
    )
    fullscreen_window.attributes("-topmost", True)

    # Embed VLC into that window
    video_frame = tk.Frame(fullscreen_window)
    video_frame.pack(fill="both", expand=True)
    fullscreen_window.update_idletasks()

    player.set_hwnd(
        video_frame.winfo_id()
    )  # On Linux/macOS use player.set_xwindow or set_nsobject
    player.play()


def stop_video():
    global fullscreen_window

    if player.is_playing():
        player.stop()

    if fullscreen_window:
        fullscreen_window.destroy()
        fullscreen_window = None


def stop_and_play():
    stop_video()
    play_video()


# Create the control window
root = tk.Tk()
root.title("Video Player Controls")
root.geometry(
    f"300x100+{main_monitor.x+50}+{main_monitor.y+50}"
)  # position on main monitor

# buttons
open_btn = tk.Button(root, text="Open Video", command=stop_and_play)
open_btn.pack(side=tk.LEFT, padx=10, pady=20)

stop_btn = tk.Button(root, text="Stop", command=stop_video)
stop_btn.pack(side=tk.LEFT, padx=10, pady=20)

root.mainloop()
