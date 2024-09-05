import customtkinter as ctk
from tkinter import filedialog, messagebox, Toplevel
from PIL import Image, ImageTk, ImageDraw, ImageFont
from collections import Counter
import numpy as np
from datetime import datetime
import math
from sklearn.cluster import KMeans
import os
import threading

# Configuração inicial do CustomTkinter
ctk.set_appearance_mode("System")  # Segue o tema do sistema (light/dark)
ctk.set_default_color_theme("blue")  # Tema padrão

# Função para converter RGB para HEX
def rgb_to_hex(rgb_color):
    return "#{:02x}{:02x}{:02x}".format(rgb_color[0], rgb_color[1], rgb_color[2])

# Função para quantizar cores usando K-means
def quantize_colors(pixels, num_colors):
    kmeans = KMeans(n_clusters=num_colors)
    kmeans.fit(pixels)
    cluster_centers = kmeans.cluster_centers_.astype(int)
    labels = kmeans.labels_
    pixel_count = Counter(labels)
    total_pixels = len(pixels)
    color_percentages = {
        rgb_to_hex(tuple(cluster_centers[i])): (count / total_pixels) * 100
        for i, count in pixel_count.items()
    }
    return color_percentages

# Função para obter as porcentagens de cores da imagem
def get_image_colors(image_path, num_colors=10):
    img = Image.open(image_path)
    img = img.convert("RGB")
    pixels = np.array(img).reshape((-1, 3))
    color_percentages = quantize_colors(pixels, num_colors)
    return color_percentages

# Função para desenhar os círculos e a imagem
def draw_color_circles(image_path, color_percentages, output_image_path):
    image_width = 1080
    image_height = 1080
    output_image = Image.new("RGB", (image_width, image_height), (255, 255, 255))
    draw = ImageDraw.Draw(output_image)
    original_img = Image.open(image_path)
    original_img.thumbnail((200, 200))
    output_image.paste(original_img, (10, 10))
    num_colors = len(color_percentages)
    columns = 3
    rows = math.ceil(num_colors / columns)
    max_circle_diameter = min(image_width // (columns + 1), image_height // (rows + 1)) - 30
    min_circle_diameter = max_circle_diameter // 2
    font = ImageFont.load_default()
    x_margin = image_width // (columns + 1)
    y_margin = image_height // (rows + 1)
    
    for i, (hex_color, percentage) in enumerate(color_percentages.items()):
        circle_diameter = int(min_circle_diameter + (percentage / 100) * (max_circle_diameter - min_circle_diameter))
        x_pos = (i % columns) * x_margin + x_margin // 2 + 200
        y_pos = (i // columns) * y_margin + y_margin // 2 + 50
        color_rgb = tuple(int(hex_color[i:i+2], 16) for i in (1, 3, 5))
        draw.ellipse([x_pos, y_pos, x_pos + circle_diameter, y_pos + circle_diameter], fill=color_rgb, outline=(0, 0, 0))
        text_position = (x_pos, y_pos + circle_diameter + 5)
        draw.text(text_position, f"{hex_color} ({percentage:.2f}%)", fill=(0, 0, 0), font=font)
    
    output_image.save(output_image_path)
    return output_image_path

# Função para carregar a imagem e mostrar no label
def load_image():
    global image_path
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
    if file_path:
        image_path = file_path
        img = Image.open(image_path)
        img.thumbnail((200, 200))
        img = ImageTk.PhotoImage(img)
        image_label.config(image=img)
        image_label.image = img
        messagebox.showinfo("Imagem carregada", "Imagem carregada com sucesso!")

# Função para mostrar popup de carregamento
def show_loading_popup():
    loading_popup = Toplevel(app)
    loading_popup.title("Processando...")
    loading_popup.geometry("200x100")
    loading_popup.grab_set()  # Bloqueia interação com a janela principal
    
    loading_label = ctk.CTkLabel(loading_popup, text="Gerando imagem...\nAguarde.", font=("Arial", 14))
    loading_label.pack(pady=20)

    return loading_popup

# Função que roda o processo em segundo plano
def generate_image_in_background(loading_popup):
    try:
        num_colors = int(color_entry.get())
        color_percentages = get_image_colors(image_path, num_colors)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_image_path = f"output_image_{timestamp}.jpg"
        draw_color_circles(image_path, color_percentages, output_image_path)
        loading_popup.destroy()  # Fecha o popup de loading
        messagebox.showinfo("Imagem gerada", f"Imagem gerada e salva em {output_image_path}")
    except Exception as e:
        loading_popup.destroy()  # Fecha o popup de loading em caso de erro
        messagebox.showerror("Erro", f"Falha ao gerar a imagem: {str(e)}")

# Função principal para gerar a imagem com o popup de loading
def generate_image():
    if not image_path:
        messagebox.showerror("Erro", "Nenhuma imagem foi selecionada.")
        return
    
    # Mostrar popup de carregamento
    loading_popup = show_loading_popup()
    
    # Criar e rodar thread para evitar bloqueio da UI
    threading.Thread(target=generate_image_in_background, args=(loading_popup,)).start()

# Interface gráfica com CustomTkinter
app = ctk.CTk()
app.title("Gerador de Paleta de Cores")
app.geometry("500x500")

image_path = None

# Título
title_label = ctk.CTkLabel(app, text="Gerador de Paleta de Cores", font=("Arial", 20))
title_label.pack(pady=20)

# Botão para selecionar imagem
select_image_btn = ctk.CTkButton(app, text="Selecionar Imagem", command=load_image)
select_image_btn.pack(pady=10)

# Label para mostrar a imagem carregada
image_label = ctk.CTkLabel(app)
image_label.pack(pady=10)

# Entrada para número de cores
color_frame = ctk.CTkFrame(app)
color_frame.pack(pady=10)
color_label = ctk.CTkLabel(color_frame, text="Número de Cores:", font=("Arial", 14))
color_label.grid(row=0, column=0, padx=10)
color_entry = ctk.CTkEntry(color_frame)
color_entry.insert(0, "10")  # Valor padrão
color_entry.grid(row=0, column=1)

# Botão para gerar a imagem
generate_image_btn = ctk.CTkButton(app, text="Gerar Imagem", command=generate_image)
generate_image_btn.pack(pady=20)

# Loop da interface
app.mainloop()