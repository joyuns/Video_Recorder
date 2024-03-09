import cv2 as cv
import numpy as np
import datetime


video_URL = 'rtsp://210.99.70.120:1935/live/cctv001.stream' #동영상경로
video = cv.VideoCapture(video_URL)
recoding_path = 'C:/Sample Data/recoding video/' #저장경로
record = False

#동영상의 크기를 저장 [640, 480]
width = video.get(cv.CAP_PROP_FRAME_WIDTH) 
height = video.get(cv.CAP_PROP_FRAME_HEIGHT) 
size = (int(width), int(height))
red_circle_position = (int(width)-30, 30)

#실시간 동영상이 일정한 fps를 제공하지 못하기 때문에 fps를 30으로 고정.
fps = 30 
wait_msec = int(1 / fps * 1000) #밀리초당 대기시간

#마우스 조작
def mouse_handler(event, x, y, flags, param):
    if event == cv.EVENT_LBUTTONDOWN:
          param[0] = True
          param[1] = (x, y)
    elif event == cv.EVENT_LBUTTONUP:
          param[0] = False
    elif event == cv.EVENT_MOUSEMOVE and param[0]:
          param[1] = (x, y)

zoom_level= 5
zoom_box_radius= 20 
zoom_box_margin= 10
mouse_state = [False, (-1, -1)] 

cv.namedWindow('Video Recorder')
cv.setMouseCallback('Video Recorder', mouse_handler, mouse_state)

#동영상 코덱설정
fourcc = cv.VideoWriter_fourcc(*'XVID')

if video.isOpened():
   while True:      
        valid, img = video.read()
        if not valid:
            break
        
        #녹화시 빨간 점 표시
        if record == True:
            recording.write(img)
            cv.circle(img, red_circle_position, radius=20, color=(0,0,255), thickness = -1)

        #원본 이미지 복사
        img_copy = img.copy()

        #마우스 좌클릭을 할때 줌인하는 함수
        mouse_left_button_click, mouse_xy = mouse_state
        if mouse_left_button_click:
            if mouse_xy[0] >= zoom_box_radius and mouse_xy[0] < (width - zoom_box_radius) and \
               mouse_xy[1] >= zoom_box_radius and mouse_xy[1] < (height - zoom_box_radius):
                
                    img_crop = img_crop = img[mouse_xy[1]-zoom_box_radius:mouse_xy[1]+zoom_box_radius, \
                                              mouse_xy[0]-zoom_box_radius:mouse_xy[0]+zoom_box_radius, :]

                
                    zoom_box = cv.resize(img_crop, None, None, zoom_level, zoom_level)
                    h, w, _ = zoom_box.shape
                    img_copy[0:h, 0:w] = zoom_box

        cv.imshow('Video Recorder', img_copy)
                
        #조작키 부분
        key = cv.waitKey(wait_msec)
        if key == 27: #ESC 누르면 종료
            break        
        
        elif key == ord(' '):
            if record == False:
                record = True
                time = datetime.datetime.now().strftime('%d_%H_%M_%S') #현재시간을 string형식으로 저장
                recording = cv.VideoWriter(recoding_path + time + '.avi', fourcc, fps, size)
            
            elif record == True:
                record = False
                recording.release()
                recording = None
                
cv.destroyAllWindows()