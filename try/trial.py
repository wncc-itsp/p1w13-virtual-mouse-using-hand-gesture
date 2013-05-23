import cv
def traverse(seq):
	while seq:
		print list(seq)
	traverse(seq.v_next()) # Recurse on children
	seq = seq.h_next() # Next sibling
capture=cv.CaptureFromCAM(-1)
count=0
while count<1000:
	image=cv.QueryFrame(capture)	
	cv.Flip(image, flipMode=1)
	grey=cv.CreateImage(cv.GetSize(image),8,1)
	cv.CvtColor(image,grey,cv.CV_BGR2GRAY)
	cv.Smooth(grey, grey, cv.CV_GAUSSIAN, 11, 11,0,0)
	cv.Threshold(grey,grey, 120,255,1)
	dst_16s2 = cv.CreateImage(cv.GetSize(image), cv.IPL_DEPTH_16S, 1)
	cv.Laplace(grey, dst_16s2,3)
	cv.Convert(dst_16s2,grey)
	contours=cv.FindContours(grey, cv.CreateMemStorage(), cv.CV_RETR_LIST, cv.CV_CHAIN_APPROX_SIMPLE, (0, 0))
	des=cv.CreateImage(cv.GetSize(image),8,3)
	for contour in contours:
		cv.DrawContours(des, [contour], (255,0,0), (0,255,0), -1,5)
	cv.ShowImage('Image_Window',grey)
	cv.ShowImage('dest_Window',des)
	print(contours)
	if cv.WaitKey(2)== 27:
		break
	count+=1		
