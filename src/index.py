import customtkinter
frame = customtkinter.CTkFrame
font = "Arial"

class NavigationBar(frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", height=40, **kwargs)
        self.btn_back = customtkinter.CTkButton(self, text="back", width=30)
        self.btn_back.pack(side="left", padx=5, pady=5)
        self.btn_forward = customtkinter.CTkButton(self, text="forward", width=30)
        self.btn_forward.pack(side="left", padx=5, pady=5)
        self.path_entry = customtkinter.CTkEntry(self, placeholder_text="C:/")
        self.path_entry.pack(side="left", fill="x", expand=True, padx=10, pady=5)

class Header(frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, border_width=1, border_color="#333333", height=50, corner_radius=0, **kwargs)
        self.label = customtkinter.CTkLabel(self, text="Header", font=(font, 16, "bold"))
        self.label.pack(side="left", padx=20)

class Sidebar(frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, width=200, corner_radius=0, **kwargs)
        self.label = customtkinter.CTkLabel(self, text="File", font=(font, 12, "bold"))
        self.label.pack(pady=10)

class Window(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("900x600")
        self.title("Custom File Explorer")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.nav = NavigationBar(master=self)
        self.nav.grid(row=0, column=0, columnspan=2, sticky="ew")

        self.header = Header(master=self)
        self.header.grid(row=1, column=0, columnspan=2, sticky="ew")

        self.sidebar = Sidebar(master=self)
        self.sidebar.grid(row=2, column=0, sticky="nsew")

        self.main_area = frame(master=self, corner_radius=0, fg_color="#1a1a1a")
        self.main_area.grid(row=2, column=1, sticky="nsew")

        self.placeholder = customtkinter.CTkLabel(self.main_area, text="Nějaké soubory")
        self.placeholder.pack(expand=True)


if __name__ == "__main__":
    app = Window()
    app.mainloop()