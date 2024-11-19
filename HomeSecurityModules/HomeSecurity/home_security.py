import datetime
import threading
import time

import cv2

STATUS_STOPPED = 0
STATUS_RUNNING = 1


class HomeSecurity:
    def __init__(self, firebase, motion_detector, fps=10, camera_input_code=0):
        self.status = STATUS_STOPPED
        self.firebase = firebase
        self.camera_input_code = camera_input_code
        self.camera = None
        self.motion_detector = motion_detector
        self.fps = fps
        self.detection_thread = None
        self.recording = False  
        self.video_writer = None 
        self.armed = False  

    def login(self, email, password, refresh_time_in_sec):
        succesful_login = self.firebase.authenticate(email, password)
        if succesful_login:
            self.refresh_user_authentication(refresh_time_in_sec)
        return succesful_login

    def refresh_user_authentication(self, time_in_sec):
        """
        We have to refresh our user because after 1 hour the authentication expires, so we need a new one
        This method
        :param time_in_sec: time to execute this function
        """

        self.firebase.refresh_user()
        print("User Token refreshed!")
        threading.Timer(time_in_sec, self.refresh_user_authentication, args=[time_in_sec]).start()

    def start_detection(self):
        self.camera = cv2.VideoCapture(self.camera_input_code)
        while self.status == STATUS_RUNNING:
            time_delta = 1. / self.fps
            time.sleep(time_delta)

            if self.status == STATUS_STOPPED:
                break

            ret, frame = self.camera.read()

            if not ret:
                print("No camera feed")
                continue

            debug_frame = frame.copy()

            is_detected, contour = self.motion_detector.detect(frame)

            if is_detected:
                frame_area = frame.shape[0] * frame.shape[1]
                contour_area = cv2.contourArea(contour)
                area_percentage = (contour_area / frame_area) * 100
                if area_percentage > 80:
                    continue
                print(
                    "Detected with area: {0:.2f} and image percentage: {1:.2f}%".format(contour_area, area_percentage))

                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(debug_frame, (x, y), (x + w, y + h), (0, 255, 0), 1)

                """*********************************
                *
                *       INSERT YOUR CODE HERE
                *
                * If you would like to use your own methods
                * (send email, play alarm sound, etc...), than call it here
                *********************************"""

                image_name = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%f") + ".jpg"
                self.firebase.store_image(image_name, debug_frame)
        print("Detection ended!")

    def get_status_code(self):
        return self.status

    def stop(self):
        if self.detection_thread is not None and self.detection_thread.is_alive():
            self.status = STATUS_STOPPED
            self.camera.release()
            self.camera = None
            self.detection_thread = None

    def start(self):
        if self.detection_thread is None:
            self.status = STATUS_RUNNING
            self.detection_thread = threading.Thread(target=self.start_detection)
            self.detection_thread.start()
    
    def arm(self):
        if not self.armed:
            self.armed = True
            self.start()
            print("System armed and detection started")
            threading.Thread(target=self.generate_frames).start()
            return True
        else:
            print("System is already armed")
            return False

    def disarm(self):
        if self.armed:
            self.armed = False
            self.stop()
            print("System disarmed and detection stopped")
            return True
        else:
            print("System is already disarmed")
            return False

    def start_recording(self):
        if not self.recording:
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            video_name = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%f") + ".avi"
            self.video_writer = cv2.VideoWriter(video_name, fourcc, self.fps, (640, 480))
            self.recording = True
            print("Recording started")
            return True
        else:
            print("Recording is already in progress")
            return False

    def stop_recording(self):
        if self.recording:
            self.recording = False
            self.video_writer.release()
            video_name = self.video_writer.filename
            self.firebase.store_video(video_name)
            print("Recording stopped and video saved to Firebase")
            return True
        else:
            print("No recording in progress to stop")
            return False
    # def generate_frames(self):
    #     try:
    #         while True:
    #             success, frame = self.camera.read()
    #             if not success:
    #                 break
    #             else:
    #                 ret, buffer = cv2.imencode('.jpg', frame)
    #                 frame = buffer.tobytes()
    #                 yield (b'--frame\r\n'
    #                     b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    #     except Exception as e:
    #         print(f"Error in generating frames: {e}")

    def generate_frames(self):
        while True:
            if self.camera is not None and self.camera.isOpened():
                success, frame = self.camera.read()
                if not success:
                    print("Failed to read frame")
                    break
                else:
                    print("Frame read successfully")
                    ret, buffer = cv2.imencode('.jpg', frame)
                    frame = buffer.tobytes()
                    yield (b'--frame\r\n'
                        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            else:
                print("Camera is not open")
                break


        # except Exception as e:
        #         print(f"Error in generating frames: {e}")



