import sys
import tkinter as tk
from tkinter import simpledialog, messagebox
from PIL import Image, ImageTk


def start_ia():
    root.destroy()
    import main_ia
    main_ia.main()


def start_server():
    root.destroy()
    import main_lan
    sys.argv = ["main_lan.py", "server"]
    main_lan.main()


def start_client():
    ip = simpledialog.askstring("Cliente LAN", "Introduce la IP del servidor:")
    if not ip:
        messagebox.showwarning("Aviso", "No se ha introducido ninguna IP.")
        return
    root.destroy()
    import main_lan
    sys.argv = ["main_lan.py", "client", ip]
    main_lan.main()


# ---------------------------
#   VENTANA PRINCIPAL
# ---------------------------

root = tk.Tk()
root.geometry("800x600")
root.overrideredirect(True)  # Oculta la barra nativa
root.resizable(False, False)

# Centrar ventana
root.update_idletasks()
w, h = 800, 600
ws = root.winfo_screenwidth()
hs = root.winfo_screenheight()
x = (ws // 2) - (w // 2)
y = (hs // 2) - (h // 2)
root.geometry(f"{w}x{h}+{x}+{y}")


# ---------------------------
#   FONDO
# ---------------------------

try:
    bg_image = Image.open("assets/gui/background.jpg")
    bg_image = bg_image.resize((800, 600), Image.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)

    background_label = tk.Label(root, image=bg_photo)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
except:
    root.configure(bg="#1e1e2f")


# ---------------------------
#   BARRA SUPERIOR PERSONALIZADA
# ---------------------------

BAR_HEIGHT = 60
bar = tk.Frame(root, bg="#0a1a2a", height=BAR_HEIGHT)
bar.pack(fill="x")

# Icono radar
try:
    icon_img = Image.open("assets/gui/icon.ico")
    icon_img = icon_img.resize((40, 40), Image.LANCZOS)
    icon_photo = ImageTk.PhotoImage(icon_img)
    icon_label = tk.Label(bar, image=icon_photo, bg="#0a1a2a")
    icon_label.place(x=10, y=10)
except:
    pass

# Título
title_label = tk.Label(
    bar,
    text="Batalla Naval V5",
    fg="white",
    bg="#0a1a2a",
    font=("Arial", 20, "bold")
)
title_label.place(relx=0.5, rely=0.5, anchor="center")

# Botón cerrar
def close_app():
    root.destroy()

close_btn = tk.Button(
    bar,
    text="✖",
    font=("Arial", 16, "bold"),
    fg="white",
    bg="#0a1a2a",
    activebackground="#112233",
    bd=0,
    command=close_app
)
close_btn.place(x=560, y=10, width=30, height=30)


# Hacer la ventana arrastrable
def start_move(event):
    root.x = event.x
    root.y = event.y

def on_move(event):
    x = event.x_root - root.x
    y = event.y_root - root.y
    root.geometry(f"+{x}+{y}")

bar.bind("<ButtonPress-1>", start_move)
bar.bind("<B1-Motion>", on_move)

# ---------------------------
#   BOTONES DEL MENÚ
# ---------------------------

frame = tk.Frame(root, bg="")  # Frame invisible para ver el fondo
frame.place(x=20, y=400)       # Alineado a la izquierda con margen amplio

def make_button(text, command):
    btn = tk.Button(
        frame,
        text=text,
        font=("Arial", 14, "bold"),
        width=22,
        bg="#2b2b40",
        fg="white",
        activebackground="#444466",
        activeforeground="white",
        relief="raised",
        bd=4,
        command=command
    )
    btn.pack(pady=10, anchor="w")  # Alineación izquierda
    return btn

make_button("Jugar contra la IA", start_ia)
make_button("Servidor LAN", start_server)
make_button("Cliente LAN", start_client)

root.mainloop()