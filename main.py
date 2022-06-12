#!/usr/bin/python

# -*- coding: utf8 -*-
n = 0

import tkinter as tk
from tkinter.ttk import Radiobutton
from tkinter.ttk import Combobox
from tkinter.ttk import Progressbar
import time
import keyboard

from tkinter import messagebox
import random



# the section with logic operations

def toFixed(numObj, digits=2): # fixed number of digits after dot
    return f"{numObj:.{digits}f}"

def check(num1, num2, num3, bit): # checks if the result and variables fit into the chosen type
    if bit == 1:
        if num1 <= 32767 and num1 >= - 32768 and num2 <= 32767 and num2 >= - 32768 and num3 <= 32767 and num3 >= - 32768:
            return True
        else:
            return False
    if bit == 2:
        if num1 <= 2147483647 and num1 >= -2147483648 and num2 <= 2147483647 and num2 >= -2147483648 and num3 <= 2147483647 and num3 >= -2147483648:
            return True
        else:
            return False
    if bit == 3:
        if num1 < 2 ** 63 and num1 >= -2 ** 63 and num2 <= 2 ** 63 and num2 >= -2 ** 63 and num3 <= 2 ** 63 and num3 >= -2 ** 63:
            return True
        else:
            return False
    if bit == 4:
        return True
    if bit == 5:
        return True


def float_to_binary(num, mod): # float number to its binary appearance
    exponent = 0
    shifted_num = num
    while shifted_num != int(shifted_num):
        shifted_num *= 2
        exponent += 1
    if exponent == 0:
        return '{0:0b}'.format(int(shifted_num))
    binary = '{0:0{1}b}'.format(int(shifted_num), exponent + 1)
    integer_part = binary[:-exponent]
    fractional_part = binary[-exponent:].rstrip('0')
    if mod == 1:
        return '{0}.{1}'.format(integer_part, fractional_part)
    else:
        return '{0}{1}'.format(integer_part, fractional_part)



def gener(): # random generating of the entrance parametres
    entry1.delete(0, 'end')
    entry2.delete(0, 'end')

    L = [8, 16, 32, 64]
    i = random.randint(0, 3)
    combo.set(L[i])
    i = random.randint(1, 5)
    selected.set(i)
    if i <= 3:
        num1 = random.randint(-18000, 30000)
        num2 = random.randint(-18000, 30000)
        entry1.insert(0, str(num1))
        entry2.insert(0, str(num2))
    else:
        num1 = random.uniform(-18000, 30000)
        num2 = random.uniform(-18000, 30000)
        entry1.insert(0, str(toFixed(num1)))
        entry2.insert(0, str(toFixed(num2)))
    i = random.randint(1, 2)
    oper.set(i)


def modify(s, bit): # enters the spaces between "bytes"
    s1 = ''
    for i in range(len(s)):
        if i % 8 == 0:
            s1 += ' '
            s1 += s[i]
        else:
            s1 += s[i]
    return s1


def inverse_to_registr(s, bit): # changes the bytes order (like in real register)
    s1 = ''

    for i in range((bit // 8) - 1, -1, -1):
        for j in range(0, 8):
            s1 += s[i * 8 + j]

    return s1


def floa(num1, num2, num3): # converts the binary float number to register appereance
    L = [num1, num2, num3]
    A = []
    for h in L:
        ans = ''
        s = float_to_binary(h, 1)
        tmp = float_to_binary(h, 0)
        if s[0] == '-':
            s = s[1:]
            tmp = tmp[1:]
        if s[0] == '.':
            s = '0' + s
            tmp = '0' + tmp
        if s[0] == '0':
            k = s.find('1') - 1
            k = -k
            tmp = tmp[s.find('1'):s.find('1') + 23]
        else:
            k = s.find('.') - 1
            tmp = tmp[1:24]
            if s.find('.') == -1:
                k = len(s) - 1

        if h < 0:
            bit = '1'
        else:
            bit = '0'

        por = str(bin(k + 127))[2:]
        if len(por) < 8:
            por = '0' * (8 - len(por)) + por

        ans = bit + por + tmp
        if len(ans) < 32:
            ans += '0' * (32 - len(ans))
        A.append(ans)
    draw_register(A[0], A[1], A[2], 32)


def doub(num1, num2, num3): # converts the binary double number to register appereance
    L = [num1, num2, num3]
    A = []
    for h in L:
        ans = ''
        s = float_to_binary(h, 1)
        tmp = float_to_binary(h, 0)
        if s[0] == '-':
            s = s[1:]
            tmp = tmp[1:]
        if s[0] == '.':
            s = '0' + s
            tmp = '0' + tmp
        if s[0] == '0':
            k = s.find('1') - 1
            k = -k
            tmp = tmp[s.find('1'):s.find('1') + 51]
        else:
            k = s.find('.') - 1
            tmp = tmp[1:52]
            if s.find('.') == -1:
                k = len(s) - 1

        if h < 0:
            bit = '1'
        else:
            bit = '0'

        por = str(bin(k + 1023))[2:]

        if len(por) < 11:
            por = '0' * (11 - len(por)) + por

        ans = bit + por + tmp
        if len(ans) < 64:
            ans += '0' * (64 - len(ans))
        A.append(ans)
    draw_register(A[0], A[1], A[2], 64)


def change(num, bit): # converts the int number to its binary appearence
    if num >= 0: # for positive numbers
        num = str(bin(int(num)))[2:]
        if len(num) < bit:
            num = '0' * (bit - len(num)) + num
    else: # for negative
        s = str(bin(abs(num) - 1))
        if len(s) < bit:
            s = '0' * (bit - len(s)) + s
        num = ''
        for i in range(len(s)):
            if s[i] == '1':
                num += '0'
            else:
                num += '1'

    return (num)


def check_int(n): # checks if n is int
    if n == int(n):
        return True
    else:
        messagebox.showerror("Ошибка", "Введите корректные значения")
        return False


def clicked_to_dr(): # this function will be executed after pressing Start button
    num1 = float(entry1.get())
    num2 = float(entry2.get())

    if oper.get() == 1:
        num3 = num1 + num2
    else:
        num3 = num1 - num2

    f = selected.get() # the type of the numbers
    if not check(num1, num2, num3, f):
        messagebox.showerror("Ошибка", "Переполнение типа!")
        return

    if f == 1:
        param = 16
    if f == 2:
        param = 32
    if f == 3:
        param = 64

    if (f == 1 or f == 2 or f == 3) and check_int(num1) and check_int(num2):
        draw_register(change(int(num1), param), change(int(num2), param), change(int(num3), param), param)

    if f == 4:
        floa(num1, num2, num3)
    if f == 5:
        doub(num1, num2, num3)




















def help():
    messagebox.showinfo('Справка',
                        'В начале работы пользователь может установить свои параметры проводимового моделирования.\n'
                        'Обратите внимание! Если выбран целочисленный тип данных и введено дробное значение, это приведет к ошибке\n'

                        'Программа имеет 2 режима работы: автоматический и ручной. \n'
                        'В автоматическом режиме после нажатия кнопки "Старт" программа сама воссоздаст процесс записи чисел в регистры процессора\n'
                        'В ручном режиме каждому такту процессора соответствует нажатие пользователем кнопки "Enter"\n'
                        'Программа имеет функцию автоматической генерации входных данных')


def draw_res(s, bit, f, registr): # draws the result in 'registers'
    if bit == 8:
        for i in range(bit // 8):
            for j in range(0, 8):
                if f % 2:
                    label1 = tk.Label(master=registr, text=f"{s[i * 8 + j]}", bg="#C0C0C0")
                    label1.grid(row=0, column=i * 8 + j + f * bit)
                else:
                    label1 = tk.Label(master=registr, text=f"{s[i * 8 + j]}", bg="#DCDCDC")
                    label1.grid(row=0, column=i * 8 + j + f * bit)

    else:

        for i in range(bit // 8):
            for j in range(0, 8):
                if i % 2:
                    label1 = tk.Label(master=registr, text=f"{s[i * 8 + j]}", bg="#C0C0C0")
                    label1.grid(row=0, column=i * 8 + j + f * bit)
                else:
                    label1 = tk.Label(master=registr, text=f"{s[i * 8 + j]}", bg="#DCDCDC")
                    label1.grid(row=0, column=i * 8 + j + f * bit)


def draw_empty(bit, registr): # draws empty registers
    for i in range(bit // 8):
        for j in range(0, 8):
            if i % 2:
                label1 = tk.Label(master=registr, text=f"  ", bg="#C0C0C0")
                label1.grid(row=0, column=i * 8 + j)
            else:
                label1 = tk.Label(master=registr, text=f"  ", bg="#DCDCDC")
                label1.grid(row=0, column=i * 8 + j)


def draw_register(s1, s2, s3, bit): # draws the full animation and all the registers
    global n
    n += 1

    if n == 1:
        label1 = tk.Label(master=frame42, text=f"Представление результата в регистре")
        label1.pack()

    toclean = [registr1, registr2, registr3, frame02, frame22, frame62, frame72, frame82]

    for i in toclean:
        y = i.winfo_children()
        for w in y:
            w.destroy()

    label1 = tk.Label(master=frame02, text=f"   Представление 1 числа в двоичном коде:")
    label1.grid(row=0, column=0)

    label1 = tk.Label(master=frame02, text=f"Представление 1 числа в регистре:")
    label1.grid(row=2, column=0)

    label1 = tk.Label(master=frame22, text=f"\nПредставление 2 числа в двоичном коде:\n")
    label1.grid(row=0, column=0)

    label1 = tk.Label(master=frame22, text=f"Представление 2 числа в регистре:")
    label1.grid(row=2, column=0)

    label1 = tk.Label(master=frame02, text=f"{modify(s1, bit)}")
    label1.grid(row=1, column=0)

    label1 = tk.Label(master=frame22, text=f"{modify(s2, bit)}")
    label1.grid(row=1, column=0)

    time.sleep(2)
    window.update()

    razr = int(combo.get())
    f = bit // razr
    if razr > bit:
        f = 1

    draw_empty(bit, registr1)
    draw_empty(bit, registr2)
    draw_empty(bit, registr3)

    d = inverse_to_registr(s1, bit)

    time.sleep(1)
    window.update()

    for t in range(f):
        y = frame62.winfo_children()
        for w in y:
            w.destroy()
        label1 = tk.Label(master=frame62, text=f"\nЗапись числа в 1 регистр...\n", bg='red')
        label1.pack()

        if sel.get() == 1:
            keyboard.wait('return')
            draw_res(d[t * razr:(t + 1) * razr], min(razr, bit), t, registr1)
        if sel.get() == 2:
            draw_res(d[t * razr:(t + 1) * razr], min(razr, bit), t, registr1)
            time.sleep(0.5)

        bar = Progressbar(master=frame62)
        bar['value'] = (t + 1) * (100 / f)
        bar.pack()
        window.update()
    y = frame62.winfo_children()
    for w in y:
        w.destroy()
    label1 = tk.Label(master=frame62, text=f"\n1 число записано в регистр\n")
    label1.pack()

    time.sleep(1)
    window.update()

    d = inverse_to_registr(s2, bit)

    for t in range(f):

        y = frame72.winfo_children()
        for w in y:
            w.destroy()
        label1 = tk.Label(master=frame72, text=f"\nЗапись числа во 2 регистр...\n", bg='red')
        label1.pack()
        if sel.get() == 1:
            keyboard.wait('return')
            draw_res(d[t * razr:(t + 1) * razr], min(razr, bit), t, registr2)
        if sel.get() == 2:
            draw_res(d[t * razr:(t + 1) * razr], min(razr, bit), t, registr2)
            time.sleep(0.5)

        bar = Progressbar(master=frame72)
        bar['value'] = (t + 1) * (100 / f)
        bar.pack()
        window.update()
    y = frame72.winfo_children()
    for w in y:
        w.destroy()
    label1 = tk.Label(master=frame72, text=f"\n2 число записано в регистр\n")
    label1.pack()

    d = inverse_to_registr(s3, bit)

    time.sleep(1)
    window.update()

    for t in range(f):

        y = frame82.winfo_children()
        for w in y:
            w.destroy()

        label1 = tk.Label(master=frame82, text=f"\nВыполнение операции...\nЗапись результата в регистр...\n", bg='red')
        label1.pack()
        if sel.get() == 1:
            keyboard.wait('return')
            draw_res(d[t * razr:(t + 1) * razr], min(razr, bit), t, registr3)
        if sel.get() == 2:
            draw_res(d[t * razr:(t + 1) * razr], min(razr, bit), t, registr3)
            time.sleep(0.5)

        bar = Progressbar(master=frame82)
        bar['value'] = (t + 1) * (100 / f)
        bar.pack()
        window.update()
    y = frame82.winfo_children()
    for w in y:
        w.destroy()
    label1 = tk.Label(master=frame82, text=f"\nРезультат записан в регистр\n")
    label1.pack()
    window.update()

    # результат в двоичном коде, внутреннем представлении и внешнем прелставлении
    time.sleep(2)

    y = frame62.winfo_children()
    for w in y:
        w.destroy()

    y = frame72.winfo_children()
    for w in y:
        w.destroy()

    y = frame82.winfo_children()
    for w in y:
        w.destroy()

    window.update()

    if selected.get() <= 3:
        num1 = int(entry1.get())
        num2 = int(entry2.get())
    else:
        num1 = float(entry1.get())
        num2 = float(entry2.get())

    if oper.get() == 1:
        num3 = num1 + num2
    else:
        num3 = num1 - num2

    label1 = tk.Label(master=frame62,
                      text=f"\nРезультат операции в двоичном коде:\n\n{modify(s3, bit)}\n\nРезультат операции во внешнем представлении:\n\n{num3}")
    label1.pack()



window = tk.Tk()
window.title("Эмулятор процессора для сложения и вычитания чисел")
window.state('zoomed')
main_menu = tk.Menu()
main_menu.add_cascade(label="Справка", command=help)

window.config(menu=main_menu)

frame00 = tk.Frame(
    master=window,
    height=70, width=70,
    borderwidth=20
)
frame00.grid(row=0, column=0)

frame01 = tk.Frame(
    master=window,
    relief=tk.RAISED,
    borderwidth=0
)
frame01.grid(row=0, column=1)

frame02 = tk.Frame(
    master=window,
    relief=tk.RAISED,
    borderwidth=0
)
frame02.grid(row=0, column=2)

registr1 = tk.Frame(
    master=window,
    relief=tk.RAISED,
    borderwidth=0
)
registr1.grid(row=1, column=2)

frame11 = tk.Frame(
    master=window,
    relief=tk.RAISED,
    borderwidth=0
)
frame11.grid(row=1, column=1)

frame12 = tk.Frame(
    master=window,
    relief=tk.RAISED,
    borderwidth=0
)
frame12.grid(row=1, column=2)

frame20 = tk.Frame(
    master=window,
    relief=tk.RAISED,
    borderwidth=0
)
frame20.grid(row=2, column=0)

frame21 = tk.Frame(
    master=window,
    relief=tk.RAISED,
    borderwidth=0
)
frame21.grid(row=2, column=1)

frame22 = tk.Frame(
    master=window,
    relief=tk.RAISED,
    borderwidth=0
)
frame22.grid(row=2, column=2)

registr2 = tk.Frame(
    master=window,
    relief=tk.RAISED,
    borderwidth=0
)
registr2.grid(row=3, column=2)

frame32 = tk.Frame(
    master=window,
    relief=tk.RAISED,
    borderwidth=0
)
frame32.grid(row=3, column=2)

frame40 = tk.Frame(
    master=window,
    relief=tk.RAISED,
    borderwidth=0
)
frame40.grid(row=4, column=0)

frame42 = tk.Frame(
    master=window,
    relief=tk.RAISED,
    borderwidth=0
)
frame42.grid(row=4, column=2)

registr3 = tk.Frame(
    master=window,
    relief=tk.RAISED,
    borderwidth=0
)
registr3.grid(row=5, column=2)

frame52 = tk.Frame(
    master=window,
    relief=tk.RAISED,
    borderwidth=0
)
frame52.grid(row=5, column=2)

frame60 = tk.Frame(
    master=window,
    relief=tk.RAISED,
    borderwidth=0
)
frame60.grid(row=6, column=0)

frame61 = tk.Frame(
    master=window,
    relief=tk.RAISED,
    borderwidth=0
)
frame61.grid(row=6, column=1)

frame62 = tk.Frame(
    master=window,
    relief=tk.RAISED,
    borderwidth=0
)
frame62.grid(row=6, column=2)

frame70 = tk.Frame(
    master=window,
    relief=tk.RAISED,
    borderwidth=0
)
frame70.grid(row=7, column=0)

frame71 = tk.Frame(
    master=window,
    relief=tk.RAISED,
    borderwidth=0
)
frame71.grid(row=7, column=1)

frame72 = tk.Frame(
    master=window,
    relief=tk.RAISED,
    borderwidth=0
)
frame72.grid(row=7, column=2)

frame80 = tk.Frame(
    master=window,
    relief=tk.RAISED,
    borderwidth=0
)
frame80.grid(row=8, column=0)

frame82 = tk.Frame(
    master=window,
    relief=tk.RAISED,
    borderwidth=0
)
frame82.grid(row=8, column=2)

frame90 = tk.Frame(
    master=window,
    relief=tk.RAISED,
    borderwidth=0
)
frame90.grid(row=9, column=0)

frame91 = tk.Frame(
    master=window,
    relief=tk.RAISED,
    borderwidth=0
)
frame91.grid(row=9, column=1)

frame92 = tk.Frame(
    master=window,
    relief=tk.RAISED,
    borderwidth=0
)
frame92.grid(row=9, column=2)

frame102 = tk.Frame(
    master=window,
    relief=tk.RAISED,
    borderwidth=0
)
frame102.grid(row=10, column=2)

# customer's parametres

label2 = tk.Label(master=frame00, text=f"Разрядность процессора")
label2.grid(column=0, row=0)

# CPU
combo = Combobox(master=frame00, width=5)
combo['values'] = (8, 16, 32, 64)
combo.current(0)
combo.grid(column=0, row=1)

# number type
label3 = tk.Label(master=frame20, text=f"Тип числовых значений")
label3.grid(column=0, row=0)

selected = tk.IntVar()
selected.set(1)
rad1 = Radiobutton(frame20, text='short', value=1, variable=selected)
rad2 = Radiobutton(frame20, text='int', value=2, variable=selected)
rad3 = Radiobutton(frame20, text='long', value=3, variable=selected)
rad4 = Radiobutton(frame20, text='float', value=4, variable=selected)
rad5 = Radiobutton(frame20, text='double', value=5, variable=selected)
rad1.grid(column=0, row=1)
rad2.grid(column=0, row=2)
rad3.grid(column=0, row=3)
rad4.grid(column=0, row=4)
rad5.grid(column=0, row=5)

# mode

label4 = tk.Label(master=frame40, text=f"Режим работы")
label4.grid(column=0, row=0)

sel = tk.IntVar()
sel.set(1)
rad1 = Radiobutton(frame40, text='Ручной', value=1, variable=sel)
rad2 = Radiobutton(frame40, text='Автоматический', value=2, variable=sel)
rad1.grid(column=0, row=1)
rad2.grid(column=0, row=2)

# Operands

label5 = tk.Label(master=frame60, text=f"\n")
label5.grid(column=0, row=0)
label5 = tk.Label(master=frame60, text=f"\n")
label5.grid(column=1, row=0)
label5 = tk.Label(master=frame60, text=f"1 число")
label5.grid(column=0, row=1)
label5 = tk.Label(master=frame60, text=f"\n2 число\n")
label5.grid(column=0, row=2)

entry1 = tk.Entry(master=frame60, width=15)
entry2 = tk.Entry(master=frame60, width=15)
entry1.grid(column=1, row=1)
entry2.grid(column=1, row=2)

# Operation

label5 = tk.Label(master=frame70, text=f"\nОперация:")
label5.grid(column=0, row=0)

oper = tk.IntVar()
oper.set(1)
rad1 = Radiobutton(frame70, text='Сложить', value=1, variable=oper)
rad2 = Radiobutton(frame70, text='Вычесть', value=2, variable=oper)
rad1.grid(column=0, row=1)
rad2.grid(column=0, row=2)

label5 = tk.Label(master=frame80, text=f"\n")
label5.grid(column=0, row=0)
draw = tk.Button(master=frame80, text="Автоматическая\nгенерация\nзначений", command=gener, relief='ridge')
draw.grid(column=0, row=1)

draw = tk.Button(master=frame80, text="Старт", command=clicked_to_dr)
draw.grid(column=0, row=2)
label5 = tk.Label(master=frame80, text=f"\n")
label5.grid(column=0, row=3)

window.mainloop()