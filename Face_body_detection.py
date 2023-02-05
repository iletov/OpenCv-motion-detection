import cv2
import time
import datetime

video = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# face detection
face_cas = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# body detection
body_cas = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_fullbody.xml')

detection = False
detection_stopped_time = None
timer_started = False
SECCOND_TO_RECORD_AFTER_DETECTION = 7

frame_size = (int(video.get(3)), int(video.get(4)))
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter()

while True:
    ret, frame = video.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cas.detectMultiScale(gray,
                                      scaleFactor =1.4,
                                      minNeighbors = 5)
    body = body_cas.detectMultiScale(gray, 1.4, 5)

    if len(faces) + len(body) > 0:
        if detection:
            timer_started = False
        else:
            detection = True
            current_time = datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
            out = cv2.VideoWriter(f'{current_time}.avi', fourcc, 20, frame_size)
            print('Recording...')
    elif detection:
        if timer_started:
            if time.time() - detection_stopped_time >= SECCOND_TO_RECORD_AFTER_DETECTION:
                detection = False
                timer_started = False
                out.release()
                print('Stopped!')
        else:
            timer_started = True
            detection_stopped_time = time.time()

    if detection:
        out.write(frame)

    cv2.imshow("camera", frame)
    if cv2.waitKey(1) == ord('q'):
        break

out.release()
video.release()
cv2.destroyAllWindows()
