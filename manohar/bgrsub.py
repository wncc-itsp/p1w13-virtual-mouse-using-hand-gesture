import cv
capture=cv.CaptureFromCAM(0)
cv.WaitKey(200)
frame=cv.QueryFrame(capture)
temp=cv.CloneImage(frame)
cv.Smooth(temp,temp,cv.CV_BLUR,5,5)
while True:
    frame=cv.QueryFrame(capture)
    cv.AbsDiff(frame,temp,frame)
    cv.ShowImage("Windo2w",temp)
    cv.ShowImage("Window",frame)
    c=cv.WaitKey(2)
    if c==27:
        break
