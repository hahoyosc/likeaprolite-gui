import tkinter
from PIL import Image, ImageTk
from cv2 import cv2


def goal():
    print("There was a goal.")


def shoot():
    print("There was a shoot.")


def outstanding_play():
    print("There was an outstanding play.")


def corner():
    print("There was a corner.")


def fault():
    print("There was a fault.")


def penalty():
    print("There was a penalty.")


def resize_ratio(ratio, width, height):
    # Calculate the ratio of the width from percentage.
    reduction = ((100 - ratio) / 100) * width
    ratio = reduction / float(width)
    # Construct the dimensions.
    return int(reduction), int(height * ratio)


class App:
    def __init__(self, window):
        self.window = window
        self.window.title("Like a Pro Lite")
        self.video_source1 = 0
        self.video_source2 = 1
        self.photo1 = ""
        self.photo2 = ""
        self.width, self.height = resize_ratio(0, 640, 480)

        # open video source
        self.vid1 = MyVideoCapture()

        # Create a canvas that can fit the above video source size
        self.canvas1 = tkinter.Canvas(window, width=self.width, height=self.height)
        self.canvas2 = tkinter.Canvas(window, width=self.width, height=self.height)
        self.canvas1.grid(column=0, row=0)
        self.canvas2.grid(column=1, row=0)

        # Buttons
        self.goal_button = tkinter.Button(window, text="Gol", width=45, command=goal)
        self.goal_button.grid(column=0, row=1, padx=5, pady=5)
        self.shoot_button = tkinter.Button(window, text="Tiro al arco", width=45, command=shoot)
        self.shoot_button.grid(column=1, row=1, padx=5, pady=5)
        self.outstanding_play_button = tkinter.Button(window, text="Jugada destacada", width=45,
                                                      command=outstanding_play)
        self.outstanding_play_button.grid(column=0, row=2, padx=5, pady=5)
        self.corner_button = tkinter.Button(window, text="Corner", width=45, command=corner)
        self.corner_button.grid(column=1, row=2, padx=5, pady=5)
        self.fault_button = tkinter.Button(window, text="Falta", width=45, command=fault)
        self.fault_button.grid(column=0, row=3, padx=5, pady=5)
        self.penalty_button = tkinter.Button(window, text="Penalty", width=45, command=penalty)
        self.penalty_button.grid(column=1, row=3, padx=5, pady=5)

        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 1
        self.update()

        self.window.mainloop()

    def update(self):
        # Get a frame from the video source
        ret1, frame1, ret2, frame2 = self.vid1.get_frame
        frame1 = cv2.resize(frame1, (self.width, self.height))
        frame2 = cv2.resize(frame2, (self.width, self.height))

        if ret1 and ret2:
            self.photo1 = ImageTk.PhotoImage(image=Image.fromarray(frame1))
            self.photo2 = ImageTk.PhotoImage(image=Image.fromarray(frame2))
            self.canvas1.create_image(0, 0, image=self.photo1, anchor=tkinter.NW)
            self.canvas2.create_image(0, 0, image=self.photo2, anchor=tkinter.NW)

        self.window.after(self.delay, self.update)


class MyVideoCapture:
    def __init__(self):
        # Open the video source
        self.vid1 = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.vid2 = cv2.VideoCapture(1, cv2.CAP_DSHOW)
        self.width = 640
        self.height = 480
        self.fps = 30.0
        self.fourcc = cv2.VideoWriter_fourcc(*'XVID')

        self.writer1 = cv2.VideoWriter(
            filename="./cam1.avi",
            fourcc=self.fourcc,
            fps=self.fps,
            frameSize=(self.width, self.height))
        self.writer2 = cv2.VideoWriter(
            filename="./cam2.avi",
            fourcc=self.fourcc,
            fps=self.fps,
            frameSize=(self.width, self.height))

        if not self.vid1.isOpened():
            raise ValueError("Unable to open video source 0")

        if not self.vid2.isOpened():
            raise ValueError("Unable to open video source 1")

    @property
    def get_frame(self):
        ret1 = None
        ret2 = None
        if self.vid1.isOpened() and self.vid2.isOpened():
            ret1, frame1 = self.vid1.read()
            ret2, frame2 = self.vid2.read()
            #frame1 = cv2.resize(frame1, (self.width, self.height))
            #frame2 = cv2.resize(frame2, (self.width, self.height))

            if ret1 and ret2:
                # Return a boolean success flag and the current frame converted to BGR
                self.save_frame(frame1, frame2)
                return ret1, cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB), ret2, cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB)
            else:
                return ret1, None, ret2, None
        else:
            return ret1, None, ret2, None

    def save_frame(self, frame1, frame2):
        self.writer1.write(frame1)
        self.writer2.write(frame2)

    # Release the video source when the object is destroyed
    def __del__(self):
        if self.vid1.isOpened():
            self.vid1.release()
            self.writer1.release()
        if self.vid2.isOpened():
            self.vid2.release()
            self.writer2.release()


# Create a window and pass it to the Application object
App(tkinter.Tk())
