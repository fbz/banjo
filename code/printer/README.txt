Howdy y'all,

These are the scripts for handling the printer. Kind thanks are due to
Steve Conklin, Limor Fried, and Becky Stern.  Run './print foo.bmp' to
print an arbitrary image, then kill PDDemulate-1.0.py once the image
has been loaded.  restart_arduino is a Perl script that restarts the
arduino, causing it to load a new image from track 1, pattern 903 of
the disk.  If the disk process is not restarted, the old pattern will
load.  (This could be patched, of course.)

Happy hacking,
--Travis Goodspeed
travis at radiantmachines.com

