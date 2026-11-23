from datetime import datetime
import customtkinter as ctk

# Configuración visual moderna
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

app = ctk.CTk()
app.title("CyberShield Pro v2.5")
app.geometry("620x520")

# Título principal
titulo = ctk.CTkLabel(
    app,
    text="CYBERSHIELD URL SCANNER PRO",
    font=("Roboto", 22, "bold"),
    text_color="#00ff88",
)
titulo.pack(pady=(20, 5))

subtitulo = ctk.CTkLabel(
    app,
    text="Analizador avanzado de enlaces sospechosos con historial automatico",
    font=("Roboto", 13),
    text_color="gray",
)
subtitulo.pack(pady=(0, 15))

# Caja redondeada para escribir el enlace
caja_url = ctk.CTkEntry(
    app,
    width=480,
    height=42,
    corner_radius=10,
    font=("Roboto", 13),
    placeholder_text="Pega aqui el enlace sospechoso y pulsa Enter...",
)
caja_url.pack(pady=10)


# --- FUNCIONES PRINCIPALES ---
def revisar():
    url = caja_url.get().strip().lower()
    if not url:
        return

    riesgo = 0
    razones = []

    # 1. Comprobar cifrado HTTPS
    if "http://" in url:
        riesgo += 2
        razones.append("• No usa HTTPS (conexion sin cifrar)")

    # 2. Comprobar símbolo '@'
    if "@" in url:
        riesgo += 3
        razones.append("• Contiene '@' (truco de redireccion oculta)")

    # 3. Comprobar guiones en el enlace
    if "-" in url:
        riesgo += 1
        razones.append("• Tiene guiones sospechosos en el dominio")

    # 4. Comprobar acortadores de enlaces
    if any(
        acortador in url
        for acortador in ["bit.ly", "tinyurl.com", "t.co", "goo.gl"]
    ):
        riesgo += 2
        razones.append("• Usa un acortador de enlaces oculto")

    # 5. Comprobar extensiones de dominio baratas/peligrosas
    if any(
        ext in url
        for ext in [".xyz", ".tk", ".top", ".click", ".buzz", ".info"]
    ):
        riesgo += 2
        razones.append("• Usa una extension de dominio sospechosa")

    # 6. Comprobar palabras típicas de estafa
    palabras = [
        "login",
        "banco",
        "verificar",
        "paypal",
        "premio",
        "gratis",
        "urgente",
        "cuenta",
        "password",
    ]
    if any(p in url for p in palabras):
        riesgo += 2
        razones.append("• Contiene palabras tipicas de suplantacion")

    detalle = "\n".join(razones)

    # Actualizar interfaz visual según el nivel de riesgo
    if riesgo >= 4:
        estado = "PELIGRO ALTO"
        barra_riesgo.set(1.0)
        barra_riesgo.configure(progress_color="#ff4d4d")
        resultado.configure(
            text=f"{estado} ({riesgo} pts)\n\n{detalle}", text_color="#ff4d4d"
        )
    elif riesgo >= 2:
        estado = "PRECAUCION"
        barra_riesgo.set(0.55)
        barra_riesgo.configure(progress_color="#ffcc00")
        resultado.configure(
            text=f"{estado} ({riesgo} pts)\n\n{detalle}", text_color="#ffcc00"
        )
    else:
        estado = "SEGURO"
        barra_riesgo.set(0.15)
        barra_riesgo.configure(progress_color="#00ff88")
        resultado.configure(
            text="ENLACE SEGURO\n\nNo se detectaron senales de peligro.",
            text_color="#00ff88",
        )

    # Guardar registro automático en historial.txt con fecha y hora
    ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("historial.txt", "a", encoding="utf-8") as archivo:
        archivo.write(f"[{ahora}] {estado} ({riesgo} pts) -> {url}\n")


def limpiar():
    caja_url.delete(0, "end")
    barra_riesgo.set(0)
    resultado.configure(text="Esperando enlace...", text_color="white")


def pegar_y_analizar():
    try:
        texto_copiado = app.clipboard_get()
        limpiar()
        caja_url.insert(0, texto_copiado)
        revisar()
    except Exception:
        resultado.configure(
            text="No hay ningun texto copiado en el portapapeles.",
            text_color="#ffcc00",
        )


# Permitir analizar pulsando la tecla Enter en la caja de texto
caja_url.bind("<Return>", lambda event: revisar())

# Contenedor horizontal para los 3 botones
caja_botones = ctk.CTkFrame(app, fg_color="transparent")
caja_botones.pack(pady=10)

boton_analizar = ctk.CTkButton(
    caja_botones,
    text="ANALIZAR",
    command=revisar,
    width=150,
    height=38,
    corner_radius=10,
    font=("Roboto", 13, "bold"),
)
boton_analizar.pack(side="left", padx=6)

boton_pegar = ctk.CTkButton(
    caja_botones,
    text="PEGAR Y ANALIZAR",
    command=pegar_y_analizar,
    width=170,
    height=38,
    corner_radius=10,
    fg_color="#1f538d",
    hover_color="#14375e",
    font=("Roboto", 13, "bold"),
)
boton_pegar.pack(side="left", padx=6)

boton_limpiar = ctk.CTkButton(
    caja_botones,
    text="LIMPIAR",
    command=limpiar,
    width=110,
    height=38,
    corner_radius=10,
    fg_color="#333344",
    hover_color="#444455",
    font=("Roboto", 13, "bold"),
)
boton_limpiar.pack(side="left", padx=6)

# Barra de peligro visual
barra_riesgo = ctk.CTkProgressBar(app, width=480, height=12, corner_radius=6)
barra_riesgo.set(0)
barra_riesgo.pack(pady=(15, 5))

# Tarjeta redondeada para mostrar el informe
tarjeta = ctk.CTkFrame(app, width=480, height=180, corner_radius=15)
tarjeta.pack(pady=15, padx=40, fill="both", expand=True)

resultado = ctk.CTkLabel(
    tarjeta,
    text="Esperando enlace...",
    font=("Roboto", 14, "bold"),
    justify="left",
)
resultado.pack(pady=25, padx=20)

# Arrancar aplicación (siempre al final)
app.mainloop()
