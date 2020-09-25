import nltk
from nltk import CFG 
from nltk.parse import RecursiveDescentParser
from nltk.parse.generate import generate
import re 
import itertools
import io 
from tkinter import *
import tkinter as tk
import importlib 
import os 

class file_read():
# here we will read the .cld files
    def read(file):
        
        with open(file,'r') as f:
            words = f.read()
            return words 

        f.close()

# here we can only read the input text from the tk.Text 
    def from_ide(plain_text):

        return True       

class set_calculus():
# here we will evaluate and return the operations but using the membership functions
# the other operations use the only the pre-processed and already declared itens
    def membership_evaluation(plain_text):
        membership_dict = {}
        try:
            membership_format = plain_text.split('name::=')             
            for sentence in membership_format:
                if 'start_cloud{' in sentence:
                    pass
                else:
                    s = sentence.split()
                    set_title = s[0]
                    function = s[7]
                    print('checked')

            return membership_dict

        except:
            return 'membership evaluation error'


class operations():
# here we will create functions that will deal with each possible operations
    def op_ss(set0,set1,oprr,conj_group):
# operation between two sets 

        iten_set_0 = []
        iten_set_1 = []

        counter = 0
        while counter < len(conj_group):
# here we store the itens from the selectionated sets 
            if conj_group[counter]['name::='] == set0:
                
                iten = conj_group[counter]['iten::=']
                iten_set_0.append(iten)

            elif conj_group[counter]['name::='] == set1:

                iten = conj_group[counter]['iten::=']
                iten_set_1.append(iten)

        
            counter+=1

# the possibilities of operations ss are : -i, -u and -c
        result = []

        if oprr == '-u':
# for the union of two sets 
            for i in iten_set_0:
                result.append(i)
            for i in iten_set_1:
                result.append(i)

            return result

        elif oprr == '<m>':
            pass 

        elif oprr == '-i':
# intersection between two sets              
            l0 = len(iten_set_0)
            l1 = len(iten_set_1)
            try:
                if l0 >= l1:
                    minimum = l0 
                else:
                    minimum = l1 
# here we iterate the lists until the smaller list 
                counter = 0
                while counter < minimum:
                    if iten_set_1[counter] in iten_set_0:
                        result.append(iten_set_1[counter])
                    else:
                        pass   
                    counter+=1
            except:
                return 'check itens again'

            return result             
        else:
            pass 
        


    def op_is(iten,set_,oprr,conj_group,path=None):
# operation between iten and set
        iten_set = []
        func_set = {}
        
        counter = 0
        while counter < len(conj_group):
            if conj_group[counter]['name::='] == set_:
                
                itens = conj_group[counter]['iten::=']
                iten_set.append(itens)

                func = list(conj_group[counter])[3]
                func_set[set_] = func

            else:
                pass 
        
            counter+=1

# the possibilities of operations ss are : in and out

        if oprr == 'in':

            if iten in iten_set:
                return True 
            else:
                return False 
            
        elif oprr == 'out':

            if iten not in iten_set:
                return True 
            else:
                return False 
# here we can acess functions from native python instead if having to rewrite it everytime
# the membership function must be the last method from a class 
        elif oprr == '<m>':
            try:
                if set_ in func_set:
                    m = globals()[func_set[set_]]
                    f = getattr(m,str(dir(m)[len(dir(m))-1])) 
                    print(f)
                    return f(iten)
                else:
                    return 'not declared'

            except:
                
                if set_ in func_set and path != None:
                    try:
                        m = importlib.__import__(path)
                    except:
                        print('exception')
                    f = getattr(m,func_set[set_])
                    print(f)
                    ff = getattr(f,dir(f)[len(dir(f))-1]) 
                    print(ff)
                    return ff(iten)
                else:
                    return 'not declared out of the file'
                

class cloudy_main():
# here we gonna implement the special part of the code in which you will declare the names are gonna use
# and the itens 
    def my_cache(plain_text):

        set_name = 0 

        return set_name 


    def normalizer(plain_text):
# here we devide the code between the structure of names and itens selections and the commands itself  
        
        normalized_text_0 = {}
        first_split = plain_text.split('}end_custom')
        
        second_split = first_split[0].split('\n')
        for m in second_split:
            if re.findall('^custom::',m):
                second_split.remove(m)
                pass 
            else:
                if len(m.split()) == 0:
                    pass 
                else:
                    k = m.split('::')
                    k_dict = {}

                    topic = None 
                    counter = 0
                    while counter < len(k):
                        
                        if counter == 0 :
                            if re.findall('itens',k[counter]):
                                topic = 'iten'
                            elif re.findall('names',k[counter]):
                                topic= 'name'
                            elif re.findall('def',k[counter]):
                                topic='def'
                            else:
                                pass 
                                
                        else:
                            k_dict[topic] = k[counter].split(',')

                            normalized_text_0.update(k_dict)


                        counter+=1

        plain_text = ''.join(first_split[1]) 

# here we erase the spaces between the lines that can appear 
# so that the user can write the code more freely than it would if he had to write
# all code together without identitation

        normalized_text = []
        no_line_text = plain_text.split("\n")
        for n in no_line_text:
            statment = n.split()
            if len(statment) == 0:
                pass 
            else:
                norm_text = ' '.join(statment)
                normalized_text.append(norm_text)

        return '\n'.join(normalized_text), normalized_text_0 



    def parser(plain_text,set_name={'name':['x','y','z'],'iten':['a','b','c'],'def':['m','n','o']}):
#first we define the cfg that will generate all possible sentences for the language 
# based on the names of set's and ite's name the user have choosen        
        # formatting the functions names
        line_grammar = "MEM_FUNC -> "
        counter = 0 
        while counter < len(set_name['def']):

            if counter == 0:
                formated_newstring = " '{a}' ".format(a=set_name['def'][counter])
            else:
                formated_newstring = " | '{a}' ".format(a=set_name['def'][counter])

            line_grammar+=formated_newstring

            counter+=1

        # formatting for set names
        line_grammar_0 = "NAME -> "
        counter = 0 
        while counter < len(set_name['name']):

            if counter == 0:
                formated_newstring = " '{a}' ".format(a=set_name['name'][counter])
            else:
                formated_newstring = " | '{a}' ".format(a=set_name['name'][counter])

            line_grammar_0+=formated_newstring

            counter+=1

        line_grammar_1 = "NAME_I -> "
        counter = 0 
        while counter < len(set_name['iten']):

            if counter == 0:
                formated_newstring = " '{a}' ".format(a=set_name['iten'][counter])
            else:
                formated_newstring = " | '{a}' ".format(a=set_name['iten'][counter])

            line_grammar_1+=formated_newstring

            counter+=1
        

        prime_cloudy_grammar = ((("""

            T ->  COM_D END | INIT_A COM_A END | 'start_cloud{' | '}end_cloud'  
            
            COM_D -> 'name::=' NAME '{' ITEN ';' MEM ';' 
            lacune_1
            lacune_2
            ATTR -> ITEN ';' MEM ';'
            ITEN -> 'iten::=' NAME_I  


            MEM -> 'membership::=' '(' MEM_FUNC ')' 
            lacune_3


            INIT_A -> 'active=>' '{'
            COM_A -> NAME Q NAME | NAME_I O NAME |'plot=>' CONJ 'using:' PLOT_S
            PLOT_S -> 'line' | 'venn'

            CONJ -> NAME Q NAME | NAME 
            Q -> '-u' | '-i' | '-c'
            O -> 'in' | 'out' | '<m>'


            END -> '}end'
            """.replace('lacune_1',line_grammar_0)).replace('lacune_2',line_grammar_1)).replace('lacune_3',line_grammar))

# using the nltk's tool to generate , we create the formal cfg 
        _cloudy_grammar = CFG.fromstring(prime_cloudy_grammar)
        #for sentences_test in generate(_cloudy_grammar,n=200):
            #print(' '.join(sentences_test))
# then we create the parser for this grammar
        cloudy_rd = RecursiveDescentParser(_cloudy_grammar)
# split the input text into lines
        code_total = plain_text.split('\n')
        
        counter = 0
        while counter < len(code_total):
            test = code_total[counter].split()
# all code must start and end with specific sample of code as follows 
            if counter == 0 and 'start_cloud{' in test:
                print("starting parsing") 
                pass
            elif counter != 0:
                pass 
            else:
                return 'start_cloud statment not found' 
# the end cloud statment determines where the parser will stop parsing the code
            if "}end_cloud" in test: 
                print('end of parsing')
                return 'end of parsing'
            else:
                pass 
                
            try:
                parsed_check = []
                for parsed in cloudy_rd.parse(test):
                    parsed_check.append(parsed)
# if the length of the list which contain the parsed sentences is equal to 0 then 
# it means that the sentence wasnt well, so there's a some syntax error                 
                if len(parsed_check) != 0:
                    pass 
                else: 
                    return 'Syntax error on: ('+str(code_total[counter]) + ' ) at line : ' + str(counter)

            except:
# if some lexical component not allowed is used then the system can recognize it faster
                return 'Lexical error on : ('+str(code_total[counter]) + ') at line : ' + str(counter)     
            
            counter+=1 

    def semantic_set_layer(well_parsed):
# first we will analyse all declarative propositions and store 
# the declared conjuncts
        conj_group = []

        code = well_parsed.split('\n')
        for well_formed in code:
# here we spot the end statment so that we avoid processing useless data for semantic info
            if well_formed == '}end_cloud':
                break
            else:
                pass 

            try:
                wf = well_formed.split()
# here we see if the lines satifies each component and decide what to do with the information
# given if the information is a set declaration or an active code execution 
                if wf[0] == 'name::=':
# first we parse and find the name of the sets we are dealing
                    for token in wf:
# then put it as a key on a dictionary , so that we can store the other kind of data 
# for the given set we are dealing with :
                        sigma = [';','{','}end']
                        
                        if token in sigma :
                            wf.remove(token)
# here we gather the real meaningful data fr   om the pure input code              
                    set_ = dict(itertools.zip_longest(*[iter(wf)] * 2, fillvalue=""))
                    conj_group.append(set_)
                
                elif wf[0] == 'active=>':
                    pass 
            except:
                print('parser error identified')
                pass 

        return conj_group


    def semantic_active_layer(well_parsed):

        code = well_parsed.split('\n')
# here we will store the operators and the elements which it will work on 
        op_list = []

        counter = 0 
        for well_formed in code:
# we just repeat the steps done before with the cloud
            if well_formed == "}end_cloud":
                break
            else:
                pass 

            try:

                wf = well_formed.split()
# plot is a special active case so we just jump right now 
                if 'plot=>' in wf:
                    break 
                else:
                    pass 
                
                if 'active=>' in wf and '}end' in wf :
# using the index of inital statment we can get the elements and the operators 
                    
                    init_index = wf.index('active=>')

                    elem_1 = wf[init_index+2]
                    opr = wf[init_index+3]
                    elem_2 = wf[init_index+4]

                    opr_set = {
                        counter:
                    {
                        'e1':elem_1,
                        'op':opr,
                        'e2':elem_2
                        }
                    }

                    op_list.append(opr_set)
                    counter+=1

                else:
                    pass
            except:
                print('parser error')
                pass 


        return op_list

    def format_set_active(conj_group,op_list,path=None):
# these function will check if all sets used on the active layer
# can be found on the declarated clouds

        console_log = []

        value = len(op_list)

        set_set = ['-u','-i','-c']
        obj_set = ['in','out','<m>']

        set_list = []
        iten_list = []

        counter = 0 
        while counter < len(conj_group):

            set_0 = conj_group[counter]['name::=']
            set_1 = conj_group[counter]['iten::=']

            set_list.append(set_0)
            iten_list.append(set_1)

            counter+=1
        
        counter = 0
        while counter < value:

            e0 = op_list[counter][counter]['e1']
            e1 = op_list[counter][counter]['e2']
            oprr = op_list[counter][counter]['op']

# here we check if it is operation between an object and a set 
# or it's a operation between set and set 
            if oprr in obj_set and oprr != '<m>':
                if e0 in iten_list and e1 in set_list:
                    q = operations.op_is(e0,e1,oprr,conj_group)
                    console_log.append(q)
                else:
                    return 'set/iten not declared'
            # here we make an specific case for the membership calculus , because it will need for computational power 
# so the special case is done in order to differenciate the interpretation time between the heavier and the lighter weights code 
            elif oprr == '<m>':
                q = operations.op_is(e0,e1,oprr,conj_group,path)
                console_log.append(q)
                
            elif oprr in set_set:
                if e0 in set_list and e1 in set_list :
                    q = operations.op_ss(e0,e1,oprr,conj_group)
                    console_log.append(q)
                else:
                    return 'set/iten not declared'
            
            counter+=1
        return console_log

class vizualization():
# here we parse the plot statment given that this is a different statment 
# the plot statment requires tkinter and matplot , so using it will open a tkinter window
# so needs a different treatment while parsing
   def plot_parse(plain_text,conj_group,op_list):
# here we spot the plot statments to parse them first as we will do with all other 
# kind of statments

        plot_code = []
        plot_list = []

        plain_code = plain_text.split('\n')
       
        for statment in plain_code:
            
            statment_list = statment.split()
            
            if 'plot=>' in statment_list:
                plot_code.append(statment)
        
        counter = 0
        for plot in plot_code:

            plot_char = plot.split()

            init_index = plot_char.index('plot=>')
            
            el0 = plot_char[init_index+1]
            oprr = plot_char[init_index+2]
            el1 = plot_char[init_index+3]

            style = plot_char[init_index+5]

            plot_stats = {
                        counter:
                    {
                        'e1':el0,
                        'op':oprr,
                        'e2':el1,
                        'style':style
                        }
                    }
            plot_list.append(plot_stats)
            counter+=1 
# here we jut copy the common set configuration for set operations in order to find the same solution as it did before 
        
        console_log = []

        value = len(plot_list)

        set_set = ['-u','-i','-c']
        obj_set = ['in','out','<m>']

        set_list = []
        iten_list = []
        func_list = []

        aux_set = {}

        counter = 0 
        while counter < len(conj_group):

            set_0 = conj_group[counter]['name::=']
            set_1 = conj_group[counter]['iten::=']
            set_2 = conj_group[counter]['def::=']

            set_list.append(set_0)
            iten_list.append(set_1)
            func_list.append(set_2)

            aux_set[set_0] = [set_1]

            counter+=1
        
        counter = 0
        while counter < value:

# we modify the code a little so that we can now use the given operations for the sets in the plot enverioment 
# given that the other function will only deal with non-plot statments 
            
            e0 = plot_list[counter][counter]['e1']
            e1 = plot_list[counter][counter]['e2']
            oprr = plot_list[counter][counter]['op']

            plot_log = []

            if oprr in obj_set:
                if e0 in iten_list and e1 in set_list:
                    q = operations.op_is(e0,e1,oprr,conj_group)
                    console_log.append(q)
                else:
                    return 'set/iten not declared'
# here we make an specific case for the membership calculus , because it will need for computational power 
# so the special case is done in order to differenciate the interpretation time between the heavier and the lighter weights code 
            elif oprr == '<m>':
                if e0 in iten_list and e1 in set_list:
                    q = operations.op_is(e0,e1,oprr,conj_group)
                    console_log.append(q) 
            elif oprr in set_set:
                if e0 in set_list and e1 in set_list :
                    q = operations.op_ss(e0,e1,oprr,conj_group)
                    console_log.append(q)
# then we need identify the sets in use and where does the itens in use belongs to 
                    for set_ in aux_set:
                        plot_set = aux_set[set_]
                        for result in q :
                            if result in plot_set:
                                plot_log.append((set_,plot_set,oprr))
                else:
                    return 'set/iten not declared'
            
            counter+=1
        return plot_log, console_log

   def create_circle(x, y, r, canvasName): #center coordinates, radius
# here we just create the circles which will represent the venn diagrams     
    x0 = x - r
    y0 = y - r
    x1 = x + r
    y1 = y + r
    return canvasName.create_oval(x0, y0, x1, y1)

   def iten_layer(info,oprr,canvasName):

    label = []
    itens = []

    for group in info[0]:
        label.append(group[0])
        itens.append(group[1])
# here we plot the union between two sets 
    if oprr == '-u':
        vizualization.create_circle(100, 55, 50, canvasName)
        vizualization.create_circle(60, 55, 50, canvasName)
        canvasName.create_text(40, 120,text=label[0])
        canvasName.create_text(105, 120,text=label[1])
        canvasName.create_text(35, 60,text=itens[0])
        canvasName.create_text(125, 60,text=itens[1])
# or the intersection between two sets 
    elif oprr == '-i':
        try:
            vizualization.create_circle(100, 55, 50, canvasName)
            vizualization.create_circle(60, 55, 50, canvasName)
            canvasName.create_text(40, 120,text=label[0])
            canvasName.create_text(105, 120,text=label[1])
            canvasName.create_text(35, 60,text=itens[0])  
            canvasName.create_text(125, 60,text=itens[1])
        except:
            return 'no intersection found'

# here we use the already parsed statment and open the generated the venn diagrams 
   def plot_function(parsed_p_statment,window=None,position=None):
       if window != None and position != None:
           window.title('Plot window')  
           myCanvas = Canvas(master=window)
           myCanvas.grid(row=position[0],column=position[1])
# here we show the vizualization
           try:
               vizualization.iten_layer(parsed_p_statment,parsed_p_statment[0][0][2],myCanvas)
           except:
               pass 
           window.mainloop()
       else:
           window_plot = tk.Tk()
           window_plot.title('Plot window')
           myCanvas = Canvas(master=window_plot)
           myCanvas.grid()
# here we show the vizualization
           try:
               vizualization.iten_layer(parsed_p_statment,parsed_p_statment[0][0][2],myCanvas)
           except:
               pass  
           window_plot.mainloop()

class interpreter():
# here all functions that are needed for the interpeter to run are putted together 
# so to import the interpreter all that is needed is to use the function interpreter.run()
    def run(text_input,window=None,position=None,path=None):
        
        normalized = cloudy_main.normalizer(text_input)
# first we filter by the non-vizualizable information which are console-only 
        parsed = cloudy_main.parser(normalized[0],normalized[1])
        
        if parsed == 'end of parsing':
            pass 
        else:
            return parsed 

        conj = cloudy_main.semantic_set_layer(normalized[0])
        opr_conj = cloudy_main.semantic_active_layer(normalized[0])
        f = cloudy_main.format_set_active(conj,opr_conj,path)

# second we filter by the plottable information
        if 'plot=>' in normalized[0].split():
            i = vizualization.plot_parse(normalized[0],conj,opr_conj)
            v = vizualization.plot_function(i,window,position)
        else:
            pass 

        return f 