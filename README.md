# Home Security System - Motion Detector

Home Security System what you can control from a website.

Detects motion with a simple (and cheap) webcamera connected to a Raspberry Pi,
and if it detects motion, the pictures are uploaded to a Firebase project storage.

[Read more about the project here](https://gaborvecsei.wordpress.com/2017/03/07/home-security-system-with-computer-vision/)

-------------------------

## Setup

What you will need:

- Raspberry Pi (but you can test it on your laptop/PC,
or any other device which can run Python scripts and the hardware is enough for image processing tasks)
- Webcamera (simple and cheap)
- Firebase Project

### Setup Firebase Project

We need to setup a Firebase project. This is a simple way to authenticate users and store captured images.

1. Go to [https://console.firebase.google.com/](https://console.firebase.google.com/)
2. Create a new Project (I named it `Home Security`)
3. Setup Authentication:
    1. Enable Email/Password user authentication
    2. Add users (for yourself, your mom, dad, etc...) - They will be able to start or stop the security system
4. Save `apiKey, authDomain, databaseURL, storageBucket, messagingSenderId` and fill out `config.ini`

<img  height=250 src="https://github.com/gaborvecsei/Home-Security/blob/master/images/create_firebase_project.jpg" />
<img  height=250 src="https://github.com/gaborvecsei/Home-Security/blob/master/images/firebase_authentication.jpg" />

### Install

You can use Anaconda to simplify the steps

- Python 3 (but it works with Python 2 too)
- [OpenCV 3 (better) or OpenCV 2](http://opencv.org/)
- [Pyrebase](https://github.com/thisbejim/Pyrebase) - `pip install pyrebase`
- Flask - `pip install flask`

After these steps, you are ready to run the code!

--------------------------

## Test

You just have to run `app_home_security.py` -> `python app_home_security.py`.

Now, find out the *local ip address* of your device which runs the Home Security System (for example `192.168.0.12`).
With another device like your smartphone, laptop, etc... open your browser and go to `192.168.0.12:5000` to see the welcome page.

Go to `192.168.0.12:5000/login` or navigate there from the homepage and you can start the fun with your own Home Security system!

* Enter your *email* and *password*
* Enter the *minimum detection area* (the smaller the value the more it is sensitive for movements, changes on the captured image)
* Choose to *start* or *stop* the system

If the System detects movement it will snap a picture and upload to your Firebase project.

<img  height=250 src="https://github.com/gaborvecsei/Home-Security/blob/master/images/firebase_storage.jpg" />

--------------------------

## Extend Home Security

If you would like to make other things happen when it detects motion than you can edit
`home_security.py` which you can find at:

```
HomeSecurityModules/
    HomeSecurity/
        home_security.py
        __init__.py
```

For example you can create a method which not just uploads the image to the Firebase project storage,
but it sends you a message, email, notification.

I provided a simple notification class with *Slack*. This sends you a message after motion is detected. You only have to
install the `slackclient` package and put the necessary code to `home_security.py`.

--------------------------

## Computer Vision

Here you can see the main steps of the motion detector. You can read more about this part at [this blog post](https://gaborvecsei.wordpress.com/2017/03/07/home-security-system-with-computer-vision/)

<img  width=400 src="https://github.com/gaborvecsei/Home-Security/blob/master/images/preprocessing.jpg" />

<img  width=200 src="https://github.com/gaborvecsei/Home-Security/blob/master/images/previous_image.jpg" />

<img  width=400 src="https://github.com/gaborvecsei/Home-Security/blob/master/images/difference_binary.jpg" />

--------------------------

## Images

<img  height=350 src="https://github.com/gaborvecsei/Home-Security/blob/master/images/index_page.jpg" />
<img  height=350 src="https://github.com/gaborvecsei/Home-Security/blob/master/images/login_form.jpg" />

<img  height=350 src="https://github.com/gaborvecsei/Home-Security/blob/master/images/raspberry_pi.jpg" />

--------------------------
