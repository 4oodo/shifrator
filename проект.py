import os #импортирование библиоте
from tkinter import * 
from tkinter import ttk
from tkinter import filedialog
filename = '' #имя файла
def hide():#определение функции
    global filename
    filename2 = filename[:-4] + '(mod).bmp'#Формируем новое имя файла
    sourcefile = open(filename, mode='rb')#открываем файл для чтения в пайтоне
    filesize = os.path.getsize(filename)#Определяем размер файла
    targetfile = open(filename2, mode = 'wb')#создание нового файла
    Header = 1023#Размер отступа от начала файла
    k = 0
    for i in range(0, Header):#Перенос заголовка
        x = sourcefile.read(1)
        targetfile.write(x)
        k = k + 1
    text = txt.get()#Берем текст с поля для ввода
    text = text + '@@'#стоп слово для программы
    length = len(text)#определение длинны текста
    textdata = text
    for j in range(0, length):#Нужное кол-во байт из исходного файла
        a = ord(textdata[j])
        for m in range(0, 8):#По 1 биту добавляем в новый файл
            b = a & (2**m)#проверка на подходящий для нас бит
            c = 0
            if b != 0:#если бит не 0 значит 1
                c = 1
            x = sourcefile.read(1)
            x2 = int.from_bytes(x)
            if c == 1:#выставление нужного бита
                y = x2 // 2
                y = y * 2
                y = y + 1
            if c == 0:
                t = int.from_bytes(x, byteorder="big")   
                y = t // 2
                y = y * 2
            z = y 
            targetfile.write(z.to_bytes(1, byteorder = 'big', signed = False))#Записываем измененный байт в файл
            k = k + 1
    while k < filesize:#запись хвоста файла
        x = sourcefile.read(1)
        targetfile.write(x)
        k = k + 1
    sourcefile.close()#Закрытие файла
    targetfile.close()#Закрытие файла
def fileopen():#функция для открытия файла
    global filename
    filename = filedialog.askopenfilename()#Диалог на выбор файла
def show():#Функция чтения файла
    Header = 1023#Пропуск системных символов
    global filename
    targetfile = open(filename, mode = 'rb')#Открываем файл для чтения
    for i in range(0, Header):#Чтение заголовка
        x = targetfile.read(1)
    s = 'aa'
    s1 = 'a'
    s2 = 'a'
    s3 = ''
    while s != '@@':#Чтение кода до стоп слова
        r2 = 0
        u =[0, 0, 0, 0, 0, 0, 0, 0]
        for m in range(0, 8):#Читаем 8 байт и из каждого берем по одному биту и записываем в массив
            r = targetfile.read(1)
            r = int.from_bytes(r, byteorder="big")
            r = r & 1
            u[m] = r
        r2 = 128 * u[7] + 64 * u[6] + 32 * u[5] + 16 * u[4] + 8 * u[3] + 4 * u[2] + 2 * u[1] + u[0]#Разворот битов в нужном порядке
        s1 = s2#Последний прочитанный символ становится предпоследним
        s2 = chr(r2)#Новый последний символ
        s3 = s3 + chr(r2)#Добавляем новый символ к прочитанной строке
        s = s1 + s2#Собираем 2 последних символа
    txt.insert(0, s3[:-2])#Прочитанный текст кроме двух собак записываем в окошко
    targetfile.close()#Закрытие файла#
    
window = Tk()#Создание окна
window.title("Шифратор")#Название окна
window.geometry('400x400')#Размер окна
lbl = Label(window, text="Текст:")#Создаем надпись "Текст"
lbl.grid(column=0, row=0)#где будет расположен
open_button = ttk.Button(text="Открыть файл", command=fileopen)#Создаем кнопку "открыть файл"
open_button.grid(column=0, row=1, sticky=NSEW, padx=10)#Расположение
hide_button = ttk.Button(text="Спрятать", command=hide)#Создаем кнопку "Спрятать"
hide_button.grid(column=0, row=2, sticky=NSEW, padx=10)#Расположение
show_button = ttk.Button(text="Показать", command=show)#Создаем кнопку "Показать"
show_button.grid(column=0, row=3, sticky=NSEW, padx=10)#Расположение
txt = Entry(window, width=30)#Создание окна для текста
txt.grid(column=1, row=0)#Расположение
txt.focus()#Чтобы курсор стоял сразу в поле для текста

window.mainloop()

