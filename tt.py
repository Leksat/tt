#!/usr/bin/env python
import sys
import gtk
import appindicator
import time

class TT:
    def __init__(self):
        self.seconds = 0
        self.ind = appindicator.Indicator("tt-indicator", "clock", appindicator.CATEGORY_APPLICATION_STATUS)
        self.ind.set_status(appindicator.STATUS_ACTIVE)
        self.menu_setup()

    def main(self):
        gtk.main()

    def update_label(self):
        self.seconds = int(time.time() - self.start_time)
        self.ind.set_label(time.strftime("%H:%M:%S", time.gmtime(self.seconds)))
        return True

    def parse_time_string(self, string):
        parts = string.split(':')
        if len(parts) != 3:
            return 0
        return int(parts[0])*60*60 + int(parts[1])*60 + int(parts[2]);

    def menu_setup(self):
        self.menu = gtk.Menu()
        self.menu_items = {
            'start': gtk.MenuItem("Start"),
            'pause': gtk.MenuItem("Pause"),
            'edit': gtk.MenuItem("Edit"),
            'clear': gtk.MenuItem("Clear"),
            'quit': gtk.MenuItem("Quit"),
        }
        keys = ['start', 'pause', 'edit', 'clear', 'quit']  # To get right order.

        for key in keys:
            self.menu_items[key].connect("activate", getattr(self, 'menu_' + key))
            self.menu_items[key].show()
            self.menu.append(self.menu_items[key])

        self.menu_items['pause'].set_sensitive(False)

        self.ind.set_menu(self.menu)

    def menu_start(self, widget):
        self.start_time = time.time() - self.seconds
        self.timer_id = gtk.timeout_add(1000, self.update_label)
        self.menu_items['start'].set_sensitive(False)
        self.menu_items['pause'].set_sensitive(True)

    def menu_pause(self, widget):
        gtk.timeout_remove(self.timer_id)
        self.menu_items['pause'].set_sensitive(False)
        self.menu_items['start'].set_sensitive(True)

    def menu_edit(self, widget):
        prompt = gtk.MessageDialog(None, 0, gtk.MESSAGE_QUESTION, gtk.BUTTONS_OK_CANCEL, 'Edit time')
        entry = gtk.Entry()
        entry.set_text(time.strftime("%H:%M:%S", time.gmtime(self.seconds)))
        prompt.vbox.add(entry)
        prompt.show_all()
        prompt.run()
        text = entry.get_text()
        prompt.destroy()
        self.start_time = time.time() - self.parse_time_string(text)
        self.update_label()

    def menu_clear(self, widget):
        self.start_time = time.time()
        self.update_label()

    def menu_quit(self, widget):
        sys.exit(0)

if __name__ == "__main__":
    tt = TT()
    tt.main()
