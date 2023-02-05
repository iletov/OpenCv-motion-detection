import cv2
import time
import datetime

video = cv2.VideoCapture(0, cv2.CAP_DSHOW)
time.sleep(2)


recording = False
stop_recording = None
timer = False
SEC_AFTER = 3

first_frame = None
#status_list=[None, None]
#times = []

frame_size = (int(video.get(3)), int(video.get(4)))
fourcc = cv2.VideoWriter_fourcc(*'XVID')
#out = cv2.VideoWriter()

while True:
    ret, frame = video.read()
    status = 0

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21,21),0)
    if first_frame is None:
        first_frame = gray
        continue

    delta_frame = cv2.absdiff(first_frame, gray)
    thresh_frame = cv2.threshold(delta_frame, 5, 255,
                                 cv2.THRESH_BINARY)[1]
    thresh_frame = cv2.dilate(thresh_frame, None, iterations = 2)
    (cnts,_) = cv2.findContours(thresh_frame.copy(),
                                 cv2.RETR_EXTERNAL,
                                 cv2.CHAIN_APPROX_SIMPLE)
    for i in cnts:
        if cv2.contourArea(i) < 25000:
            continue
        status = 1
        (x,y,w,h) = cv2.boundingRect(i)
        cv2.rectangle(frame, (x,y), (x+w, y+h), (80,200,20), 2)

    # 1 когато програмата разпознае движение
    if status == 1:     #8 когато разпознае движение и таймера е включен
        if recording:   #2 когато НЕ Е засечено предишно движение и преминава на 3
                        #9 когато Е засечено предишно движение и таймера не е превишил зададеното време, го изключваме
            timer = False
        else:
        #3 засечено е движение и започва да записва видео
            recording = True
            current_time = datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
            out = cv2.VideoWriter(
                f'{current_time}.avi', fourcc, 30, frame_size)
            print('Recording...')
    elif recording:     #4 джижението спира, вече не засича движение и status ==
        if timer:       #5 проверя дали таймера е стартирал, първоначално НЕ Е стартиран
                        #7 таймера е стартиран и ако надвиши зададеното време, спира записа, ако не - започва отначало и се връща на т1
            if time.time() - stop_recording >= SEC_AFTER:
                recording = False
                timer = False
                out.release()
                print('Stopped!')
        else:       #6 стартира таймера в посоченото време
            timer = True
            stop_recording = time.time()

    if recording:
        out.write(frame)

    cv2.imshow("camera", frame)
    if cv2.waitKey(1) == ord('q'):
        break

out.release()
video.release()
cv2.destroyAllWindows()
