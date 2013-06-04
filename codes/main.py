import cv
import random
from unix import PyMouse
	
minsat=30
maxsat=150
minhue=0
maxhue=20

def changeMinSat(x):
	global minsat
	minsat=x
def changeMaxSat(x):
	global maxsat
	maxsat=x	
def changeMinHue(x):
	global minhue
	minhue=x
def changeMaxHue(x):
	global maxhue
	maxhue=x		
	
mouse = PyMouse()
width,height= mouse.screen_size()
capture=cv.CaptureFromCAM(-1)
count=0
#cv.NamedWindow("Image_Window")	
#cv.CreateTrackbar("min-saturation", "Image_Window", minsat, 255, changeMinSat );
#cv.CreateTrackbar("max-saturation", "Image_Window", maxsat, 255, changeMaxSat );
#cv.CreateTrackbar("min-hue", "Image_Window", minhue, 255, changeMinHue );
#cv.CreateTrackbar("max-hue", "Image_Window", maxhue, 255, changeMaxHue );
while count<1000:
	image=cv.QueryFrame(capture)
	w,h=cv.GetSize(image)
#	cv.AddWeighted(image,0.01,background,0.99,0,background)
#	cv.AbsDiff(image,background,image)
	cv.Flip(image, flipMode=1)
	hsv_image=cv.CreateImage(cv.GetSize(image),8,3)
	hsv_mask = cv.CreateImage( cv.GetSize(image), 8, 1);
	hsv_edge = cv.CreateImage( cv.GetSize(image), 8, 1);
	hsv_min = cv.Scalar(minhue, minsat, 60, 0);
	hsv_max = cv.Scalar(maxhue, maxsat, 255, 0);
	cv.CvtColor(image,hsv_image,cv.CV_BGR2HSV)
	cv.InRangeS (hsv_image, hsv_min, hsv_max, hsv_mask)
	element_shape = cv.CV_SHAPE_RECT
	pos=1
	element = cv.CreateStructuringElementEx(pos*2+1, pos*2+1, pos, pos, element_shape)
	cv.Dilate(hsv_mask,hsv_mask,element,2)
	cv.Erode(hsv_mask,hsv_mask,element,2)
	cv.Smooth(hsv_mask, hsv_mask, cv.CV_MEDIAN, 27,0,0,0)
#	cv.Threshold(grey,grey, 150,255,1)
#	dst_16s2 = cv.CreateImage(cv.GetSize(image), cv.IPL_DEPTH_16S, 1)
#	cv.Laplace(hsv_mask, dst_16s2,3)
#	cv.Convert(dst_16s2,hsv_mask)
	cv.Canny(hsv_mask, hsv_edge, 1, 3, 5);
	contours=cv.FindContours(hsv_mask, cv.CreateMemStorage(), cv.CV_RETR_LIST, cv.CV_CHAIN_APPROX_SIMPLE, (0, 0))
	des=cv.CreateImage(cv.GetSize(image),8,3)
	result=0
	result2=0
	contours2 = False
	contoursCopy=contours
	hull=False
	blank=cv.CreateImage(cv.GetSize(image),8,3)
	while contours:
		result = abs( cv.ContourArea( contours ) )
		if result>result2:
			contours2=contours
		contours = contours.h_next()
	if contours2:
		hull=cv.ConvexHull2(contours2, cv.CreateMemStorage(),cv.CV_CLOCKWISE,0)
		defects=cv.ConvexityDefects(contours2, hull, cv.CreateMemStorage())	

		cv.DrawContours(blank, contours2, (255,0,0), (0,255,0), 0,5)
		noOfDefects=0
		for defect in defects:																				
			start,end,far,d = defect
			cv.Line(blank,start,end,[0,255,0],2)				
			if d > 20:
				cv.Circle(blank,far,5,[0,0,255],-1)
				noOfDefects=noOfDefects+1
		print noOfDefects		
		x,(p,q),radius = cv.MinEnclosingCircle(contours2)	
		if x:
			cv.Circle(blank,(int(p),int(q)),int(radius),[0,0,255],1)
		X,Y = ((p-w/2)*width*5/(w*4))+width/2,((q-h/2)*height*5/(h*4))+height/2
		if X < 0:
			X = 0
		else										
			X=min(X,width)
			
		if Y < 0:
			Y = 0
		else:
			Y=min(Y,height)
					
		if noOfDefects >= 3:				
			mouse.move(X,Y)
		elif noOfDefects > 1:	
			mouse.click(X,Y)		
	cv.ShowImage('Image_Window',blank)
	if cv.WaitKey(2)== 27:
		break
	count+=1
		
