import cv2

from ultralytics import YOLO
import numpy as np
#from torchvision import transforms
import pyrealsense2 as rs
#import matplotlib.pyplot as plt
import RPi.GPIO as GPIO
#import curses
import time




class cam:
    def __init__(self,width,height):
        self.pipeline = rs.pipeline()
        self.config = rs.config()
        self.config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
        self.config.enable_stream(rs.stream.color, 640, 480, rs.format.rgb8, 30)
        self.width= width
        self.height = height 
        self.mid_x = width//2
        self.mid_y = height//2
        self.co_x = int(0.05 * (width))
        self.u = self.mid_x-self.co_x 
        self.v = self.co_x +self.mid_x
    def get_quad(self,x,y):
        #x_mid = self.mid_x
        y_mid = self.mid_y
        #co_x = int(0.1 * (2*x_mid))
        #co_y = int(0.1 * (2*y_mid))
        
        if x <self.u  and y < y_mid:
            #print("first")
            quad = 1
        elif x >self.v and y < y_mid:
            quad =2 
        elif x >self.v and y >y_mid:
            quad =3
        elif x <self.u and y > y_mid:
            #print("first")
            quad = 4
        else:
            quad = 0
        
        return quad
    
    def get_frame(self):
        # Start the RealSense pipeline
        self.pipeline.start(self.config)

        # Get the depth and color frames
        frames = self.pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()

        # Convert the depth frame to a numpy array
        depth_image = np.asanyarray(depth_frame.get_data())

        # Convert the color frame to a numpy array (in RGB format)
        color_image = np.asanyarray(color_frame.get_data())

        # Stop the pipeline
        self.pipeline.stop()
        self.frame = color_image
        self.depth = depth_frame

        return color_image, depth_image

    def detect(self,mdl_path):
        vid = cv2.VideoCapture(0) 
        vid.set(cv2.CAP_PROP_FRAME_WIDTH,self.width)
        vid.set(cv2.CAP_PROP_FRAME_HEIGHT,self.height)
        model = YOLO(mdl_path)
        
        while (True):
            ret, frame = vid.read()
            cv2.line(frame,(self.mid_x,0),(self.mid_x,self.height),(255,255,0),2)
            cv2.line(frame,(self.u,0),(self.u ,self.height),(255,255,0),2)
            cv2.line(frame,(self.v,0),(self.v ,self.height),(255,255,0),2)
            
            results = model.predict(source =frame, save = False ,  stream = True, imgsz = 240, conf = 0.5)
            
            detect = False
            
            for result in results:
                for box in result.boxes:
                    clss=box.cls
                    if len(clss)>0:
                        co=box.xywh
                        detect = True
            if detect == True:
                coordinates = co.int()
                x1=coordinates[0][0].item()
                y1 =coordinates[0][1].item()
                w=coordinates[0][2].item()
                h=coordinates[0][3].item()
                cv2.circle(frame,(x1,y1),5,(0,255,0),-1)
                cv2.circle(frame,(x1,y1),50,(0,255,0),1)
                font = cv2.FONT_HERSHEY_SIMPLEX 
                org = (50, 50) 
                fontScale = 1
                color = (255, 0, 0) 
                thickness = 2

                quad = self.get_quad(x1,y1)
                quad = str(quad)
                #image = cv2.putText(frame, quad, org, font,  fontScale, color, thickness, cv2.LINE_AA)
                #cv2.imshow('frame', image)
                #return (x1,y1)
            
            cv2.imshow('frame', frame) 
            
            
            if cv2.waitKey(1) & 0xFF == ord('q'): 
                break
        vid.release() 
        # Destroy all the windows 
        cv2.destroyAllWindows() 
    def detect_from_depth(self,mdl_path):
            model = YOLO(mdl_path)
            results = model.predict(source =self.frame, save = False ,  stream = True, imgsz = 240, conf = 0.5)


    def get_center(self,mdl_path):
        
        model = YOLO(mdl_path)
        detect = False
        results = model.predict(source = self.frame, save = False ,  stream = True, imgsz = 240, conf = 0.5)    
        for result in results:
            for box in result.boxes:
                clss=box.cls
                if len(clss)>0:
                    co=box.xywh
                    detect = True
        if detect == True:
            coordinates = co.int()
            x1=coordinates[0][0].item()
            y1 =coordinates[0][1].item()
            w=coordinates[0][2].item()
            h=coordinates[0][3].item()
            return [x1,y1],True
            
        else:
            return [],False

    def get_dir(self,quad):
        
        dir = 's'
        
        if quad== 0:
            dir = 'f'
        if quad == 3:
            dir = 'r'
        if quad == 4:
            dir = 'l'
        if quad== 1:
           dir = 'f'
        if quad== 2:
            dir = 'f'
        return dir
    def move(self,dir):
        if dir == 'f':
            rover.forward()
        if dir == 'l':
            rover.left()
        if dir == 'r':
            rover.right()
            
         
        
class rover:
    def __init__(self,relay_2,speed_1,relay_1, speed_2):
        GPIO.setmode(GPIO.BCM)
        self.p = GPIO.PWM(16, 100)
        self.relay_2 = relay_2
        self.speed_1 =speed_1
        self.relay_1 = relay_1
        self.speed_2 = speed_2

    
        # Set up the GPIO pins you are using
        
    def left(self):
        speed_1 = self.p.start(30)
        speed_2 = self.p.start(30)
        GPIO.output(speed_1, GPIO.HIGH)
        GPIO.output(speed_2, GPIO.HIGH)
        GPIO.output(self.relay_1, GPIO.LOW)
        GPIO.output(self.relay_2, GPIO.HIGH)
        time.sleep(1) 
    def right(self):
        speed_1 = self.p.start(30)
        speed_2 = self.p.start(30)
        GPIO.output(speed_1, GPIO.HIGH)
        GPIO.output(speed_2, GPIO.HIGH)
        GPIO.output(self.relay_1, GPIO.HIGH)
        GPIO.output(self.relay_2, GPIO.LOW)
        time.sleep(1)
    def forward(self):
        speed_1 = self.p.start(50)
        speed_2 = self.p.start(50)
        GPIO.output(speed_1, GPIO.HIGH)
        GPIO.output(speed_2, GPIO.HIGH)
        GPIO.output(self.relay_1, GPIO.LOW)
        GPIO.output(self.relay_2, GPIO.LOW)
        time.sleep(1)  # Adjust sleep time as needed
    def back(self):
        speed_1 = self.p.start(20)
        speed_2 = self.p.start(20)
        GPIO.output(speed_1, GPIO.HIGH)
        GPIO.output(speed_2, GPIO.HIGH)
        GPIO.output(self.relay_1, GPIO.HIGH)
        GPIO.output(self.relay_2, GPIO.HIGH)
        time.sleep(1)
    def stop(self):
        GPIO.output(self.speed_1, GPIO.LOW)
        GPIO.output(self.speed_2, GPIO.LOW)
        GPIO.output(self.relay_1, GPIO.LOW)
        GPIO.output(self.relay_2, GPIO.LOW)     
    
    



