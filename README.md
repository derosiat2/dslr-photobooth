I'm trying to develop a DSLR photobooth application with emailing and live preview
that runs on a raspberry pi and am currently using a Nikon D5100. This program 
will require gphoto2 to be installed along with MUTT for emailing attachments. 
This program also relies on Pillow. Pillow is a fork of PIL (program image library). 

This photobooth application also adds a watermark to the final images. The images
will be saved under the email address entered with the .jpg extension and
the water mark image is expected to be a .png file. 

I am currently having many issues with this program the most major one right now 
being that the performance of tkinter of loading the images for the preview is 
super slow. So if anyone knows of a faster way to do this, that would be great. 

PERFORMANCE ISSUES
~.25 seconds for this ImaeTk.PhotoImage function 
preview_photo = ImageTk.PhotoImage(raw_string) 

~.21 seconds for this create_image function 
preview = pre_frame.create_image(320, 213, image=preview_photo) 
END PERFORMANCE ISSUES

The other major issue is that I don't know how to get a full size image capture. I can only
get a preview sized image. I thought gp.gp_camera_capture(cam, fil, ctx) would get me a 
full sized image, but it doesn't. 

I also need to figure out how to do an autofocus using ctypes and libgphoto2.