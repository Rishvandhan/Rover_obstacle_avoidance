from oop import cam
from oop import rover
import cv2

cam = cam(640,480)
rover = rover(relay_2 = 20,speed_1 = 19,relay_1 = 26,speed_2 = 16)
mdl_path = 'cylinder.pt'
frame,depth = cam.get_frame()
center,detect = cam.get_center( mdl_path=mdl_path)
while(not detect):
    
    frame = cam.get_frame() 
    center,detect = cam.get_center( mdl_path=mdl_path)
    #rover.left()
    print('nodetection moving left')
    if detect:
        center,detect = cam.get_center( mdl_path=mdl_path)


        quad = cam.get_quad(center[0],center[1])
    
    
        dirct=cam.get_dir(quad)

        while (dirct != 'f'):
            
            #cam.move(dirct)
            #print(dirct)
            frame = cam.get_frame() 
            center,detect = cam.get_center(mdl_path=mdl_path)
            if detect:
                center,detect = cam.get_center(mdl_path=mdl_path)
                quad = cam.get_quad(center[0],center[1])
                dirct = cam.get_dir(quad)
                print(dirct)
            else:
                cam.move('l')
                print('not detected moving left')
        
        
        
    
    
    if (dirct == 'f'):
        cam.move('f')
        print('f')
       

    

  
    

    
    
