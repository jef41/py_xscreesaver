#!/usr/bin/python

import os
import sys

import gtk
from gtk import gdk
from datetime import datetime
from random import random
#import time

# mostly taken from http://alvinalexander.com/python/python-screensaver-xscreensaver-linux/
# the secret sauce is to get the "window id" out of $XSCREENSAVER_WINDOW
# code comes from these two places:
# 1) http://pastebin.com/nSCiq1P3
# 2) http://stackoverflow.com/questions/4598581/python-clutter-set-display

class ScreenSaverWindow(gtk.Window):

    def __init__(self):
        gtk.Window.__init__(self)
        self.location = None
        self.label = None
        pass

    def realize(self):
        if self.flags() & gtk.REALIZED:
            return

        ident = os.environ.get('XSCREENSAVER_WINDOW')
        if not ident is None:
            print 'if not ident is None:'
            self.window = gtk.gdk.window_foreign_new(int(ident, 16))
            self.window.set_events (gdk.EXPOSURE_MASK | gdk.STRUCTURE_MASK)
            # added by aja
            x, y, w, h, depth = self.window.get_geometry()
            self.size_allocate(gtk.gdk.Rectangle(x, y, w, h))
            self.set_default_size(w, h)
            self.set_decorated(False)
            # aja - more
            self.window.set_user_data(self)
            self.style.attach(self.window)
            self.set_flags(self.flags() | gtk.REALIZED)
            #self.window.connect("destroy", self.destroy)

        if self.window == None:
            print 'self.window == None:'
            self.window = gdk.Window(None, 1024, 768, gdk.WINDOW_TOPLEVEL,
                                     (gdk.EXPOSURE_MASK | gdk.STRUCTURE_MASK),
                                     gdk.INPUT_OUTPUT)

        if self.window != None:
            print 'self.window != None:'
            #self.window.add_filter(lambda *args: self.filter_event(args))
            self.set_flags(self.flags() | gtk.REALIZED)
            
    def update(self):
        now = datetime.now()
        lblText = now.strftime("%A %H:%M:%S")+"\nwaiting for video to start"
        self.label.set_markup("<span foreground=\"yellow\" size=\"50000\" weight=\"5000\">"+lblText+"</span>")
        return True  #needed to keep the update method in the schedule
    def move(self):
        self.remove(self.location)
        #self.remove(self.label)
        self.location = gtk.Alignment(random(),random(), 0, 0)
        self.location.add(self.label)
        self.location.show()
        self.label.show()
        self.add(self.location)
        return True  #needed to keep the update method in the schedule
        
def main():
    gtk.main()

if __name__ == "__main__":
    window = ScreenSaverWindow()
    window.set_title('Floaters')
    window.connect('delete-event', gtk.main_quit)
    window.set_default_size(1024, 768)
    window.realize()
    window.modify_bg(gtk.STATE_NORMAL, gdk.color_parse("black"))
    now = datetime.now()
    lblText = now.strftime("%A %H:%M")+"\nwaiting for video to start"
    window.label = gtk.Label()
    #position = gtk.Alignment(0.1,0.25, 0, 0)
    window.location = gtk.Alignment(random(),random(), 0, 0)
    window.label.set_markup("<span foreground=\"yellow\" size=\"50000\" weight=\"5000\">"+lblText+"</span>")
    window.location.add(window.label)
    window.location.show()
    window.label.show()
    window.add(window.location)
    window.show()
    gtk.timeout_add(200, window.update)    
    gtk.timeout_add(60000, window.move)
    main()
