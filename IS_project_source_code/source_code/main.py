import numpy as np
import cv2
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import imutils
import time
from tensorflow.keras.models import load_model



class mainwindow:
    def __init__(self):
        self.em_label=['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']
        self.gender_label = ["male","female"]        
        self.age_label = ['1-5','6-15','16-26','27-41','42-60','greater 60']
        
        self.modelgen = load_model('models/gender.h5')        
        self.modelage = load_model('models/age.h5')
        self.modelem = load_model('models/emotion.h5')

        (self.width, self.height) = (720, 1280) 
        haar_file = 'haarcascade_frontalface_default.xml'
        self.face_cascade = cv2.CascadeClassifier(haar_file)

        self.b,self.g,self.r,self.a = 0,255,0,0        
        self.count = 1



        self.window = tk.Tk()  #Makes main window
        self.window.wm_title("Gender, age and emotion recognition")    
        self.window.config(background="#FFFFFF")

        self.imageFrame = tk.Frame(self.window, width=854, height=480)
        self.imageFrame.grid(row=3, column=0, padx=10, pady=2)

        self.stringvarinfile = tk.StringVar()
        self.stringvarinfile.set('')
        self.stringtypeinput = tk.StringVar()
        self.stringtypeinput.set('')
        self.screenwidth = self.window.winfo_screenwidth()
        self.screenheight = self.window.winfo_screenheight()
        
        self.window.geometry(f'{int(self.screenwidth/1.2)}x{int(self.screenheight/1.2)}+{int(self.screenwidth/12)}+{int(self.screenheight/12)}')
        self.entryvidname =  tk.Entry(self.window, textvariable=str(self.stringvarinfile), font = "Helvetica 12 bold",width=55,bg='white',fg='black',justify='center',state='disable')
        self.entryvidname.grid(padx=10,pady=10,row=1,column=0)
        
        self.menubutton = tk.Menubutton(self.window, textvariable=self.stringtypeinput, indicatoron=True,
                                borderwidth=1, relief="raised", width=20)
        self.main_menu = tk.Menu(self.menubutton, tearoff=False)
        self.menubutton.configure(menu=self.main_menu)
        list_input = [["Webcam"],["Video"],["Image"]]
        list_cam = self.show_camera_list()
        for cam in list_cam:
            list_input[0].append(cam)
        for item in list_input:
            if item[0] == 'Webcam':
                menu = tk.Menu(self.main_menu, tearoff=False)
                self.main_menu.add_cascade(label=item[0], menu=menu)            
                for value in item[1:]:
                    menu.add_radiobutton(value=value, label=value, variable=self.stringtypeinput,command=lambda: self.show())            
            else:
                self.main_menu.add_radiobutton(value=item, label=item, variable=self.stringtypeinput,command=lambda: self.show())
        
        self.menubutton.grid(padx=5,pady=5,row=1,column=1)
        self.browse_file = tk.Button(self.window,text="Browse",font="Helvetica 12",command =lambda: self.fileDialog(self.stringvarinfile))
        self.browse_file.grid(padx=5,pady=5,row=1,column=2)

        
        self.play_button = tk.Button(self.window,text="PLAY",font="Helvetica 12",command = lambda:self.play_video())
        self.play_button.grid(padx=5,pady=5,row=2,column=1)
        self.play_button = tk.Button(self.window,text="STOP",font="Helvetica 12",command = lambda:self.turn_off_current())
        self.play_button.grid(padx=5,pady=5,row=2,column=2)
        self.lmain = tk.Label(self.imageFrame)
        self.lmain.grid(padx=5,pady=5,row=0,column=0)
        self.file_path = tk.StringVar()
        self.file_path.set('')
        self.prev_frame_time = 0
        self.startTime = time.time()
        
        self.new_frame_time = 0
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.stream_status = False

        self.window.mainloop()
    def turn_off_current(self):
        self.stream_status = False
    def show_camera_list(self):
        index = 0
        arr = []
        while True:
            test_cap = cv2.VideoCapture(index)
            if not test_cap.read()[0]:
                break
            else:
                arr.append(f'Camera {str(index)}')
            test_cap.release()
            index += 1
        return arr
    def show(self):
        self.turn_off_current()        
        if self.stringtypeinput.get() == "Video" or self.stringtypeinput.get() =="Image":
            self.browse_file.config(state="normal")
        else:
            self.browse_file.config(state="disable")
    def play_video(self):   
        var_input = self.stringtypeinput.get().split()
        if var_input[0] == 'Video' or var_input[0] == 'Image':
            path = self.file_path.get()
        else:           
            path = int(var_input[1])
        if self.stream_status == False:
            if 'cap' in dir(self):   
                del self.cap
                time.sleep(2)
                self.cap=cv2.VideoCapture(path)
            else:
                self.cap=cv2.VideoCapture(path)
            self.stream_status = True        
            self.show_frame()
    def show_frame(self):
        if self.stream_status == False:
            return 0
        else:
            _, frame = self.cap.read()
            frame = imutils.resize(frame, width=720)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.3, 4)
            for (x, y, w, h) in faces:
              if len(faces) > 0:
                facergb = frame[y:y + h, x:x + w]
                facegray = gray[y:y + h, x:x + w]
                
                infacergb= cv2.resize(facergb,(48,48))
                infacergb = np.array([el/255.0 for el in infacergb])
                infacergb = infacergb.reshape(1, 48, 48, 3)
                
                #gender+age
                pred_gen = self.modelgen.predict(infacergb)
                pred_gen = self.gender_label[int(np.round(pred_gen))]
                pred_age = self.modelage.predict(infacergb)
                pred_age = self.age_label[np.argmax(pred_age)]

                #emotion
                infacegray= cv2.resize(facegray,(48,48))
                infacegray = np.array([el/255.0 for el in infacegray])
                infacegray  = infacegray .reshape(1, 48, 48, 1)
                pred_em = self.modelem.predict(infacegray)
                pred_em=  self.em_label[np.argmax(pred_em)]

                #draw to each frame
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(frame, pred_gen , (x-18, y+30), font, 1, (0, 255, 255), 2, cv2.LINE_AA)
                cv2.putText(frame, pred_age , (x-18, y), font, 1, (255, 255, 0), 2, cv2.LINE_AA)
                cv2.putText(frame, pred_em , (x-18, y+100), font, 1, (255, 255, 0), 2, cv2.LINE_AA)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

            img = Image.fromarray(cv2.cvtColor(frame,cv2.COLOR_BGR2RGB))
            imgtk = ImageTk.PhotoImage(image=img)
            self.lmain.imgtk = imgtk
            self.lmain.configure(image=imgtk)
      
            return self.lmain.after(1,lambda: self.show_frame())

    def fileDialog(self,path):        
        filename = filedialog.askopenfilename(initialdir =  "/", title = "Select A File", filetype = (("all files","*.*"),) )
        self.turn_off_current()
        self.stringvarinfile.set(filename)
        self.file_path.set(filename)
 
if __name__ == "__main__":
    GUI = mainwindow()
