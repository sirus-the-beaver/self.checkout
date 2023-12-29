import tkinter as tk
from tkinter import messagebox
from picamera import PiCamera
from picamera.array import PiRGBArray
from PIL import Image, ImageTk
import threading
import subprocess

class IDVerificationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ID Verification")

        self.camera = PiCamera()
        self.camera.resolution = (640, 480)
        self.raw_capture = PiRGBArray(self.camera, size=(640, 480))

        self.video_panel = tk.Label(root)
        self.video_panel.pack(padx=10, pady=10)

        self.start_button = tk.Button(root, text="Start Verification", command=self.start_verification)
        self.start_button.pack(pady=10)

        self.is_verification_started = False

    def start_verification(self):
        if not self.is_verification_started:
            self.is_verification_started = True
            self.start_button.config(state=tk.DISABLED)
            self.video_thread = threading.Thread(target=self.capture_video)
            self.video_thread.start()
        else:
            messagebox.showinfo("Verification Already Started", "Verification is already in progress.")

    def capture_video(self):
        for frame in self.camera.capture_continuous(self.raw_capture, format="bgr", use_video_port=True):
            img = frame.array
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(img)
            img = ImageTk.PhotoImage(image=img)
            self.video_panel.img = img
            self.video_panel.config(image=img)
            self.video_panel.update()

            # Check if the user presses the 'ESC' key to stop verification
            key = cv2.waitKey(1)
            if key == 27:  # ESC key
                break

            self.raw_capture.truncate(0)

        self.camera.close()
        self.start_button.config(state=tk.NORMAL)
        self.is_verification_started = False
        self.video_thread.join()
        self.execute_verification_script()

    def execute_verification_script(self):
        script_path = '../scripting/take_picture.py'

        # Example: Run the script in a new process
        try:
            subprocess.run(["python", script_path], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error executing the script: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = IDVerificationApp(root)
    root.mainloop()
