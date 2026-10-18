import tkinter as tk
import signal

class HUD:
    def __init__(self):
        self.root = tk.Tk()
        signal.signal(signal.SIGINT, lambda *args: self.root.destroy())
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.attributes("-transparentcolor", "black")
        self.root.configure(bg="black")
    
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        self.root.geometry(f"600x40+100+{sh-1300}")
    
        self.label = tk.Label(
            self.root,
            text="Coach loading...",
            bg="black",
            fg="#E8B84B",
            font=("Arial", 13, "bold"),
            padx=10, pady=8
        )
        self.label.pack()

        self.root.after(200, self._keep_on_top)

    def _keep_on_top(self):
        self.root.attributes("-topmost", True)
        self.root.lift()
        self.root.after(200, self._keep_on_top)


    def update(self, text):
        self.label.config(text=text)

    def run(self):
        self.root.mainloop()
        self._keep_on_top()

if __name__ == "__main__":
    hud = HUD()
    hud.update("Test: You are on Ascent — Blue team")
    hud.run()