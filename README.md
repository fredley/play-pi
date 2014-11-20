#play-pi

A frontend for a [Google Play Music](http://play.google.com/music/) Pi Jukebox. Play-pi will provide a web-frontend that can be used to browse and play your Google Music library.

![Screenshot](http://i.imgur.com/Ar4dqoN.png)

###Setup/Installation:

* Not covered in this guide: Setting up ssh/wireless/sound card. These topics are covered in this [lifehacker guide](http://lifehacker.com/5978594/turn-a-raspberry-pi-into-an-airplay-receiver-for-streaming-music-in-your-living-room).
* Assuming you've got the Pi set up as you want, you'll need to install the required tools:
`sudo apt-get install mpd mpc python-pip screen`
* Test that `mpc` is working by entering the command `sudo mpc`. You should see output like
*volume: 80%   repeat: off   random: off   single: off   consume: off*
There are [futher instructions for setting up/testing mpc](http://www.gmpa.it/it9xxs/?p=727) if you want them.
* Next you'll need to use `pip` to install the required python packages:
`sudo pip install -r requirements.txt`
* Now clone this repository:
`git clone git://github.com/fredley/play-pi.git`
`cd play-pi`
* Create a file called `local_settings.py` in the same folder as `settings.py`. Add the following lines:
`GPLAY_USER="you@gmail.com"`
`GPLAY_PASS="your-password"`
It's highly recommended you use an [application specific password](https://support.google.com/accounts/answer/185833?hl=en) for this.
* Now set up the Django app with the following commands. This will create the database:
`./manage.py syncdb`
During this step you will be asked for a superuser name and password. You can use these to access the admin should you want to.
* Now sync your Google Music library. This can take a very long time, just let it run:
`./manage.py init_gplay`
* You're now ready to roll! Start up a screen by typing `screen`. Running the server in the screen means that it will keep running after `ssh` is disconnected. You need to use `sudo` for this command if you want to use port 80 (recommended).
`sudo ./manage.py runserver 0.0.0.0:80`
* You should now be able to access play-pi from your web browser, point it at the IP of your Pi. You can go to `http://192.168.pi.ip/admin` and log in with your credentials to access the admin.
* Setting up a better web server is left as an excercise for the enthusiast. I can personally recommend [gunicorn](http://gunicorn.org/).
