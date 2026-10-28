import tkinter as tk
from playsound3 import playsound
import random
import chat
import threading

SIZE = 500
OFFSET = 2
max_msg_size = SIZE // 2
history = []

def render_frames(parent):
    header = tk.Frame(parent, bg="#4a90e2")
    footer = tk.Frame(parent,  bg="#e290e2")
    body = tk.Frame(parent)

    header.pack(side=tk.TOP, fill=tk.X)
    footer.pack(side=tk.BOTTOM, fill=tk.X)
    body.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    entry_name = render_header(header)
    render_footer(footer, body, entry_name)

    body.bind("<Configure>", lambda event: on_resize(event))
    return body


def on_resize(event):
    global max_msg_size
    print(event.width)
    max_msg_size = int(event.width * 0.8)
    print(max_msg_size)

def render_header(parent):
    lbl_name = tk.Label(parent, text="Name:", padx=10)
    lbl_name.pack(side=tk.LEFT)
    entry_name = tk.Entry(parent)
    entry_name.pack(side=tk.LEFT)
    name = f"Kotik-{random.randint(0, 1000)}"
    entry_name.insert(0, name)
    return entry_name


def send_msg(body, entry_msg, entry_name):
    msg_text = entry_msg.get()
    name = entry_name.get()
    entry_msg.delete(0, tk.END)
    msg = f"{name}:\n{msg_text}"
    chat.send_msg(msg)
    #render_msg(body, msg)


def render_msg(parent, msg):
    lbl_msg = tk.Label(parent, text=msg,
                        padx=OFFSET, 
                        pady=OFFSET,
                        background="#92c2f2",
                        wraplength=max_msg_size)
    lbl_msg.pack(side=tk.TOP,
                anchor=tk.NE,
                pady=OFFSET,
                padx=OFFSET)
    
    history.append(lbl_msg)
    height = 0
    for msg in history:
        msg_height = msg.winfo_reqheight()
        height += (msg_height + OFFSET*2)

    while height >= parent.winfo_height():
        msg_lbl = history.pop(0)
        height -= msg_lbl.winfo_reqheight()
        msg_lbl.destroy()
        root.update_idletasks()
    sound = playsound("sounds/send_music.mp3", block=False)

def render_footer(parent, body, entry_name):
    entry_msg = tk.Entry(parent)
    entry_msg.pack(side=tk.LEFT, fill=tk.X, expand=True)
    btn_send = tk.Button(parent, text="Send",
                        command=lambda: send_msg(body, entry_msg, entry_name))
    btn_send.pack(side=tk.RIGHT)

if __name__ == '__main__':
    root = tk.Tk()
    root.geometry(f"{SIZE}x{SIZE}")
    root.title("Max")
    body = render_frames(root)
    threading.Thread(target=chat.read_msgs,
                    args=(render_msg, body),
                    daemon=True).start()
    root.mainloop()
