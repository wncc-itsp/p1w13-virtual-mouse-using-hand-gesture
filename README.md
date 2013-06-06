p1w13-virtual-mouse-using-hand-gesture
=========================
This is a linux based mouse control application made using python. The libraries included for this application is openCV and unix. Unix library is present in the repo. In this project hand is detected using hsv skin color filtering and then the fingers are detected from the convex hull. To use this application you must wear a hand band or a full shirt. The background color should not be the same as skin color. You must avoid your face from being detected as it may  disturb the contours. This application is slow. So, you must be patient. 

We are thinking of extending it's applications gradually and make it more user friendly. currently only mouse movements and left click are there. To move the mouse on the screen simply move your open palm in front of camera. To click fold last three fingers. 
