import customtkinter
from pathlib import Path


class SimpleExplorer(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("800x500")
        self.title("Basic Explorer")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar = customtkinter.CTkFrame(self, width=160, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        customtkinter.CTkLabel(self.sidebar, text="Menu", font=("Arial", 20)).pack(pady=20)
        customtkinter.CTkButton(self.sidebar, text="Home").pack(pady=10, padx=20)
        customtkinter.CTkButton(self.sidebar, text="Settings").pack(pady=10, padx=20)

        self.scrollable_frame = customtkinter.CTkScrollableFrame(self, label_text="Files in Current Directory")
        self.scrollable_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        self.load_files()

    def load_files(self):
        current_dir = Path.cwd()
        for item in current_dir.iterdir():
            icon = "📁" if item.is_dir() else "📄"
            label = customtkinter.CTkLabel(self.scrollable_frame, text=f"{icon} {item.name}")
            label.pack(anchor="w", padx=10, pady=2)


if __name__ == "__main__":
    app = SimpleExplorer()
    app.mainloop()