import string
import tkinter.ttk as ttk
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import random as rn
import hashlib
import numpy as np


# ---------------------------- libs


import LSB
import AES_cript
import steg_on_hamming


# ---------------------------- files

def randomPhrase():
    alphabet = string.ascii_letters + string.digits + string.punctuation
    phrase = ""
    for i in range(15):
        phrase += alphabet[rn.randint(0, len(alphabet) - 1)]
    return phrase


def getOrigImg():
    global img_path
    file = filedialog.askopenfile()
    if file != '':
        newImg = ImageTk.PhotoImage(Image.open(file.name))
        origImgLbl.configure(image=newImg)
        origImgLbl.image = newImg
        img_path = file.name
    else:
        print('ne')


def getEncImg():
    global img1_path
    file = filedialog.askopenfile()
    if file != '':
        newImg = ImageTk.PhotoImage(Image.open(file.name))
        encryptedImgLbl.configure(image=newImg)
        encryptedImgLbl.image = newImg
        img1_path = file.name
    else:
        print('ne')


def hideMess():
    global img_path, img1_path
    key = keyEnt.get()
    text = messTxt.get('0.0', tk.END)
    tempP = []
    img = Image.open(img_path)

    for i in np.array(img):
        for j in i:
            tempP.append(j[0])
            tempP.append(j[1])
            tempP.append(j[2])
    # print(tempP)

    raid = float(raidCbox.get())
    move = int(moveEnt.get())
    m_start = startPointEnt.get()
    m_end = endPointEnt.get()
    method = methodCbox.current()

    encText = AES_cript.encrypt(text, key)
    hashM_start = hashlib.sha256(m_start.encode('utf-8')).hexdigest()
    hashM_end = hashlib.sha256(m_end.encode('utf-8')).hexdigest()
    new_image = ""

    lengthImg = len(np.array(img)[0])
    widthImg = len(np.array(img))

    print(str(hashM_start))
    print(str(hashM_end))
    print(method)
    print(encText)

    if method == 0:
        new_image = LSB.LSB_R_enc(tempP, text, hashM_start, hashM_end, move, raid)
    elif method == 1:
        new_image = LSB.LSB_M_enc(tempP, text, hashM_start, hashM_end, move, raid)
    elif method == 2:
        new_image = steg_on_hamming.SoH_enc(tempP, text, hashM_start, hashM_end, move)
    res_img = []
    print(len(new_image))
    c1 = 0
    while c1 != len(new_image):
        rgb_pixel = []
        for q in range(3):
            rgb_pixel.append(new_image[c1])
            c1 += 1
        res_img.append(rgb_pixel)
    print('tut ', len(res_img))

    print(res_img)

    for i in range(0, len(new_image) - 1, 3):
        rgb_pixel = []
        rgb_pixel.append(new_image[i + 0])
        rgb_pixel.append(new_image[i + 1])
        rgb_pixel.append(new_image[i + 2])
        res_img.append(rgb_pixel)
    c = 0
    new_res_img = []
    for i in range(widthImg):
        q = []
        for j in range(lengthImg):
            q.append(res_img[c])
            c += 1
        new_res_img.append(q)
    # print(new_res_img)
    new_res_img = np.array(new_res_img)
    print(len(new_res_img[0]))

    mega_test_img = Image.new('RGB', (lengthImg, widthImg), "white")
    pixels = mega_test_img.load()
    print()
    for k in range(lengthImg):
        for l in range(widthImg):
            pixels[k, l] = (new_res_img[l, k][0], new_res_img[l, k][1], new_res_img[l, k][2])

    # mega_test_img.show()
    # img1_path ='M0.bmp'
    img1_path = 'pic_M' + str(method) + '_R' + str(raid) + '_S' + str(move) + '.bmp'
    mega_test_img.save(img1_path)

    newImg1 = ImageTk.PhotoImage(Image.open(img1_path))
    encryptedImgLbl.configure(image=newImg1)
    encryptedImgLbl.image = newImg1


def extractMess():
    global img1_path
    key = keyEnt.get()

    raid = float(raidCbox.get())
    m_start = startPointEnt.get()
    m_end = endPointEnt.get()
    method = methodCbox.current()

    hashM_start = hashlib.sha256(m_start.encode('utf-8')).hexdigest()
    hashM_end = hashlib.sha256(m_end.encode('utf-8')).hexdigest()

    private_text = ''
    print(method)

    img = Image.open(img1_path)
    tempP2 = []
    for i in np.array(img):
        for j in i:
            tempP2.append(j[0])
            tempP2.append(j[1])
            tempP2.append(j[2])

    if method == 0 or method == 1:
        private_text = LSB.LSB_dec(tempP2, hashM_start, hashM_end, raid)
        print('private text 0 or 1', private_text)

    elif method == 2:
        private_text = steg_on_hamming.SoH_dec(tempP2, hashM_start, hashM_end)
        print('private text 2 ', private_text)
    # text = AES_cript.decrypt(private_text, key)
    # print(text)


window = tk.Tk()
window.geometry('600x600')
window.config(bg='black')

messLbl = tk.Label(text="Скрываемое сообщение", background="#000000", foreground="#FFFFFF")
messTxt = tk.Text(width=20, height=1, background="#333333", foreground="#FFFFFF")

startPointLbl = tk.Label(text="Метка начала", background="#000000", foreground="#FFFFFF")
startPointEnt = tk.Entry(background="#333333", foreground="#FFFFFF")
startPointEnt.insert(0, randomPhrase())
keyLbl = tk.Label(text="Ключ", background="#000000", foreground="#FFFFFF")
keyEnt = tk.Entry(background="#333333", foreground="#FFFFFF")
keyEnt.insert(0, randomPhrase())
endPointLbl = tk.Label(text="Метка конца", background="#000000", foreground="#FFFFFF")
endPointEnt = tk.Entry(background="#333333", foreground="#FFFFFF")
endPointEnt.insert(0, randomPhrase())

moveLbl = tk.Label(text="Сдвиг",background="#000000", foreground="#FFFFFF")
moveEnt = tk.Entry(background="#333333", foreground="#FFFFFF")
moveEnt.insert(0, "1")

methodValues = ["LSB_R", "LSB_M", "Код Хэмминга"]
methodCbox = ttk.Combobox(values=methodValues, width=23, height=1)
methodCbox.set(methodValues[0])
raidValues = ["3", "1", "0.25", "0.27"]
raidCbox = ttk.Combobox(values=raidValues, width=29, height=1)
raidCbox.set(raidValues[0])

openOrigImgBtn = tk.Button(text="Выбрать пустой контейнер", command=getOrigImg, background="#333333", foreground="#FFFFFF")
openEncryptedImgBtn = tk.Button(text="Выбрать заполненный контейнер", command=getEncImg, background="#333333", foreground="#FFFFFF")


img_path = ''
origImgLbl = tk.Label(background="#000000", foreground="#FFFFFF")

img1_path = ''
encryptedImgLbl = tk.Label(background="#000000", foreground="#FFFFFF")

hideMessBtn = tk.Button(text="Спрятать сообщение", command=hideMess, width=22, height=1, background="#333333", foreground="#FFFFFF")
getHiddenMessBtn = tk.Button(text="Извлечь сообщение", command=extractMess, width=27, height=1, background="#333333", foreground="#FFFFFF")


messLbl.grid(row=10, column=0, padx=5, pady=2)
messTxt.grid(row=11, column=0, padx=5, pady=2)

moveLbl.grid(row=10, column=1, padx=5, pady=2)
moveEnt.grid(row=11, column=1, padx=5, pady=2)

startPointLbl.grid(row=0, column=0, padx=5, pady=2)
startPointEnt.grid(row=1, column=0, padx=5, pady=2)

keyLbl.grid(row=4, column=0, padx=5, pady=2)
keyEnt.grid(row=5, column=0, padx=5, pady=2)

endPointLbl.grid(row=8, column=0, padx=5, pady=2)
endPointEnt.grid(row=9, column=0, padx=5, pady=2)

methodCbox.grid(row=12, column=0, padx=5, pady=2)
raidCbox.grid(row=12, column=1, padx=5, pady=2)

openOrigImgBtn.grid(row=13, column=0, padx=5, pady=2)
openEncryptedImgBtn.grid(row=13, column=1, padx=5, pady=2)

hideMessBtn.grid(row=14, column=0, padx=5, pady=2)
getHiddenMessBtn.grid(row=14, column=1, padx=5, pady=2)

origImgLbl.grid(row=15, column=0, padx=5, pady=2)

encryptedImgLbl.grid(row=15, column=1, padx=5, pady=2)


window.mainloop()
