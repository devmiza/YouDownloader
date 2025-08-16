import os
import subprocess
import tkinter as tk
from tkinter import messagebox
from yt_dlp import YoutubeDL
import threading
import sys ### NOVO ###

### NOVO: Função para encontrar o ffmpeg.exe ###
def obter_caminho_ffmpeg():
    """ Determina o caminho para o ffmpeg.exe, seja em modo de script ou executável. """
    if getattr(sys, 'frozen', False):
        # Se estiver rodando como um executável PyInstaller
        return os.path.join(sys._MEIPASS, "ffmpeg.exe")
    else:
        # Se estiver rodando como um script .py
        return "ffmpeg.exe" # Procura na mesma pasta do script

# Verifica ffmpeg (Agora verifica no caminho específico)
def verificar_ffmpeg():
    try:
        caminho_ffmpeg = obter_caminho_ffmpeg()
        # Executa o ffmpeg de forma silenciosa para verificar se existe
        subprocess.run([caminho_ffmpeg, "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return True
    except:
        return False

# Função chamada no botão principal
def mostrar_opcoes_download():
    if not entrada.get():
        messagebox.showwarning("Atenção", "Cole um link do YouTube.")
        return
    
    opcoes_frame.pack(pady=10)

# Botão: Baixar Vídeo
def baixar_video():
    opcoes_frame.pack_forget()
    threading.Thread(target=lambda: iniciar_download(entrada.get(), "video")).start()

# Botão: Baixar MP3
def baixar_mp3():
    if not verificar_ffmpeg():
        # Esta mensagem agora aparecerá se o ffmpeg não for empacotado corretamente
        messagebox.showerror("Erro", "O ffmpeg.exe não foi encontrado junto com o programa.")
        return
    opcoes_frame.pack_forget()
    threading.Thread(target=lambda: iniciar_download(entrada.get(), "audio")).start()

# Função de download
def iniciar_download(link, tipo):
    try:
        downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")

        if tipo == "video":
            ydl_opts = {
                'outtmpl': os.path.join(downloads_path, '%(title)s.%(ext)s'),
                'progress_hooks': [barra_progresso],
            }
        else:
            # Opções para áudio (MP3)
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': os.path.join(downloads_path, '%(title)s.mp3'), # Força a extensão .mp3
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'progress_hooks': [barra_progresso],
                'ffmpeg_location': obter_caminho_ffmpeg() ### NOVO: Informa ao yt-dlp onde está o ffmpeg ###
            }

        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])
            status_var.set(f"✅ Download finalizado!\nSalvo em: {downloads_path}")
            entrada.delete(0, tk.END)
    except Exception as e:
        status_var.set("❌ Erro ao baixar")
        messagebox.showerror("Erro", str(e))

# Barra de progresso
def barra_progresso(d):
    if d['status'] == 'downloading':
        percent = d.get('_percent_str', '0.0%').strip()
        status_var.set(f"⬇️ Baixando... {percent}")
    elif d['status'] == 'finished':
        status_var.set("🟢 Finalizando conversão...")

# UI principal
app = tk.Tk()
app.title("YouDownloader")
app.geometry("450x280")
app.configure(bg="#1a1a1a")

fonte = ("Segoe UI", 10)

tk.Label(app, text="Cole o link do YouTube:", bg="#1a1a1a", fg="#ffffff", font=fonte).pack(pady=(20, 5))

entrada = tk.Entry(app, width=50, font=fonte)
entrada.pack(pady=5)

btn_baixar = tk.Button(app, text="🎬 Baixar", command=mostrar_opcoes_download, width=20, bg="#4caf50", fg="white")
btn_baixar.pack(pady=10)

# Frame com botões mp3/mp4
opcoes_frame = tk.Frame(app, bg="#1a1a1a")
tk.Button(opcoes_frame, text="MP4 (Vídeo)", width=15, command=baixar_video).pack(side="left", padx=10)
tk.Button(opcoes_frame, text="MP3 (Áudio)", width=15, command=baixar_mp3).pack(side="right", padx=10)

# Status
status_var = tk.StringVar()
status_var.set("Aguardando link...")
tk.Label(app, textvariable=status_var, fg="#00ff99", bg="#1a1a1a", font=fonte).pack(pady=15)

app.mainloop()