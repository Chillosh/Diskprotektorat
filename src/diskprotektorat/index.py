import customtkinter
import pathlib

frame = customtkinter.CTkFrame
font = "Arial"

class NavigationBar(frame):
    def __init__(self, master, callback, **kwargs):
        super().__init__(master, fg_color="transparent", height=40, **kwargs)
        self.callback = callback
        self.btn_back = customtkinter.CTkButton(self, text="back", width=30)
        self.btn_back.pack(side="left", padx=5, pady=5)
        self.path_entry = customtkinter.CTkEntry(self, placeholder_text="C:/")
        self.path_entry.pack(side="left", fill="x", expand=True, padx=10, pady=5)
        self.path_entry.bind("<Return>", lambda e: self.callback(self.path_entry.get()))


class Sidebar(frame):
    def __init__(self, master, callback, **kwargs):
        super().__init__(master, width=200, corner_radius=0, **kwargs)
        self.callback = callback
        self.label = customtkinter.CTkLabel(self, text="Quick Access", font=(font, 12, "bold"))
        self.label.pack(pady=10)

        for drive in ["C:/", "D:/"]:
            if pathlib.Path(drive).exists():
                btn = customtkinter.CTkButton(self, text=drive, fg_color="transparent", anchor="w", command=lambda d=drive: self.callback(d))
                btn.pack(fill="x", padx=5)

        home = pathlib.Path.home()
        dirs = ["Downloads", "Documents", "Desktop", "Pictures", "Music"]

        for d_name in dirs:
            full_path = home / d_name
            if full_path.exists():
                customtkinter.CTkButton(self, text=d_name, fg_color="transparent", anchor="w", command=lambda p=full_path: self.callback(p)).pack(fill="x", padx=5)


class Window(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("900x600")
        self.title("Diskprotektorat")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.nav = NavigationBar(master=self, callback=self.load_path)
        self.nav.grid(row=0, column=0, columnspan=2, sticky="ew")

        self.sidebar = Sidebar(master=self, callback=self.load_path)
        self.sidebar.grid(row=2, column=0, sticky="nsew")

        self.main_area = customtkinter.CTkScrollableFrame(master=self, corner_radius=0, fg_color="#1a1a1a")
        self.main_area.grid(row=2, column=1, sticky="nsew")

        self.load_path("C:/")

    def load_path(self, path):
        for widget in self.main_area.winfo_children():
            widget.destroy()

        try:
            p = pathlib.Path(path)
            self.nav.path_entry.delete(0, "end")
            self.nav.path_entry.insert(0, str(p.absolute()))

            for item in p.iterdir():
                color = "#1f538d" if item.is_dir() else "#333333"
                btn = customtkinter.CTkButton(self.main_area, text=item.name,fg_color=color, anchor="w", command=lambda i=item: self.load_path(i) if i.is_dir() else None)
                btn.pack(fill="x", padx=10, pady=2)
        except Exception as e:
            customtkinter.CTkLabel(self.main_area, text=f"Error: {e}").pack()

def main():
    app = Window()
    app.mainloop()

if __name__ == "__main__":
    main()