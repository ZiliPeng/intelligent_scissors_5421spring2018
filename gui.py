import tkinter
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from PIL import ImageTk, Image, ImageDraw
from intelligent_scissor import IntelligentScissor
import numpy as np
import time
from functools import partial


LOAD_IMAGE_STATE=0
PREPARE_STATE = 1
START_COUNTER_STATE =2
PROCESS_COUNTER_STATE=3
FINISH_STATE=4
FINISH_CLOSE_STATE=5
CHOOSE_STATE=6

gloabl_state = -1

#Global variables shared between files
#cursor_x, cursor_y holds current cursor coordinates
cursor_x, cursor_y = 0, 0
#xy_stack saves all past clicks
xy_stack = []
#canvas ids of line segments in path drawn on canvas, correspond to the computed path
canvas_path = []
canvas_path_stack = []
contour_stack = []
history_paths = []

#Global variables used within this file
#file_name = ''
#image = ''

start_flag = False
finish_flag = False
lastx, lasty = 0, 0
canvas_id = 0
#startx, starty = 0, 0
i = 0
wrap_length = 1920

#obj = IntelligentScissor(cvimg, (int(seed_x),int(seed_y)))
#obj.link_calculation()
#start_time = time.time()
#print('node dict generation')
#obj.generate_all_node_dict()
#print('node dict generation time:', time.time() - start_time)

class GUI():
    def __init__(self, global_state=-1):
        self.state = gloabl_state
        self.canvas_path=[]
        self.canvas_path_stack=[]
        self.contour_stack=[]
        self.history_paths=[]
        self.lastx, self.lasty=0,0
        self.canvas_id = 0
        #self.canvas = canvas

        #frame
        self.mainframe = ttk.Frame(root,padding='20', borderwidth = '8')
        self.mainframe['relief'] = 'ridge'
        self.mainframe.grid(column=0, row=0, sticky=(N,W,E,S))

        #define scroll bar
        h = ttk.Scrollbar(self.mainframe, orient=HORIZONTAL)
        v = ttk.Scrollbar(self.mainframe, orient=VERTICAL)

        #canvas
        self.canvas = Canvas(self.mainframe, width=640, height=480, bg='white',scrollregion=(0, 0, 1000, 1000), yscrollcommand=v.set,xscrollcommand=h.set)
        self.canvas.grid(column=0, row=0, columnspan = 4, rowspan = 4, sticky=(N,W,E,S))
        self.mainframe.columnconfigure(0,weight = 3)
        self.mainframe.columnconfigure(1,weight = 3)
        self.mainframe.columnconfigure(2,weight = 3)
        self.mainframe.columnconfigure(3,weight = 3)
        self.mainframe.rowconfigure(0,weight = 3)
        self.mainframe.rowconfigure(1,weight = 3)
        self.mainframe.rowconfigure(2,weight = 3)
        self.mainframe.rowconfigure(3,weight = 3)
            

        #scroll bar setup
        h['command'] = self.canvas.xview
        v['command'] = self.canvas.yview
        h.grid(column=0, row=4, columnspan = 4, sticky=(W,E))
        v.grid(column=4, row=0, rowspan = 4,  sticky=(N,S))

    def open_image(self):
        #default = False
        #start_flag = False
        #if default == True:
            #image = ImageTk.PhotoImage(file='./images/test.jpg')
            ##cvimg = cv2.imread("../images/test.jpg")
            #cvimg = np.array(Image.open("./images/test.jpg"))
            #canvas.create_image(0,0, image=image, anchor=NW)
        #else :
            #TODO get current path
        file_name = filedialog.askopenfilename(initialdir = './images')
        image = ImageTk.PhotoImage(file=file_name)
        pil_img = Image.open(file_name)
        self.canvas.create_image(0,0, image=image, anchor=NW)
        draw_image = ImageDraw.Draw(pil_img)
        obj = IntelligentScissor(np.array(pil_img))
        
#def open_image():
    #global canvas, image, cvimg, start_flag, obj, draw_image, gloabl_state
    ##TODO remove debug clause
    #default = False
    #start_flag = False
    #if default == True:
        #image = ImageTk.PhotoImage(file='./images/test.jpg')
        ##cvimg = cv2.imread("../images/test.jpg")
        #cvimg = np.array(Image.open("./images/test.jpg"))
        #canvas.create_image(0,0, image=image, anchor=NW)
    #else :
        ##TODO get current path
        #file_name = filedialog.askopenfilename(initialdir = './images')
        #image = ImageTk.PhotoImage(file=file_name)
        #pil_img = Image.open(file_name)
        #canvas.create_image(0,0, image=image, anchor=NW)
        #draw_image = ImageDraw.Draw(pil_img)
    #obj = IntelligentScissor(np.array(pil_img))

#def seed_to_graph(seed_x,seed_y):
    ##global obj
    #obj.update_seed((seed_x, seed_y))
    #start_time = time.time()
    ##print('cost_map_generation')
    #obj.cost_map_generation()
    #print('cost map generation time:', time.time() - start_time)
    ##print('cost map generation COMPLETED')

#def start(event):
    #global lastx, lasty, startx, starty, start_flag, xy_stack, finish_flag
    #start_flag = True
    #finish_flag = False
    #startx, starty = canvas.canvasx(event.x), canvas.canvasy(event.y)
    #lastx, lasty = startx, starty
    #xy_stack.append([startx,starty,-99])
    #stack_label.configure(text=xy_stack)
    #print('startx, starty: {0} {1}'.format(startx, starty))
    #seed_to_graph(startx,starty)

#def close_contour_finish(event):
    #global start_flag, canvas_id, canvas_path_stack, canvas_path, i, history_paths, finish_flag, obj, contour_stack
    #print('close contour finish called')
    #if (start_flag == True):
        ##canvas_id = canvas.create_line((lastx, lasty, startx, starty), fill=color, width=1,tags='currentline')
        #remove_canvas_path(canvas_path)
        #canvas_path.clear()
        #draw_path(startx,starty)
        #canvas_path_stack.append(canvas_path[:])
        #path = obj.get_path((int(startx),int(starty)))
        #history_paths.append(path[:])

        ##path_label.configure(text = '{0}th canvas_path: {1}'.format(i,canvas_path))
        #path_label.configure(text = 'closing path: {1}'.format(i,path))
        ##history_paths_label.configure(text='path_stack {0}: {1}'.format(i, canvas_path_stack[i]))
        #history_paths_label.configure(text='closed history_paths : {1}'.format(i, history_paths))
        #i = i + 1

        #canvas_path.clear()
        #start_flag = False
        #finish_flag = True
        #xy_stack.append([startx,starty,canvas_id])
        #stack_label.configure(text=xy_stack)
        ##TODO uncomment to integrate
        #obj.generate_mask(history_paths)
    #else:
        #print('Warning: end() is called before start()')

#def finish(event):
    #global start_flag, finish_flag
    #start_flag = False
    #finish_flag = True
    #print('finish called')

#def click_xy(event):
    #global lastx, lasty, start_flag, xy_stack, canvas_id, canvas_path, canvas_path_stack, i
    ##print('event x y:{0} {1}'.format(event.x,event.y))
    ##print('last  x y:{0} {1}'.format(lastx,lasty))
    #if (start_flag == True):

        #x, y = canvas.canvasx(event.x), canvas.canvasy(event.y)
        ##set_color('green')

        ##fix current path on canvas, start new seed
        ##canvas_id = canvas.create_line((lastx, lasty, x, y), fill=color, width=1,tags='currentline')
        #draw_path(x,y)
        #path = obj.get_path((int(x),int(y)))
        #history_paths.append(path[:])
        #path_label.configure(text = '{0}th path: {1}'.format(i,path))
        ##path_label.configure(text='path_stack before append {0}: {1}'.format(i, canvas_path_stack))
        ##history_paths_label.configure(text='path_stack {0}: {1}'.format(i, canvas_path_stack[0]))
        ##history_paths_label.configure(text='path_stack after {0}: {1}'.format(i, canvas_path_stack))
        #canvas_path_stack.append(canvas_path[:])
        ##canvas_path_stack.append('test {0}'.format(i))
        ##history_paths_label.configure(text='path_stack {0}: {1}'.format(i, canvas_path_stack[0]))
        #history_paths_label.configure(text='history_paths after {0}th append: {1}'.format(i, history_paths))
        #i = i + 1
        #canvas_path.clear()

        ##generate new graph with new seed
        #seed_to_graph(x,y)

        #lastx, lasty = x, y
        #xy_stack.append([x,y,canvas_id])
        #stack_label.configure(text=xy_stack)
    #debug_label.configure(text='start_flag:{0}'.format(start_flag))
    #debug2_label.configure(text='line_id:{0}'.format(canvas_id))
    #debug3_label.configure(text='lastx:{0} lasty:{1}'.format(lastx,lasty))

#def delete_path(event):
    #global canvas_id, lastx, lasty, start_flag, canvas_path, canvas_path_stack, start_flag, finish_flag
    ##[popx, popy, pop_id] = xy_stack[-1]
    #if start_flag == True:
        #[popx, popy, pop_id] = xy_stack.pop()
        #stack_label.configure(text=xy_stack)
        #canvas_path_to_be_removed = canvas_path_stack.pop()
        #path_to_be_removed = history_paths.pop()
        #path_label.configure(text = 'path to be removed: {1}'.format(i,path_to_be_removed))
        #history_paths_label.configure(text='path_stack after pop: {1}'.format(i, history_paths))
        #if pop_id == -99 :
            #start_flag = False
            #remove_canvas_path(canvas_path)
        #else :
            ##delete point in stack
            #canvas.delete(pop_id)
            #[lastx, lasty, canvas_id] = xy_stack[-1]
            #seed_to_graph(lastx,lasty)
            ##delete drawn path on canvas
            #remove_canvas_path(canvas_path_to_be_removed)

            ##update debug info
            #stack_label.configure(text=xy_stack)
            #debug_label.configure(text='canvas_id:{0}'.format(canvas_id))
            #debug2_label.configure(text='removed_id:{0}'.format(pop_id))
            #debug3_label.configure(text='lastx:{0} lasty:{1}'.format(lastx,lasty))
    #elif finish_flag==True:
        #while len(canvas_path_stack)>0:
            #path = canvas_path_stack.pop()
            #remove_canvas_path(path)
        #start_flag = False
        #finish_flag = False
        #canvas_path_stack.clear()
        #canvas_path.clear()
    #else:
        #print('please move cursor inside an existing contour to delete')
        ##TODO select existing contour and delete it

#def draw_line_image(path_):
    ## TODO draw path in canvas_path_stack to image and saved as countour
    #pass


#def get_xy(event):
    #global cursor_x, cursor_y, cursor_label, canvas_id, lastx, lasty, canvas_path
    #cursor_x, cursor_y = canvas.canvasx(event.x), canvas.canvasy(event.y)
    #cursor_label.configure(text = 'x:{0} y:{1}'.format(cursor_x, cursor_y))
    #debug_label.configure(text='start_flag:{0}'.format(start_flag))
    #debug2_label.configure(text='line_id:{0}'.format(canvas_id))
    #debug3_label.configure(text='lastx:{0} lasty:{1}'.format(lastx,lasty))
    ##print(cursor_x, cursor_y)
    #if start_flag == True:
        ##remove last path in canvas
        #remove_canvas_path(canvas_path)
        #canvas_path.clear()
        ##draw new path on canvas
        #draw_path(cursor_x,cursor_y)
        #path = obj.get_path((int(cursor_x),int(cursor_y)))
    ##path_label.configure(text = 'current canvas_path: {1}'.format(i,canvas_path))
        #path_label.configure(text = 'current path: {1}'.format(i,path))

#def remove_canvas_path(canvas_path_to_be_removed):
    #canvas_path_len = len(canvas_path_to_be_removed)
    #for line_id in canvas_path_to_be_removed:
        #canvas.delete(line_id)
    ##canvas_path_to_be_removed.clear()

#def draw_path(x,y):
    #global cursor_label, canvas_id, lastx, lasty, canvas_path, path_label
    #cursor_label.configure(text = 'getting path for x:{0} y:{1}'.format(cursor_x, cursor_y))
    #path = obj.get_path((int(x),int(y)))
    ##set_color('red')
    #path_len = len(path)
    #for index, point in enumerate(path):
        #if index < (path_len - 1):
            #next_point = path[index + 1]
        #else:
            ##print('reached last point, break for loop')
            #break
        #canvas_id = canvas.create_line((point[0],point[1],next_point[0],next_point[1]), fill = color, width = 1, tags = 'currentline')
        ##canvas_id = canvas.create_line((point[1],point[0],next_point[1],next_point[0]), fill = color, width = 1, tags = 'currentline')
        #canvas_path.append(canvas_id)


        ##cursor_label.configure(text = 'getting path for x:{0} y:{1}'.format(cursor_x, cursor_y))
        ##path = obj.get_path((int(cursor_x),int(cursor_y)))
        ##print(path)

def set_color(newcolor, canvas):
    global color
    color = newcolor
    canvas.dtag('all', 'paletteSelected')
    canvas.itemconfigure('palette', outline='white')
    canvas.addtag('paletteSelected', 'withtag', 'palette%s' % color)
    canvas.itemconfigure('paletteSelected', outline='#999999')

#def save_contour():
    #if start_flag==True or finish_flag==True:
        #file_name = filedialog.asksaveasfilename(initialdir = './images',
                #filetypes = (("png files","*.png"), ("jpeg files","*.jpg")))
        #canvas.postscript(file=file_name, colormode='color')
    ##return

#def save_mask():
    #if finish_flag==True:
        #file_name = filedialog.asksaveasfilename(initialdir = './images',
                #filetypes = (("png files","*.png"), ("jpeg files","*.jpg")))
        #Image.fromarray((obj.mask*255).astype(np.uint8)).save(file_name)
    ##return

def create_scissor_window():
    scissor_window = tkinter.Toplevel(root)

root = Tk()
root.title('Intelligent Scissors by Lei & Hao HKUST COMP5421 Spring 2018')
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)



#canvas = gui_obj.canvas
gui_obj = GUI()
#menu
menubar = Menu(root)
filemenu = Menu(menubar, tearoff = 0)
filemenu.add_command(label="Open Image", command = gui_obj.open_image)
#filemenu.add_separator()
#filemenu.add_command(label="Save Contour", command = save_contour)
#filemenu.add_command(label="Save Mask", command = save_mask)
#filemenu.add_separator()
#filemenu.add_command(label="Exit", command = root.quit)
menubar.add_cascade(label="File", menu=filemenu)

toolmenu = Menu(menubar, tearoff = 0)
toolmenu.add_command(label = "Scissor", command = create_scissor_window)
menubar.add_cascade(label="Tool", menu=toolmenu)

root.configure(menu = menubar)



#button
#button_open_image = ttk.Button(mainframe, text = 'open image', command = open_image).grid(column=5,row=0, sticky=(E,N))

#size grip
ttk.Sizegrip(root).grid(column=1, row=1, sticky=(S,E))

#show cursor coornidate
cursor_label =ttk.Label(gui_obj.mainframe, text='x:0,y:0')
cursor_label.grid(column = 3, row = 5, sticky = (E,N))
gui_obj.canvas.bind('<Leave>', lambda e: cursor_label.configure(text='cursor outside canvas'))

#show other debug info
debug_label = ttk.Label(gui_obj.mainframe, text='<debug info>')
debug_label.grid(column = 0, row = 5, sticky = (W,N))
debug2_label = ttk.Label(gui_obj.mainframe, text='<debug2 info>')
debug2_label.grid(column = 1, row = 5, sticky = (W,N))
debug3_label = ttk.Label(gui_obj.mainframe, text='<debug3 info>')
debug3_label.grid(column = 2, row = 5, sticky = (W,N))


stack_label = ttk.Label(gui_obj.mainframe, text='<stack info>', wraplength = wrap_length, justify = 'left')
stack_label.grid(column = 0, row = 6, columnspan = 4, sticky = (W,N))

path_label = ttk.Label(gui_obj.mainframe, text='<path info>', wraplength = wrap_length, justify = 'left')
path_label.grid(column = 0, row = 7, columnspan = 4, sticky = (W,N))

history_paths_label = ttk.Label(gui_obj.mainframe, text='<path stack info>', wraplength = wrap_length, justify = 'left')
history_paths_label.grid(column = 0, row = 8, columnspan = 4, sticky = (W,N))

#Main function binding
#gui_obj.canvas.bind('<Button-1>', click_xy)
#gui_obj.canvas.bind('<Control-Button-1>', start)
#root.bind('<Return>', finish)
#root.bind('<BackSpace>', delete_path)
#root.bind('<Control-Return>', close_contour_finish)
#gui_obj.canvas.bind('<Motion>', get_xy)
#canvas.bind('<B1-Motion>', add_line)
#canvas.bind('<B1-ButtonRelease>', done_stroke)

#TODO palette, should do with color chooser dialog
canvas_id = gui_obj.canvas.create_rectangle((10, 10, 30, 30), fill='red', tags=('palette','palettered', 'paletteSelected'))
gui_obj.canvas.tag_bind(canvas_id, '<Button-1>', lambda x: set_color('red', gui_obj.canvas))
canvas_id = gui_obj.canvas.create_rectangle((10, 35, 30, 55), fill='green', tags=('palette','palettegreen'))
gui_obj.canvas.tag_bind(canvas_id, '<Button-1>', lambda x: set_color('green',gui_obj.canvas))
set_color('green', gui_obj.canvas)
gui_obj.canvas.itemconfigure('palette', width=5)

#gui_obj.canvas.pack()
#gui_obj.mainframe.pack()
root.mainloop()
