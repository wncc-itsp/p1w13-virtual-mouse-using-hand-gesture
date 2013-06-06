import cv
import random
from unix import PyMouse
	

minV=10
hc = cv.Load("haarcascade_frontalface_alt.xml")

def changeMinBrightness(x):
	global minV
	minV=x
		
		
def pointInFace(xpos,ypos,x,y,w,h):
	return (xpos>x and xpos<x+w and ypos>y and ypos<y+h)
x=0
y=0
w=0
h=0	
mouse = PyMouse()
width,height= mouse.screen_size()
capture=cv.CaptureFromCAM(-1)
image=cv.QueryFrame(capture)
X,Y=mouse.position()
click=False
#writer=cv.CreateVideoWriter("output.avi", 0, 15, cv.GetSize(image), 1)
count=0 
cv.NamedWindow("Image Window")	
cv.CreateTrackbar("min-brightness", "Image Window", minV, 100, changeMinBrightness );

while True:
	image=cv.QueryFrame(capture)
	cv.Flip(image, flipMode=1)
	grey=cv.CreateImage(cv.GetSize(image),8,1)
	cv.CvtColor(image,grey,cv.CV_BGR2GRAY)
	
	#Detect face in image
	if count % 10 == 0:
		face = cv.HaarDetectObjects(grey, hc, cv.CreateMemStorage(), 1.2,2, cv.CV_HAAR_DO_CANNY_PRUNING, (0,0) )
		
	#print face	
	for [(x,y,w,h),k] in face:
		cv.Rectangle(image,(x ,y),(x+w,y+h),(0,255,0))
		
	window_width,window_height=cv.GetSize(image)
	hsv_image=cv.CreateImage(cv.GetSize(image),8,3)
	hsv_mask = cv.CreateImage( cv.GetSize(image), 8, 1);
	hsv_edge = cv.CreateImage( cv.GetSize(image), 8, 1);
	hsv_min = cv.Scalar(0, 30, minV, 0);
	hsv_max = cv.Scalar(20, 150, 255, 0);
	cv.CvtColor(image,hsv_image,cv.CV_BGR2HSV)
	cv.InRangeS (hsv_image, hsv_min, hsv_max, hsv_mask)
	element_shape = cv.CV_SHAPE_RECT
	pos=1
	element = cv.CreateStructuringElementEx(pos*2+1, pos*2+1, pos, pos, element_shape)
	cv.Dilate(hsv_mask,hsv_mask,element,2)
	cv.Erode(hsv_mask,hsv_mask,element,2)
	cv.Smooth(hsv_mask, hsv_mask, cv.CV_MEDIAN, 25,0,0,0)
	cv.Canny(hsv_mask, hsv_edge, 1, 3, 5);
	contours=cv.FindContours(hsv_mask, cv.CreateMemStorage(), cv.CV_RETR_LIST, cv.CV_CHAIN_APPROX_SIMPLE, (0, 0))
	des=cv.CreateImage(cv.GetSize(image),8,3)
	contours2 = False
	hull=False
	blank=cv.CreateImage(cv.GetSize(image),8,3)
	
	while contours:	
		contours2=contours
		contours = contours.h_next()
		
	if contours2:
		hull=cv.ConvexHull2(contours2, cv.CreateMemStorage(),cv.CV_CLOCKWISE,0)
		defects=cv.ConvexityDefects(contours2, hull, cv.CreateMemStorage())	
		cv.DrawContours(image, contours2, (255,0,0), (0,255,0), 0,5)		
		noOfDefects=0		
		comx,comy=0,0
		Z,(p,q),radius = cv.MinEnclosingCircle(contours2)
		
		if Z:
			cv.Circle(image,(int(p),int(q)),int(5),[0,255,255],-1)	
			
		for defect in defects:																				
			start,end,far,d = defect
			xpos,ypos=far
			cv.Line(image,start,end,[0,255,0],2)
							
			if d > 20 and not pointInFace(xpos,ypos,x,y,w,h):
				cv.Circle(image,far,5,[0,0,255],-1)				
				if noOfDefects:					
					cv.Circle(image,end,10,[0,0,0],-1)
					#cv.Line(image,end,(int(p),int(q)),[0,0,0],3)
					x,y=end
					comx,comy=comx+x,comy+y
				else:
					cv.Circle(image,start,10,[0,0,0],-1)
					#cv.Line(image,start,(int(p),int(q)),[0,0,0],3)
					x,y=start
					comx,comy=comx+x,comy+y
					cv.Circle(image,end,10,[0,0,0],-1)
					#cv.Line(image,end,(int(p),int(q)),[0,0,0],3)
					x,y=end
					comx,comy=comx+x,comy+y
				noOfDefects=noOfDefects+1	
		p,q=comx/(noOfDefects+1),comy/(noOfDefects+1)
		#print len(defects),noOfDefects								
		initx,inity=X,Y	
		X,Y = ((p-window_width/12)*width*6/(window_width*5)),((q-window_height/12)*height*6/(window_height*5))
		
		diffx,diffy=X-initx,Y-inity		
		X,Y=initx+ diffx*(0.1+abs(diffx)/700), inity+ diffy*(0.1+abs(diffy)/300)	
						
		if X < 0:
			X = 0
		else:										
			X=min(X,width)
			
		if Y < 0:
			Y = 0
		else:
			Y=min(Y,height)
			
		if len(defects) > 10 and len(defects) < 35:				
			if noOfDefects > 0 and noOfDefects < 7 :
				i=0.33
				while i<=1:			
					mouse.move(initx+i*(X-initx),inity+i*(Y-inity))
					i+=0.33
				if noOfDefects > 1 and noOfDefects<3:
					if not(click):	
						mouse.click(initx,inity)
						click=True	
				else:
					click=False
							
	cv.ShowImage('Image Window',image)
#	cv.WriteFrame(writer, image)
	if cv.WaitKey(2)== 27:
		break
	count+=1
		
