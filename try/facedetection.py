import cv
import numpy
capture=cv.CaptureFromCAM(-1)
#writer=cv.CreateVideoWriter("output.avi", 0, 20, (640,480) , 1)
count=0
hc = cv.Load("/usr/share/opencv/haarcascades/haarcascade_frontalface_alt.xml")
while count<500:
	image=cv.QueryFrame(capture)	
	cv.Flip(image, flipMode=1)
	grey=cv.CreateImage(cv.GetSize(image),8,1)
	cv.CvtColor(image,grey,cv.CV_BGR2GRAY)
	#Detect face in image
	if count % 5 == 0:
		face = cv.HaarDetectObjects(grey, hc, cv.CreateMemStorage(), 1.2,2, cv.CV_HAAR_DO_CANNY_PRUNING, (0,0) )
#	print face
	for [(x,y,w,h),k] in face:
		print 'face found at: '+str(x)+','+str(y)
		cv.Rectangle(image,(x ,y),(x+w,y+h),(0,255,0))
	cv.ShowImage('Image_Window',image)
	cv.WaitKey(2)
	count+=1		
