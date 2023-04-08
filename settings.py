from tkinter import *
import tkinter.messagebox

def dialogbox(main):
    #main= Tk()
    #main.title('Settings')
    #main.geometry('400x135')

    C1_check= IntVar()
    global C1_var
    C1_var=0
    C2_check= IntVar()
    global C2_var
    C2_var=0
    C3_check= IntVar()
    global C3_var
    C3_var=0

    file= open('settings.txt', 'r')
    stream= file.read()
    print(stream)
    stream_list= stream.split(',')
    file.close()

    C1_var= int(stream_list[0])
    C2_var= int(stream_list[1])
    C3_var= int(stream_list[2])

    print(C1_var, C2_var, sep='\n')

    def check1clicked():
        global C1_var
        if C1_check.get():
            C1_var=1
        else:
            C1_var=0
        print(C1_var)


    def check2clicked():
        global C2_var
        if C2_check.get():
            C2_var=1
        else:
            C2_var=0
        print(C2_var)

    def check3clicked():
        global C3_var
        if C3_check.get():
            C3_var=1
        else:
            C3_var=0
        print(C3_var)

    title= Label(main, text='Settings:', font=('Nexa-ExtraLight.ttf',18))
    C1= Checkbutton(main, text='Warn when entry is wrong', variable=C1_check, onvalue=1, offvalue=0, height=1, width=20, font=('Nexa-ExtraLight.ttf',10), command= check1clicked)
    C2= Checkbutton(main, text='Check if pencil value is correct', variable=C2_check, onvalue=1, offvalue=0, height=1, width=25, font=('Nexa-ExtraLight.ttf',10), command= check2clicked)
    C3= Checkbutton(main, text='Automatic pencil value removal', variable=C3_check, onvalue=1, offvalue=0, height=1, width=25, font=('Nexa-ExtraLight.ttf',10), command= check3clicked)


    if C1_var==1:
        C1_check.set(1)
    if C2_var==1:
        C2_check.set(1)
    if C3_var==1:
        C3_check.set(1)

    title.pack()
    C1.pack()
    C2.pack()
    C3.pack()
    main.mainloop()

    file= open('settings.txt', 'w')
    stream2= str(C1_var) + ',' + str(C2_var) +',' +str(C3_var)
    file.write(stream2)
    print(stream2)
    file.close()

def fetch():
    file= open('settings.txt','r')
    stream= file.readline()
    settings1= stream[0]
    settings2= stream[2]
    settings3= stream[4]
    file.close()
    return (settings1, settings2, settings3)

if __name__=='__main__':
    dialogbox()