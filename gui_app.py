import os
import sys
import threading
import customtkinter as ctk
from tkinter import filedialog, messagebox
from video_process import process_video

def get_resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    # Also check parent directory if not found in current (for weights/)
    full_path = os.path.join(base_path, relative_path)
    if not os.path.exists(full_path):
        full_path = os.path.join(os.path.dirname(base_path), relative_path)
    
    return full_path

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("green")

class LuminaLaneApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("LuminaLane AI - Next-Gen Lane Detection")
        self.geometry("600x450")
        
        # UI Elements
        self.header_label = ctk.CTkLabel(self, text="LuminaLane AI", font=ctk.CTkFont(size=30, weight="bold"))
        self.header_label.pack(pady=(40, 5))
        
        self.sub_label = ctk.CTkLabel(self, text="Premium Lane Detection Engine", text_color="gray")
        self.sub_label.pack(pady=(0, 30))

        self.select_button = ctk.CTkButton(self, text="Select Video File", command=self.select_file, height=45, corner_radius=50)
        self.select_button.pack(pady=20)

        self.progress_label = ctk.CTkLabel(self, text="Status: Ready", font=ctk.CTkFont(size=14))
        self.progress_label.pack(pady=(20, 5))

        self.progress_bar = ctk.CTkProgressBar(self, width=400)
        self.progress_bar.set(0)
        self.progress_bar.pack(pady=10)

        self.output_label = ctk.CTkLabel(self, text="", text_color="green")
        self.output_label.pack(pady=20)

        self.selected_path = None

    def select_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4 *.avi *.mov")])
        if file_path:
            self.selected_path = file_path
            filename = os.path.basename(file_path)
            self.progress_label.configure(text=f"Selected: {filename}")
            self.start_processing()

    def start_processing(self):
        if not self.selected_path:
            return

        self.select_button.configure(state="disabled")
        self.progress_label.configure(text="Processing Vision... 0%")
        self.progress_bar.set(0)
        
        output_dir = "videos/output"
        os.makedirs(output_dir, exist_ok=True)
        filename = os.path.basename(self.selected_path)
        output_path = os.path.join(output_dir, f"detected_{filename}")

        model_weight = get_resource_path('weights/tusimple_18.pth')
        
        # Start processing in thread
        thread = threading.Thread(target=self.run_process, args=(self.selected_path, output_path, model_weight))
        thread.start()

    def run_process(self, input_path, output_path, model_weight):
        def progress_callback(percent):
            self.after(0, self.update_progress, percent)

        try:
            process_video(input_path, output_path, model_path=model_weight, callback=progress_callback)
            self.after(0, self.on_complete, output_path)
        except Exception as e:
            self.after(0, self.on_error, str(e))

    def update_progress(self, percent):
        self.progress_bar.set(percent / 100)
        self.progress_label.configure(text=f"Processing Vision... {percent}%")

    def on_complete(self, output_path):
        self.progress_bar.set(1)
        self.progress_label.configure(text="Processing Complete! ✅")
        self.output_label.configure(text=f"Saved to: {os.path.basename(output_path)}")
        self.select_button.configure(state="normal")
        
        # Auto-play the video using the system's default player
        try:
            os.system(f'xdg-open "{output_path}" &')
        except:
            pass

        messagebox.showinfo("Success", f"Lane detection complete!\n\nVideo saved to:\n{output_path}\n\nOpening video...")

    def on_error(self, message):
        self.select_button.configure(state="normal")
        self.progress_label.configure(text="Error occurred ❌")
        messagebox.showerror("Error", f"An error occurred during processing:\n{message}")

if __name__ == "__main__":
    app = LuminaLaneApp()
    app.mainloop()
