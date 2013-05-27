import cv
import random
def randomColor():
	return (random.randint(0,255),random.randint(0,255),random.randint(0,255))

capture=cv.CaptureFromCAM(-1)
count=0
while count<1000:
	image=cv.QueryFrame(capture)	
	cv.Flip(image, flipMode=1)
	hsv_image=cv.CreateImage(cv.GetSize(image),8,3)
	hsv_mask = cv.CreateImage( cv.GetSize(image), 8, 1);
	hsv_edge = cv.CreateImage( cv.GetSize(image), 8, 1);
	hsv_min = cv.Scalar(0, 30, 60, 0);
	hsv_max = cv.Scalar(20, 150, 255, 0);
	cv.CvtColor(image,hsv_image,cv.CV_BGR2HSV)
	cv.InRangeS (hsv_image, hsv_min, hsv_max, hsv_mask)
	element_shape = cv.CV_SHAPE_RECT
	pos=1
	element = cv.CreateStructuringElementEx(pos*2+1, pos*2+1, pos, pos, element_shape)
	cv.Dilate(hsv_mask,hsv_mask,element,1)
#	cv.Erode(hsv_mask,hsv_mask,element,2)
	cv.Smooth(hsv_mask, hsv_mask, cv.CV_GAUSSIAN, 15,15,0,0)
#	cv.Threshold(grey,grey, 150,255,1)
#	dst_16s2 = cv.CreateImage(cv.GetSize(image), cv.IPL_DEPTH_16S, 1)
#	cv.Laplace(hsv_mask, dst_16s2,3)
#	cv.Convert(dst_16s2,hsv_mask)
	cv.Canny(hsv_mask, hsv_edge, 1, 3, 5);
	contours=cv.FindContours(hsv_mask, cv.CreateMemStorage(), cv.CV_RETR_LIST, cv.CV_CHAIN_APPROX_SIMPLE, (0, 0))
	des=cv.CreateImage(cv.GetSize(image),8,3)
	result=0
	result2=0
	contours2 = contours
	contoursCopy=contours
	hull=False
	while contours:
		result = abs( cv.ContourArea( contours ) )
		if result>result2:
			contours2=contours
			hull = cv.ConvexHull2(contours, cv.CreateMemStorage(),cv.CV_CLOCKWISE,1)
			defects=cv.ConvexityDefects(contours2, hull, cv.CreateMemStorage())
		contours = contours.h_next()
		
	cv.DrawContours(hsv_image, contours2, (255,0,0), (0,255,0), 0,5)
	if hull:
		cv.DrawContours(hsv_image, hull, (0,0,0), (0,255,0), 0,5)	
	cv.ShowImage('Image_Window',hsv_image)
	if cv.WaitKey(2)== 27:
		break
	count+=1
		
