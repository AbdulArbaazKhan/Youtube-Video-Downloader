from tkinter import *
from pytube import YouTube
from tkinter import ttk
from tkinter.filedialog import askdirectory


# image2 = Image.open("1.jpg")
# image2.thumbnail((200,100),Image.ANTIALIAS)
# photo = ImageTk.PhotoImage(image2)
# photo_label = Label(setting, image=photo)
# photo_label.pack(side=LEFT)
# image_url = video_details.thumbnail_url
# image1 = Image.open(requests.get(image_url, stream=True).raw)
# if os.path.exists("1.jpg"):
#     os.remove("1.jpg")
# else:
#     image1.save("1.jpg")


def video_progress(stream=None, data_chunk=None, bytes_remaining=None):
    progress_bar['value'] = ((download_video_size - bytes_remaining) / download_video_size) * 100
    root.update()


def Fetch_video():
    global list_of_formats, video_details, file_sizes, audio_file, only_video
    fetch.configure(text="Fetching...", )
    root.update()
    url = url_entry.get()

    try:
        video_details = YouTube(url, on_progress_callback=video_progress)
        all_formats = video_details.streams
        list_of_formats = all_formats.filter(progressive=True)
        audio_file = all_formats.filter(only_audio=True)
        only_video = all_formats.filter(adaptive=True).first()

        for V_quality in list_of_formats:
            try:
                file_sizes.append(round(V_quality.filesize / 1000000))
            except Exception:
                file_sizes.append("N/A")
        for A_quality in list_of_formats:
            try:
                file_sizes.append(round(A_quality.filesize / 1000000))
            except Exception:
                file_sizes.append("N/A")
        try:
            file_sizes.append(round(only_video.filesize / 1000000))
        except Exception:
            file_sizes.append("N/A")
        title['text'] = video_details.title
        fetch.configure(text="Fetch Video", )
        url_error.grid_forget()
        root.update()
        setting.pack(fill=X, pady=20, padx=2)
        if len(list_of_formats) > 1:
            p720['text'] = f"\t    720p\t\tVideo\t\t{file_sizes[0]}mb\t     mp4"
        p360['text'] = f"\t    360p\t\tVideo\t\t{file_sizes[1]}mb\t     mp4"
        audio_m4a['text'] = f"\t    144\t\taudio\t\t{file_sizes[2]}mb\t     m4a"
        audio_opus['text'] = f"\t    144\t\taudio\t\t{file_sizes[3]}mb\t     opus"
        video_only['text'] = f"\t    HD\t\tvideo only\t{file_sizes[4]}mb\t     mp4"
        options.pack(fill=BOTH, pady=10, padx=2)
        progress_bar.pack(fill=X)
        del file_sizes
    except Exception as e:
        url_error.grid(row=2, column=1, )
        fetch.config(text="Fetch Video")

    # setting2.pack(fill=BOTH,pady=2, padx=2)
    # title['text'] = video_details.title
    # fetch.grid_forget()

    # print(list_of_formats.get_lowest_resolution())
    root.update_idletasks()


def download_video():
    global progress_bar_lenght, download_video_size
    folder = askdirectory()
    if len(folder) > 0:
        fetch.config(text="Fetch Video")
        download_btn.config(text="Downloading...")
        root.update()
        if p720_status.get() == "1":
            try:
                status_var.set(f"Downloading...{video_details.title}")
                root.update()
                video = list_of_formats.filter(file_extension='mp4').get_highest_resolution()
                download_video_size = video.filesize
                video.download(folder)
                # progress_bar_lenght = video.filesize
                download_btn.config(text="Download Video")
                status_var.set(f"Your video has been downloaded at \'{folder}\'")
                root.update()
            except Exception as e:
                status_var.set("Network Error! Check your connection")
                download_btn.config(text="Download Video")
                status.config(fg="red")
        if p360_status.get() == "1":
            try:
                status_var.set(f"Downloading...{video_details.title}")
                root.update()
                video = list_of_formats.filter(file_extension='mp4').get_lowest_resolution()
                download_video_size = video.filesize
                video.download(folder)
                # progress_bar_lenght = video.filesize
                download_btn.config(text="Download Video")
                status_var.set(f"Your video has been downloaded at \'{folder}\'")
            except Exception as e:
                status_var.set("Network Error! Check your connection")
                download_btn.config(text="Download Video")
                status.config(fg="red")
        if audio_status_m4a.get() == "1":
            try:
                status_var.set(f"Downloading...{video_details.title}")
                root.update()
                video = audio_file.first()
                download_video_size = video.filesize
                video.download(folder)
                # progress_bar_lenght = video.filesize
                download_btn.config(text="Download Video")
                status_var.set(f"Your video has been downloaded at \'{folder}\'")
            except Exception as e:
                status_var.set("Network Error! Check your connection")
                download_btn.config(text="Download Video")
                download_btn.config(text="Download Video")
                status.config(fg="red")
        if audio_status_opus.get() == "1":
            try:
                status_var.set(f"Downloading...{video_details.title}")
                root.update()
                video = audio_file.last()
                download_video_size = video.filesize
                video.download(folder)
                # progress_bar_lenght = video.filesize
                download_btn.config(text="Download Video")
                status_var.set(f"Your video has been downloaded at \'{folder}\'")
            except Exception as e:
                status_var.set("Network Error! Check your connection")
                download_btn.config(text="Download Video")
                status.config(fg="red")
        if video_only_status.get() == "1":
            # try:
            status_var.set(f"Downloading...{video_details.title}")
            download_video_size = only_video.filesize
            only_video.download()
            download_btn.config(text="Download Video")
            status_var.set(f"Your video has been downloaded at \'{folder}\'")
            root.update()
            # except Exception as e:
            #     print(e)
            #     status_var.set("Network Error! Check your connection")
            #     downlaod_btn.config(text="Download Video")
            #     status.config(fg="red")
    else:
        status_var.set("Please select location where u want to save file!")
    # status_frame.pack(anchor=SW, fill=X)
    progress_bar['value'] = 0

    root.update()


# Program variables
root = Tk()
root.config(bg="#525F83")
width = 700
height = 800
root.geometry(f"{width}x{height}")
root.title("Youtube Downloader")
file_sizes = []
download_video_size = 0
video_details = None
# Title
lable_frame = Frame(root, bd=3, relief=RIDGE, bg="#525F83")
Label(lable_frame, text="Welcome To Youtube Downloader", font="timesnewroman 16 bold", bg="#525F83", ).pack(pady=20)
lable_frame.pack(fill=X, anchor="n", pady=1)

# Url Frame
url_frame = Frame(root, height=400, bd=3, relief=GROOVE, bg="#525F83")
Label(url_frame, text="Paste the link of the video: ", font="comicsansms 14 bold", bg="#525F83", fg="#39273E").grid(
    column=0, row=0, padx=8)
url_var = StringVar()
url_var.set("https://www.youtube.com/watch?v=9RTaIpVuTqE")
url_entry = Entry(url_frame, width=50, borderwidth=2, textvariable=url_var, relief=GROOVE, bg="#525F83", fg="#929BE2")
url_entry.grid(column=1, row=1, ipady=4)
url_error = Label(url_frame, text="Unable to get the video! Please enter valid link.", fg="red", bg="#FFCAA1", width=43)
fetch = Button(url_frame, text="Fetch Video", command=Fetch_video, font="timesnewroman 8 italic", relief=GROOVE, bg="#0E245D", fg="white", overrelief=RIDGE, height=1, width=10, activeforeground="#0E245D")
fetch.grid(row=3, column=1, sticky=W, pady=10, ipady=3, ipadx=3)
url_frame.pack(fill=X, anchor=N)

# Video Title
setting = Frame(root, bg="#525F83")
Label(setting, text="Choose Quality", font="comicsansms 16", bg="#525F83").pack()
Label(setting, text="Title: ", font="tiemsnewroman 17 bold", fg="black", bg="#525F83").pack(side=LEFT, padx=50)
title = Label(setting, text="", font="tiemsnewroman 10 italic", fg="#AABAAE", bg="#525F83")
title.pack(side=LEFT, )

# Resolution
options = Frame(root, bg="#525F83")
Label(options, text="Quality\t  Type\t        Size\t     Format", font="comicsansms 12 bold", padx=80, bg="#525F83").pack(anchor=W)
p720_status, p360_status, audio_status_m4a, audio_status_opus, video_only_status = StringVar(), StringVar(), StringVar(), StringVar(), StringVar()
p720_status.set(0), p360_status.set(0), audio_status_m4a.set(0), audio_status_opus.set(0), video_only_status.set(0)
p720 = Checkbutton(options, variable=p720_status, bg="#525F83", activebackground='#293656')
p720.pack(anchor=W, pady=4)
p360 = Checkbutton(options, variable=p360_status, bg="#525F83", activebackground='#293656')
p360.pack(anchor=W, pady=4)
audio_m4a = Checkbutton(options, variable=audio_status_m4a, bg="#525F83", activebackground='#293656')
audio_m4a.pack(anchor=W, pady=4)
audio_opus = Checkbutton(options, variable=audio_status_opus, bg="#525F83", activebackground='#293656')
audio_opus.pack(anchor=W, pady=4)
video_only = Checkbutton(options, variable=video_only_status, bg="#525F83", activebackground='#293656')
video_only.pack(anchor=W, pady=4)
download_btn = Button(options, text="Download Video", command=download_video, font="timesnewroman 8 italic", relief=GROOVE, bg="#0E245D", fg="white", height=2, width=14, overrelief=RIDGE, activeforeground="#0E245D")
download_btn.pack(pady=2)

# Video Status
progress_frame = Frame(root, bd=2, relief=GROOVE, bg="#525F83")
# progress_bar_lenght = 0
# print(root.clipboard_get())
progress_bar = ttk.Progressbar(progress_frame, mode="determinate", length=100, value=0, )
# progress_bar.pack(fill=X)

status_frame = Frame(root, bg="#525F83", bd=2, height=10, relief=GROOVE)
status_var = StringVar()
status_var.set("Copy and paste the link")
status = Label(status_frame, textvar=status_var, font="timesnewroman 8 italic", anchor=W, fg="white", bg="#525F83", padx=6)

status.pack(side=LEFT, )
copyR = Label(status_frame, text="Created by: Arbaz Khan\n Copyright 2021", font="timesnewroman 6 italic", anchor=E, bg="#525F83", )
copyR.pack(side=RIGHT, pady=10)
status_frame.pack(side=BOTTOM, fill=X, pady=2)
progress_frame.pack(fill=X, side=BOTTOM, padx=4)
url_entry.bind("<Button-1>", lambda event: url_var.set(url_entry.clipboard_get()))

root.mainloop()
