import tkinter as tk
import fuzzy_script
from fuzzy_script import interpreter
import datetime 
import time 
from PIL import ImageTk, Image
import os 
import json 
import pathlib 
import pathlib

def file_name():
    x = os.path.realpath(__file__)
    print(x)
    y = x.split("\\")
    print(y)
    y_ = y[len(y)-1].split('.py')
    print(y_[0])
    return y_[0]


p = pathlib.Path(__file__).parent.absolute()
z = str(p).split('/')

z[0].replace("\\","//")


window = tk.Tk()
window.title('Cerberus IDE')
photo = ImageTk.PhotoImage(Image.open(str(z[0]+str('/icon_cloud_2.jpg'))))
window.iconphoto(False,photo)

global console_log 
console_log = []

global path_list 
path_list = []

try:
    main_path = str(z[0]+str('/path_in.json'))
    path_unique = json.load(open(main_path,encoding='utf-8'))
    with open(main_path) as JsonFile:
        root = json.load(JsonFile)

    path_label_main = tk.Label(
        master=window,
        background='black',
        fg='lime',
        width="68",
        text='{x}.py'.format(x=root['path'])
    )
except:
    path_label_main = tk.Label(
        master=window,
        background='black',
        fg='lime',
        width="68"
    )

# here the sets will be plotted

def plot_window():

    p_window = tk.Tk()
    p_window.title('Plot window')
    p_window.config(background="black")

    c = tk.Canvas(master=p_window)
    
    c.grid()
    p_window.mainloop()

def config_window():

    c_window = tk.Tk()
    c_window.title('config')

    path = tk.Entry(
        master=c_window,
        width=36,
        bg='black',
        fg='lime'
    )
    try:
        path_label = tk.Label(
            master=c_window,
            bg='black',
            fg='lime',
            width=30,
            text=path_list[len(path_list)-1]
        )
    except:
        path_label = tk.Label(
            master=c_window,
            bg='black',
            fg='lime',
            width=30
        )

    def path_choose():
        pa = path.get()
        main_path = str(z[0]+str('/path_in.json'))
        path_unique = json.load(open(main_path,encoding='utf-8'))
        with open(main_path) as JsonFile:
            root = json.load(JsonFile)
        root['path'] = pa  
        with open(main_path,'w') as JsonFile:
            json.dump(root,JsonFile)

        path_list.append(pa)
        path_label['text'] = '{x}.py'.format(x=path_list[len(path_list)-1])
        path_label_main['text'] = '{x}.py'.format(x=path_list[len(path_list)-1])

    btn_0 = tk.Button(
        master=c_window,
        width=30,
        text='choose',
        bg='black',
        fg='lime',
        command=path_choose
    )

   
    path.grid()
    btn_0.grid()
    path_label.grid()
    c_window.mainloop()
    return 

# configuration button #
btn_config = tk.Button(
    master=window,
    background='grey',
    width="67",
    text="config",
    command=config_window)

# text editor # 
editor = tk.Text(
    master=window,
    background="MediumPurple1",
    fg="black",
    font=('Times new romans',8,'bold')
)

#editor.insert('0.0','\nstart_cloud{ \n}end_cloud\n')
#editor.insert('0.0','custom::={ \n}end_custom\n')

# here the textual results will be written 
console = tk.Text(
    master=window,
    background="MediumPurple2",
    fg="black",
    font=("Times new romans",8,'bold'),
    height="13",

    
)

def intepreter_run_now():

    try:
        e = editor.get(0.0,'end')
        t0 = time.time() 
        try:
            main_path = str(z[0]+str('/path_in.json'))
            path_unique = json.load(open(main_path,encoding='utf-8'))
           str(e),w i = interpreter.run(indow,[1,2],path=path_unique['path'])
        except:
            i = interpreter.run(str(e),window,[1,2],path=path_list[len(path_list)-1])

        t1 = time.time()
        console_log.append(i)
        log = 'Date:{t}, running time:{r} seconds'.format(t=str(datetime.date.today()),r=round(t1-t0,3))
        console.insert('end','\n'+log)

        if type(i) is list:
            counter = 0
            for result in i :
                if counter == len(i)-1:
                    console.insert('end','\n'+'>> '+str(result))
                    console.insert('end','\n'+'finished<<')
                else:
                    console.insert('end','\n'+'>> '+str(result))
                counter+=1
        else:
            console.insert('end','\n'+'>>'+str(i))
            console.insert('end','\n'+'finished<<')
    except:
        console.insert('0.0','okay okay, no panic something went , but you know what? it will be fixed soon! \nfinished<<')


# run the code button #
btn_run = tk.Button(
    master=window,
    background='lightSkyBlue',
    width="67",
    text="Run >>>",
    command=intepreter_run_now
)

# here just put the version
v_label = tk.Label(
    master=window,
    text="version 0.0.1",
    background="white",
    fg="black",
    font=("Times new romans",8)
)

def erease():
    console.delete('0.0','end')
    try:
        mycanvas.grid_remove()
    except:
        pass 

erase_console = tk.Button(
    master=window,
    text='clear console',
    background='grey',
    fg='black',
    width='67',
    command=erease
)

transpile = tk.Button(
    master=window,
    text='Transpile it!',
    background='lime',
    fg='black',
    width='67',
)


text_input_0 = """
custom::={

            names::set_0,set_1,set_2
    
            itens::a,b,c,f

            def::funcc,funcc_2

}end_custom

start_cloud{ 

        name::= set_0 { iten::= a ; membership::= ( funcc ) ; }end 

        name::= set_1 { iten::= b ; membership::= ( funcc_2 ) ; }end 
    
        name::= set_2 { iten::= b ; membership::= ( funcc ) ; }end 

    active=> { a <m> set_0 }end

    active=> { b <m> set_0 }end

    active=> { f <m> set_1 }end
}end_cloud


"""

# here we get an example of an well done sample of code #

editor.insert('0.0',text_input_0)

btn_config.grid(row=0,column=1)
editor.grid(row=1,column=1)
btn_run.grid(row=2,column=1)
path_label_main.grid(row=3,column=1)
erase_console.grid(row=4,column=1)
transpile.grid(row=5,column=1)
console.grid(row=6,column=1)
v_label.grid(row=7,column=1)

window.mainloop()
