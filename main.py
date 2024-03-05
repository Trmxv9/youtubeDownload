#                                  ,--.--------.       ,----.                        ___      ,---.               ,-.--, 
#     _..---.    ,--.-.  .-,--.   /==/,  -   , -\   ,-.--` , \   .-.,.---.    .-._ .'=.'\   .--.'  \     .--.-.  /=/, .'  
#   .' .'.-. \  /==/- / /=/_ /    \==\.-.  - ,-./  |==|-  _.-`  /==/  `   \  /==/ \|==|  |  \==\-/\ \    \==\ -\/=/- / 
#  /==/- '=' /  \==\, \/=/. /      `--`\==\- \     |==|   `.-. |==|-, .=., | |==|,|  / - |  /==/-|_\ |    \==\ `-' ,/ 
#  |==|-,   '    \==\  \/ -/            \==\_ \   /==/_ ,    / |==|   '='  / |==|  \/  , |  \==\,   - \    |==|,  - |     
#  |==|  .=. \    |==|  ,_/             |==|- |   |==|    .-'  |==|- ,   .'  |==|- ,   _ |  /==/ -   ,|   /==/   ,   \      
#  /==/- '=' ,|   \==\-, /              |==|, |   |==|_  ,`-._ |==|_  . ,'.  |==| _ /\   | /==/-  /\ - \ /==/, .--, - \               
# |==|   -   /    /==/._/               /==/ -/   /==/ ,     / /==/  /\ ,  ) /==/  / / , / \==\ _.\=\.-' \==\- \/=/ , /                           
# `-._`.___,'     `--`-`                `--`--`   `--`-----``  `--`-`--`--'  `--`./  `--`   `--`          `--`-'  `--`  



import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from pytube import YouTube
import os
import random
import string


# interface
root = tk.Tk()
root.title("TR Menus - Youtube Downloader")
root.geometry("580x200")
root.minsize(580, 200)
root.maxsize(580, 200)
root.iconbitmap("img/icon.ico")
root.resizable(0, 0)


# Using clam theme for the interface
style = ttk.Style()
style.theme_use('clam') 

# link
link = tk.StringVar()
link_label = ttk.Label(root, text="Link: ")
link_label.grid(column=0, row=0, padx=10, pady=10)
link_entry = ttk.Entry(root, textvariable=link, width=30)
link_entry.grid(column=1, row=0, padx=10, pady=10)

# select format
formato = tk.IntVar()
format_label = ttk.Label(root, text="Formato: ")
format_label.grid(column=0, row=1, padx=10, pady=10)
format_1 = ttk.Radiobutton(root, text="Video", variable=formato, value=1)
format_1.grid(column=1, row=1, padx=10)
format_2 = ttk.Radiobutton(root, text="Audio", variable=formato, value=2)
format_2.grid(column=2, row=1, padx=10)

# logs
logs = tk.Text(root, height=10, width=25)
logs.grid(column=3, row=0, rowspan=3, padx=10, pady=10)

def download():
    try:
        yt = YouTube(link.get())

        # generates random string
        def randomword(length):
            return ''.join(random.choice(string.ascii_letters + string.digits) for i in range(length))

        # create folder /downloads if not exists
        if not os.path.exists('downloads'):
            os.makedirs('downloads')

        # download video
        if formato.get() == 1:
            video = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
            if video:
                name = video.title + "_" + randomword(10) + ".mp4"
                path = os.path.join('downloads/videos', name)

                if not os.path.exists(path):
                    video.download(output_path='downloads/videos', filename=name)
                    logs.insert(tk.END, f"Download: {name} Complete!\n")
                else:
                    logs.insert(tk.END, f"File {name} already exists.\n")
            else:
                logs.insert(tk.END, "No video streams available.\n")

        # download audio
        elif formato.get() == 2:
            video = yt.streams.filter(only_audio=True).first()
            if video:
                name = video.title + "_" + randomword(10) + ".mp3"
                path = os.path.join('downloads/audios', name)

                if not os.path.exists(path):
                    video.download(output_path='downloads/audios', filename=name)
                    logs.insert(tk.END, f"Download: {name} Complete!\n")
                else:
                    logs.insert(tk.END, f"File {name} already exists.\n")
            else:
                logs.insert(tk.END, "No audio streams available.\n")

        else:
            logs.insert(tk.END, "Option not found\n")

    except Exception as e:
        logs.insert(tk.END, f"Please check your link.\n")


download_button = ttk.Button(root, text="Download", command=download)
download_button.grid(column=1, row=2, padx=10, pady=10)

root.mainloop()
