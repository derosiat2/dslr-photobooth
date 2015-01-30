#get full size captures to work
#PERFORMANCE ISSUES
#~.25 seconds for this ImaeTk.PhotoImage function 
#preview_photo = ImageTk.PhotoImage(raw_string) 
#"raw_string" is not actually a string as raw_string might indicate, it's opening a data structure that has already been opened by PIL/pillow as an image 
#~.21 seconds for this create_image function 
#preview = pre_frame.create_image(320, 213, image=preview_photo) 
#END PERFORMANCE ISSUES
#consider terminating the program better or going back to preview mode
#add loop that takes multiple photos
import StringIO
import ctypes 
import sys 
#used for timing the countdown loop and trouble shooting
import time 
#for communication with bash and open/saving fles
import os
#my watermark program
import watermark
#from image updater program
from Tkinter import *
from PIL import Image, ImageTk, ImageDraw


#create a statusbar class
#this status bar isn't currently used.
class StatusBar(Frame):

    def __init__(self, master):
        Frame.__init__(self, master)
        self.label = Label(self, bd=1, relief=SUNKEN, anchor=W)
        self.label.pack(fill=X)

    def set(self, format, *args):
        self.label.config(text=format % args)
        self.label.update_idletasks()

    def clear(self):
        self.label.config(text="")
        self.label.update_idletasks()

def callback():
    #used for testing
    print "called the callback!"

def check(rtn): 
    if rtn != GP_OK: 
        gp.gp_result_as_string.restype = ctypes.c_char_p 
        print '!! ERROR(%s) %s' % (rtn,gp.gp_result_as_string(rtn)) 
        sys.exit(0) 
		
def preview_capt():
	gp.gp_camera_capture_preview(cam, fil, ctx)
	cData = ctypes.c_void_p() 
	cLen = ctypes.c_ulong() 
	gp.gp_file_get_data_and_size(fil, ctypes.byref(cData), ctypes.byref(cLen))
	img = ctypes.string_at(cData.value, cLen.value) 
	return img

	
def display(img, countdown):
	#start from image updater progam
	raw_string = Image.open(StringIO.StringIO(img))
	#raw_string = Image.open(img) #I use this when I'm not hooked up to the camera
	preview_photo = ImageTk.PhotoImage(raw_string)
	preview = pre_frame.create_image(320, 213, image=preview_photo)
	#to correct issue with printing long countdown strings on the screen when getting to 0
	if countdown <= 0:
	    countdown = 0
	if countdown >= 3:
	    countdown = 3
	countdown = str(int(countdown))
	#When countdown ends it shows all the numbers. 
	#Hopefully when I go back to live view that'll get overwritten
	countdown = pre_frame.create_text(40, 60, anchor=W, font=("Purisa", 40), fill="white", text=countdown)
	pre_frame.update_idletasks()
	pre_frame.pack()


#I don't know how to send data structure to capture_loop with a button press
#def capture_loop(time_sec, loops):
def capture_loop():
	#check(gp.gp_camera_init(cam, ctx)) #initializes the camera - maybe should be outside of function
	#print '** camera connected' 
	#end_time = time.time() + float(time_sec)
	global e    
	end_time = time.time() + 3.0
	cnt = 0 
	cur_time = 0. 
	start_time = time.time()
	while cur_time < end_time: 
		cnt+=1
		pic = cnt % 3 + 1
		display(preview_capt(), end_time-cur_time)
		#display("img%s.jpg" % pic, end_time-cur_time) #used when not hooked up to camera
		cur_time = time.time() 
	print 'total frames = %s, time = %s' % (cnt, (end_time - start_time))
	email = e.get()

	#trying to capture full size image, but it only comes out as a preview sized image
	gp.gp_camera_capture(cam, fil, ctx)
	cData = ctypes.c_void_p()
	cLen = ctypes.c_ulong()
	gp.gp_file_get_data_and_size(fil, ctypes.byref(cData), ctypes.byref(cLen))
	full_string = ctypes.string_at(cData.value, cLen.value) 
	full_size = Image.open(StringIO.StringIO(full_string))
	mark = Image.open('logo.png')
	full_size = watermark.watermark(full_size, mark, (.70, .70), .3, 1.0)
	#full_size.show() #test to make sure that the image is being captured
	full_size.save('%s.jpg' % email)
	#wait for file to write (not sure if this is necessary)
	write_delay  = 1.0 + time.time()
	while cur_time < write_delay: 
		cur_time = time.time() 
	os.system('echo "Sending an attachment." | mutt -s "attachment" %s -a /home/pi/projects/photobooth/%s.jpg' % (email, email))
	#test print to make sure the formatting is correct, it appears to be
	print 'echo "Sending an attachment." | mutt -s "attachment" %s -a /home/pi/projects/photobooth/%s.jpg' % (email, email)


#start gphoto specific calls
gp = ctypes.CDLL('libgphoto2.so') 

GP_OK = fileNbr = 0 
GP_VERSION_VERBOSE = 1 

cam = ctypes.c_void_p() 
gp.gp_camera_new(ctypes.byref(cam)) 
ctx = gp.gp_context_new() 
fil = ctypes.c_void_p() 
gp.gp_file_new(ctypes.byref(fil))
#end gphoto specific calls


#Set up GUI Window
root = Tk()
root.title("Window Title")
root.geometry("640x500")

#Set up preview frame
pre_frame = Canvas(root, bg = 'black', height = 426, width = 640)
pre_frame.pack(side = 'top')

#Initial preview before capturing happens
imageFile = 'img0.jpg'
image1 = ImageTk.PhotoImage(Image.open(imageFile))
preview = pre_frame.create_image(320, 213, image=image1)
pre_frame.pack()

# create a toolbar
toolbar = Frame(root)
toolbar_text = Label(toolbar, text="Enter your email address:", fg="blue")
toolbar_text.pack(side=TOP, padx=2, pady=2)

e = Entry(toolbar)
e.pack()

e.delete(0, END)
e.insert(0, "your@email.com")

#email = e.get()

#add buttons
#I don't know how to send data structure to capture_loop with a button press
b = Button(toolbar, text="Start capture!", width=10, command=capture_loop)
#b = Button(toolbar, text="Set Status", width=6, command=callback)
b.pack(side=TOP, padx=2, pady=2)

toolbar.pack(side=TOP, fill=X)
totLen = 0


#capture_loop(3, 1)
#os.system("gphoto2 --capture-image-and-download --filename fullsize.jpg")
#print 'echo "Sending an attachment." | mutt -s "attachment" %s -a /home/pi/mono.jpg' % email
root.mainloop()
