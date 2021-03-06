from pykinect2 import PyKinectV2
from pykinect2.PyKinectV2 import *
from pykinect2 import PyKinectRuntime

import ctypes
import _ctypes
import pygame
import sys

from pickle import dump

if sys.hexversion >= 0x03000000:
    import _thread as thread
else:
    import thread

# colors for drawing different bodies 
SKELETON_COLORS = [pygame.color.THECOLORS["red"], 
                  pygame.color.THECOLORS["blue"], 
                  pygame.color.THECOLORS["green"], 
                  pygame.color.THECOLORS["orange"], 
                  pygame.color.THECOLORS["purple"], 
                  pygame.color.THECOLORS["yellow"], 
                  pygame.color.THECOLORS["violet"]]


class BodyGameRuntime(object):
    def __init__(self):
        pygame.init()

        # Used to manage how fast the screen updates
        self._clock = pygame.time.Clock()

        # Set the width and height of the screen [width, height]
        self._infoObject = pygame.display.Info()
        self._screen = pygame.display.set_mode((self._infoObject.current_w >> 1, self._infoObject.current_h >> 1), 
                                               pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE, 32)

        pygame.display.set_caption("Kinect for Windows v2 Body Game")

        # Loop until the user clicks the close button.
        self._done = False

        # Used to manage how fast the screen updates
        self._clock = pygame.time.Clock()

        # Kinect runtime object, we want only color and body frames 
        self._kinect = PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Color | PyKinectV2.FrameSourceTypes_Body)
        ##PyKinectRuntime.PyKinectRuntime(PyKinectV2.framesource

        # back buffer surface for getting Kinect color frames, 32bit color, width and height equal to the Kinect color frame size
        self._frame_surface = pygame.Surface((self._kinect.color_frame_desc.Width, self._kinect.color_frame_desc.Height), 0, 32)

        # here we will store skeleton data 
        self._bodies = None


    def draw_body_bone(self, joints, jointPoints, color, joint0, joint1):
        joint0State = joints[joint0].TrackingState;
        joint1State = joints[joint1].TrackingState;

        # both joints are not tracked
        if (joint0State == PyKinectV2.TrackingState_NotTracked) or (joint1State == PyKinectV2.TrackingState_NotTracked): 
            return

        # both joints are not *really* tracked
        if (joint0State == PyKinectV2.TrackingState_Inferred) and (joint1State == PyKinectV2.TrackingState_Inferred):
            return

        # ok, at least one is good 
        start = (jointPoints[joint0].x, jointPoints[joint0].y)
        end = (jointPoints[joint1].x, jointPoints[joint1].y)

        ##if (joint0 == PyKinectV2.JointType_WristRight):
            ##print(joints[joint0].x, joints[joint0].y) #, jointPoints[joint0].z)
            ##print(joints[joint0].Position.x, joints[joint0].Position.y, joints[joint0].Position.z)

        try:
            pygame.draw.line(self._frame_surface, color, start, end, 8)
        except: # need to catch it due to possible invalid positions (with inf)
            pass
        
    def draw_pagh(self, joints, jointPoints):
        
        self.img = pygame.image.load('PAGG.png')
        (width,height) = self.img.get_size()

        p1 = (jointPoints[PyKinectV2.JointType_Head].x, jointPoints[PyKinectV2.JointType_Head].y)
        p2 = (jointPoints[PyKinectV2.JointType_Head].x, jointPoints[PyKinectV2.JointType_Head].y)
        p3 = (jointPoints[PyKinectV2.JointType_Head].x, jointPoints[PyKinectV2.JointType_Head].y)
        p4 = (jointPoints[PyKinectV2.JointType_Head].x, jointPoints[PyKinectV2.JointType_Head].y)

        
        (x0,y0) = (p1[0]-width/2,p1[1]-8.5*height/10)

        #surface = self._frame

        self._frame_surface.blit(self.img, (x0,y0))

        try:
            
            pygame.draw.line(self._frame_surface, color, start, end, 8)
        except: # need to catch it due to possible invalid positions (with inf)
            pass

    def checkHand(self, jointsList):
        delta = 0.11
        leftWristX = jointsList[PyKinectV2.JointType_WristLeft].Position.x
        leftWristY = jointsList[PyKinectV2.JointType_WristLeft].Position.y
        (x1,x2) = (leftWristX - delta, leftWristX + delta)
        (y1,y2) = (leftWristY - delta, leftWristY + delta)
        xTest = jointsList[PyKinectV2.JointType_HandTipLeft].Position.x
        yTest = jointsList[PyKinectV2.JointType_HandTipLeft].Position.y
        ##print ("(x1, x2)=", x1, x2)
        ##print ("(y1, y2)=", y1, y2)
        ##print ("xtest=", xTest)
        ##print ("ytest=", yTest)
        if ((x1 <= xTest and xTest <= x2) and (y1 <= yTest and yTest <= y2)):
            return True
        return False

    def getHandPos(self, joints):
        #leftWristX = jointsList[PyKinectV2.JointType_WristLeft].Position.x
        #leftWristY = jointsList[PyKinectV2.JointType_WristLeft].Position.y

        jointPoints = self._kinect.body_joints_to_color_space(joints)

        x = jointPoints[PyKinectV2.JointType_HandLeft].x
        y = jointPoints[PyKinectV2.JointType_HandLeft].y

        print(ctypes.c_int(PyKinectV2._HandState).value)

        return (x, y)





    def draw_body(self, joints, jointPoints, color):
        #pagh
        #pagh = pygame.image.load(os.path.join('data', 'PAGG.png'))
        #self.draw_pagh(joints, jointPoints)

        # Torso
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_Head, PyKinectV2.JointType_Neck);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_Neck, PyKinectV2.JointType_SpineShoulder);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_SpineShoulder, PyKinectV2.JointType_SpineMid);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_SpineMid, PyKinectV2.JointType_SpineBase);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_SpineShoulder, PyKinectV2.JointType_ShoulderRight);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_SpineShoulder, PyKinectV2.JointType_ShoulderLeft);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_SpineBase, PyKinectV2.JointType_HipRight);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_SpineBase, PyKinectV2.JointType_HipLeft);
    
        # Right Arm    
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_ShoulderRight, PyKinectV2.JointType_ElbowRight);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_ElbowRight, PyKinectV2.JointType_WristRight);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_WristRight, PyKinectV2.JointType_HandRight);
        ##self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_HandRight, PyKinectV2.JointType_HandTipRight);
        ##self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_WristRight, PyKinectV2.JointType_ThumbRight);

        # Left Arm
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_ShoulderLeft, PyKinectV2.JointType_ElbowLeft);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_ElbowLeft, PyKinectV2.JointType_WristLeft);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_WristLeft, PyKinectV2.JointType_HandLeft);
        ##self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_HandLeft, PyKinectV2.JointType_HandTipLeft);
        ##self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_WristLeft, PyKinectV2.JointType_ThumbLeft);


        # Right Leg
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_HipRight, PyKinectV2.JointType_KneeRight);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_KneeRight, PyKinectV2.JointType_AnkleRight);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_AnkleRight, PyKinectV2.JointType_FootRight);

        # Left Leg
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_HipLeft, PyKinectV2.JointType_KneeLeft);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_KneeLeft, PyKinectV2.JointType_AnkleLeft);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_AnkleLeft, PyKinectV2.JointType_FootLeft);


    def draw_color_frame(self, frame, target_surface):
        target_surface.lock()
        address = self._kinect.surface_as_array(target_surface.get_buffer())
        ctypes.memmove(address, frame.ctypes.data, frame.size)
        del address
        target_surface.unlock()

    


    def run(self):
        ######## Saving Data Values ########
        mainDict = dict()
        mainDict[11] = [] #Left Wrist
        mainDict[12] = [] #Left Elbow
        mainDict[13] = [] #Left Shoulder
        mainDict[21] = [] #Right Wrist
        mainDict[22] = [] #Right Elbow
        mainDict[23] = [] #Right Shoulder
        mainDict[31] = [] #Left Ankle
        mainDict[32] = [] #Left Knee
        mainDict[33] = [] #Left Hip
        mainDict[41] = [] #Right Ankle
        mainDict[42] = [] #Right Knee
        mainDict[43] = [] #Right Hip
        mainDict[99] = [] #Top of Spine
        mainDict[98] = [] #Centre of Spine
        mainDict[96] = [] #Bottom of Spine
        keyList = [11,12,13,21,22,23,31,32,33,41,42,43,99,98,96]
        jointTypes = [PyKinectV2.JointType_WristLeft, PyKinectV2.JointType_ElbowLeft,
                        PyKinectV2.JointType_ShoulderLeft, PyKinectV2.JointType_WristRight,
                        PyKinectV2.JointType_ElbowRight, PyKinectV2.JointType_ShoulderRight,
                        PyKinectV2.JointType_AnkleLeft, PyKinectV2.JointType_KneeLeft,
                        PyKinectV2.JointType_HipLeft, PyKinectV2.JointType_AnkleRight,
                        PyKinectV2.JointType_KneeRight, PyKinectV2.JointType_HipRight,
                        PyKinectV2.JointType_SpineShoulder, PyKinectV2.JointType_SpineMid,
                        PyKinectV2.JointType_SpineBase]
        grandTime = 0



        

        # -------- Main Program Loosp -----------
        while not self._done:
            # --- Main event loop

            for event in pygame.event.get(): # User did something
                if event.type == pygame.QUIT: # If user clicked close
                    #print(mainDict[11])  # testing dict values by printing
                    #print()
                    #print(mainDict[99])
                    #fout = open('saveFile.pkl', 'wb') #creating save file #pickledump
                    #dump( mainDict, fout, protocol = 2)
                    #fout.close()
                    self._done = True # Flag that we are done so we exit this loop

                elif event.type == pygame.VIDEORESIZE: # window resized
                    self._screen = pygame.display.set_mode(event.dict['size'], 
                                               pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE, 32)
                    
            # --- Game logic should go here

            # --- Getting frames and drawing  
            # --- Woohoo! We've got a color frame! Let's fill out back buffer surface with frame's data 
            if self._kinect.has_new_color_frame():
                frame = self._kinect.get_last_color_frame()
                self.draw_color_frame(frame, self._frame_surface)
                frame = None

            # --- Cool! We have a body frame, so can get skeletons
            if self._kinect.has_new_body_frame(): 
                self._bodies = self._kinect.get_last_body_frame()

            # --- draw skeletons to _frame_surface
            if self._bodies is not None: 
                for i in range(0, self._kinect.max_body_count):
                    body = self._bodies.bodies[i]
                    if not body.is_tracked: 
                        continue 
                    
                    joints = body.joints 
                    # convert joint coordinates to color space 
                    joint_points = self._kinect.body_joints_to_color_space(joints)
                   
                    

                    ####### main loop to save coordinates & time #######
                    jointsList = body.joints
                    grandTime += self._clock.get_time()
                    counter = 0 # which index pf the jointTypes should be accessed
                    for key in keyList:
                        jointType = jointTypes[counter] # type of joint
                        jointPos = jointsList[jointType].Position # position of that joint
                        val = (jointPos.x, jointPos.y, jointPos.z, grandTime)
                        mainDict[key].append(val)
                        counter += 1

                    self.draw_body(joints, joint_points, SKELETON_COLORS[i])


                   

                    #if (abs(leftTip-leftWrist) <= delta):
                    #   print("Peepadoo")

                    if (self.checkHand(jointsList)):
                        #print ("hand closed")
                        (x,y) = self.getHandPos(joints)
                        self.img = pygame.image.load('xMarksTheSpot.png')
                        (width,height) = self.img.get_size()
                        (x0,y0) = (x-width/2,y-height/2)
                        self._frame_surface.blit(self.img, (x0,y0))
       
                        
                    TAKE_SCREENSHOT = True
                    ##print (PyKinectV2.HandState_NotTracked)
                    if (TAKE_SCREENSHOT):
                        pygame.image.save(self._frame_surface, "startPage.jpeg")
                        TAKE_SCREENSHOT = False
                        



            # --- copy back buffer surface pixels to the screen, resize it if needed and keep aspect ratio
            # --- (screen size may be different from Kinect's color frame size) 
            h_to_w = float(self._frame_surface.get_height()) / self._frame_surface.get_width()
            target_height = int(h_to_w * self._screen.get_width())
            surface_to_draw = pygame.transform.scale(self._frame_surface, (self._screen.get_width(), target_height));
            self._screen.blit(surface_to_draw, (0,0))
            surface_to_draw = None
            pygame.display.update()

            
            

            # --- Go ahead and update the screen with what we've drawn.
            pygame.display.flip()

            
            
            


            # --- Limit to 60 frames per second
            self._clock.tick(20)


        # Close our Kinect sensor, close the window and quit.
        self._kinect.close()
        pygame.quit()


__main__ = "Kinect v2 Body Game"
game = BodyGameRuntime();
game.run();

