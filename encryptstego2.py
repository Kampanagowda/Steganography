from tkinter import *
from ctypes import windll
from tkinter import filedialog, messagebox
from PIL import ImageTk, Image
import encode
import decode


encode_opened = False
decode_opened = False
help_opened = False

file_path = ""


##########################################################
# ENCODE WINDOW COMPONENTS
##########################################################
# function to open a new window for encoding functionality
def open_encode_window():
   
    global encode_opened
    
    if not encode_opened:
        encode_window = Toplevel(window)
        encode_window.title("Encryptstego - Encode")
        
        encode_window.geometry('800x500')
        
        encode_window.resizable(False, False)
        
        encode_window.transient(window)

        if windows:
            windll.shcore.SetProcessDpiAwareness(1)

       
        raw_image_label = Label(encode_window, text="Select Raw Image", height=20, width=50, relief="solid",
                                bg="#FFFFFF")
       
        raw_image_label.place(x=20, y=20)

       
        text_to_encode_label = Label(encode_window, text="Text to Encode")
        text_to_encode_label.config(font=("Open Sans", 12))
        text_to_encode_label.place(x=400, y=20)

       
        text_to_encode = Text(encode_window, height=7, width=34)
        text_to_encode.config(relief="solid", font=("Open Sans", 15))
        text_to_encode.place(x=400, y=51)

       
        pass_to_encode_label = Label(encode_window, text="Password")
        pass_to_encode_label.config(font=("Open Sans", 12))
        pass_to_encode_label.place(x=400, y=262)

        
        pass_to_encode = Entry(encode_window, width=34)
        pass_to_encode.config(relief="solid", font=("Open Sans", 15), show="*")
        pass_to_encode.place(x=400, y=293)

       
        
        browse_image_btn = Button(encode_window, text="Browse Raw Image", width=29, cursor="hand2",
                                  command=lambda: browse_image(raw_image_label))
        browse_image_btn.config(font=("Open Sans", 15), bg="#36923B", fg="white", borderwidth=0)
        browse_image_btn.place(x=20, y=350)

        
        
        encode_image_btn = Button(encode_window, text="Encode", width=15, cursor="hand2",
                                  command=lambda: encode_image(file_path, pass_to_encode.get(),
                                                               text_to_encode.get("1.0", END)))
        encode_image_btn.config(font=("Open Sans", 15), bg="#503066", fg="white", borderwidth=0)
        encode_image_btn.place(x=592, y=420)

        
        encode_opened = True
        
        encode_window.protocol("WM_DELETE_WINDOW", lambda: close_encode_window(encode_window))



def save_image(stego_image):
   
    save_path = filedialog.asksaveasfile(initialfile="encryptstego.png", mode="wb", defaultextension=".png",
                                         filetypes=(("Image File", "*.png"), ("All Files", "*.*")))
   
    stego_image.save(save_path)



def encode_image(image_path, password, text_to_encode):
   
    encode_action = encode.Encode(image_path, password, text_to_encode)
    
    msg = encode_action.are_values_valid()
   
    if not msg[1]:
        
        messagebox.showerror("Error Encoding", msg[0])
    else:
        
        stego_image = encode_action.encode_into_image()
        
        if stego_image[1]:
           
            if save_image(stego_image[0]) is None:
                messagebox.showinfo("Image Saved", "Encode operation was successful.")
        else:
           
            messagebox.showerror("Error Encoding", stego_image[0])


##########################################################
# DECODE WINDOW COMPONENTS
##########################################################

def open_decode_window():
   
    global decode_opened
    if not decode_opened:
        decode_window = Toplevel(window)
        decode_window.title("Encryptstego - Decode")
        decode_window.geometry('800x500')
        decode_window.resizable(False, False)
        decode_window.transient(window)

        if windows:
            windll.shcore.SetProcessDpiAwareness(1)

        stego_image_label = Label(decode_window, text="Select Stego Image", height=20, width=50, relief="solid",
                                  bg="#FFFFFF")
        stego_image_label.place(x=20, y=20)

        text_to_decode_label = Label(decode_window, text="Decoded Text")
        text_to_decode_label.config(font=("Open Sans", 12))
        text_to_decode_label.place(x=400, y=20)

        text_to_decode = Text(decode_window, height=7, width=34)
        text_to_decode.config(relief="solid", font=("Open Sans", 15), state=DISABLED)
        text_to_decode.place(x=400, y=51)

        pass_to_decode_label = Label(decode_window, text="Password")
        pass_to_decode_label.config(font=("Open Sans", 12))
        pass_to_decode_label.place(x=400, y=262)

        pass_to_decode = Entry(decode_window, width=34)
        pass_to_decode.config(relief="solid", font=("Open Sans", 15), show="*")
        pass_to_decode.place(x=400, y=293)

        browse_stego_btn = Button(decode_window, text="Browse Stego Image", width=29, cursor="hand2",
                                  command=lambda: browse_image(stego_image_label))
        browse_stego_btn.config(font=("Open Sans", 15), bg="#503066", fg="white", borderwidth=0)
        browse_stego_btn.place(x=20, y=350)

        decode_stego_btn = Button(decode_window, text="Decode", width=15, cursor="hand2",
                                  command=lambda: decode_image(file_path, pass_to_decode.get(), text_to_decode))
        decode_stego_btn.config(font=("Open Sans", 15), bg="#36923B", fg="white", borderwidth=0)
        decode_stego_btn.place(x=592, y=420)

        decode_opened = True
        decode_window.protocol("WM_DELETE_WINDOW", lambda: close_decode_window(decode_window))


def decode_image(image_path, password, text_field):
    decode_action = decode.Decode(image_path, password)
    msg = decode_action.are_values_valid()
    if not msg[1]:
        messagebox.showerror("Error Decoding", msg[0])
    else:
        decoded_text = decode_action.decode_from_image()
        if decoded_text[1]:
            text_field.config(state=NORMAL)
            text_field.delete(1.0, END)
            text_field.insert(1.0, decoded_text[0])
            text_field.config(state=DISABLED)
            messagebox.showinfo("Text Decoded", "Decode operation was successful.")
        else:
            messagebox.showerror("Error Decoding", decoded_text[0])


##########################################################
# COMMON COMPONENTS
##########################################################
def browse_image(image_frame):
    global file_path
    file_path = filedialog.askopenfilename(title="Choose an Image",
                                           filetypes=(("Image Files", "*.png"), ("All Files", "*.*")))
    selected_image = Image.open(file_path)
    max_width = 350
    aspect_ratio = max_width / float(selected_image.size[0])
    max_height = int((float(selected_image.size[1]) * float(aspect_ratio)))
    selected_image = selected_image.resize((max_width, max_height), Image.ANTIALIAS)
    selected_image = ImageTk.PhotoImage(selected_image)
    image_frame.config(image=selected_image, height=304, width=354)
    image_frame.image = selected_image


##########################################################
# MAIN WINDOW COMPONENTS
##########################################################
def close_encode_window(encode_window):
    global encode_opened
    encode_window.destroy()
    encode_opened = False


def close_help_window(help_window):
    global help_opened
    help_window.destroy()
    help_opened = False


def close_decode_window(decode_window):
    global decode_opened
    decode_window.destroy()
    decode_opened = False


def help_menu():
    global help_opened
    if not help_opened:
        help_window = Toplevel(window)
        # Setting title of the help window
        help_window.title("Help")
        # Setting the size of the help window
        help_window.geometry('500x420')
        help_window.resizable(False, False)
        help_window.transient(window)
        # windll is Windows OS specific
        if windows:
            windll.shcore.SetProcessDpiAwareness(1)

        # Label to indicate textarea to display title text
        text_to_decode_label = Label(help_window, text="\nEncryptstego v1.0\nDeveloped by @iamsubingyawali")
        text_to_decode_label.config(font=("Open Sans", 12))
        text_to_decode_label.pack()

        # Label to indicate textarea to display help text
        text_to_decode_label = Label(help_window,
                                     text="Encryptstego is an Image Steganography tool "
                                          "used to embed text messages into an Image. The "
                                          "embedded text is encrypted using the password."
                                          "\n\nTo encode the message into an image, click on Encode"
                                          " and select an Image. Choose a password and the text to embed."
                                          " Then click Encode to embed and save your image with message."
                                          "\n\nTo decode the message from an encoded image, click Decode and select"
                                          " the encoded image, provide the password used to encode and click Decode."
                                          " Your decoded message will be displayed on the window. If the provided "
                                          "password is incorrect, message can never be extracted.")
        text_to_decode_label.config(font=("Open Sans", 12),  justify="left", wraplength=450)
        text_to_decode_label.pack(padx=20, pady=20)

        help_opened = True
        help_window.protocol("WM_DELETE_WINDOW", lambda: close_help_window(help_window))


window = Tk()
window.title("Encryptstego")
window.geometry('800x500')
window.resizable(False, False)
# windll is Windows OS specific
if windows:
    windll.shcore.SetProcessDpiAwareness(1)

logo = Image.open("../images/logo.png")
logo = logo.resize((100, 100), Image.ANTIALIAS)
logo = ImageTk.PhotoImage(logo)
window.iconphoto(True, logo)

image_label = Label(window, image=logo, height=100, width=100)
# Packing the label on the window
image_label.pack(pady=20)

title_label = Label(window, text="Encryptstego")
title_label.pack()
title_label.config(font=("Open Sans", 32))

encode_btn = Button(window, text="Encode", height=2, width=15, bg="#503066", fg="white", cursor="hand2", borderwidth=0,
                    command=open_encode_window)
encode_btn.config(font=("Open Sans", 15, "bold"))
encode_btn.pack(side=LEFT, padx=50)

decode_btn = Button(window, text="Decode", height=2, width=15, bg="#36923B", fg="white", cursor="hand2", borderwidth=0,
                    command=open_decode_window)
decode_btn.config(font=("Open Sans", 15, "bold"))
decode_btn.pack(side=RIGHT, padx=50)

footer_label = Label(window, text="Subin Gyawali")
footer_label.pack(side=BOTTOM, pady=20)

menu = Menu(window)
# Adding help menu
menu.add_command(label="Help", command=help_menu)
window.config(menu=menu)

window.mainloop()
