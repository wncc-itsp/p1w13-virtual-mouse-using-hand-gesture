import cv
capture=cv.CaptureFromCAM(0)
image=cv.QueryFrame(capture)
writer=cv.CreateVideoWriter("D:\output.avi", 0, 15, cv.GetSize(image), 1)
count=0
while count<100:
    image=cv.QueryFrame(capture)
    grey=cv.CreateImage(cv.GetSize(image),8,1)
    cv.CvtColor(image,grey,cv.CV_BGR2GRAY)
    cv.Smooth(grey,grey,cv.CV_MEDIAN)
    cv.EqualizeHist(grey,grey)
    #threshold=100
    #colour=255
    #cv.Threshold(grey,grey,threshold,colour,cv.CV_THRESH_OTSU)
    #pos=2
    #element_shape=cv.CV_SHAPE_RECT
    #element = cv.CreateStructuringElementEx(pos*2+1, pos*2+1, pos, pos, element_shape)
    # cv.Erode(grey,grey,element,2)
    dst_16s2 = cv.CreateImage(cv.GetSize(grey), cv.IPL_DEPTH_16S, 1)
    cv.Laplace(grey, dst_16s2,3)
    cv.Convert(dst_16s2,grey)
    #storage = cv.CreateMemStorage()
   # haar=cv.LoadHaarClassifierCascade('haarcascade_frontalface_default.xml')
    #detected = cv.HaarDetectObjects(grey, haar, storage, 1.2, 2,cv.CV_HAAR_DO_CANNY_PRUNING, (100,100))
    #if detected:
    #    for face in detected:
     #3       print face
    cv.WriteFrame(writer,grey)
    cv.ShowImage('Image_Window',grey)
    cv.WaitKey(2)
    count+=1
    
