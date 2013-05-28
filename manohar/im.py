import cv
capture=cv.CaptureFromCAM(-1)
contours=cv.CreateMemStorage()
while True:
    image=cv.QueryFrame(capture)
    grey=cv.CreateImage(cv.GetSize(image),8,1)
    cv.CvtColor(image,grey,cv.CV_BGR2GRAY)
    cv.Smooth(grey,grey,cv.CV_GAUSSIAN)
    threshold=100
    colour=255
    #cv.Threshold(grey,grey,threshold,colour,1)
    #cv.FindContours(grey,contours,cv.CV_RETR_LIST,cv.CV_CHAIN_APPROX_SIMPLE,(0,0))
#cv.DrawContours(grey,contours,(255,255,255),(255,255,255),2,1,8,(0,0))
#cv.Canny(grey,edges
    cv.ShowImage('a_window',grey)
    c=cv.WaitKey(2)
    if c==27:
        break
