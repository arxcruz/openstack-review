from gi.repository import Gtk
from gi.repository import GObject

from jenkins_info import JenkinsInfo


class JenkinsRow(Gtk.ListBoxRow):
    def __init__(self, j_info):
        self.j_info = None
        Gtk.ListBoxRow.__init__(self)
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.image = Gtk.Image.new_from_stock('gtk-no', Gtk.IconSize.BUTTON)
        self.subject = Gtk.Label()
        self.subject.set_line_wrap(True)
        self.subject.set_xalign(0)
        self.subject.set_use_markup(True)
        self.description = Gtk.Label()
        self.description.set_line_wrap(True)
        self.description.set_xalign(0)
        self.url = Gtk.LinkButton()
        self.url.set_label('Review this change')

        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        hbox.pack_start(self.image, False, False, 6)
        hbox.pack_start(self.subject, False, False, 6)
        box.pack_start(hbox, True, True, 0)
        expander = Gtk.Expander.new('Details')
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        hbox.pack_start(self.description, True, True, 6)
        expander.add(hbox)
        box.pack_start(expander, True, True, 6)
        box.pack_start(self.url, True, True, 6)
        self.jenkis_info = j_info
        self.add(box)

    @GObject.Property(type=JenkinsInfo)
    def jenkins_info(self):
        return self.j_info

    @jenkins_info.setter
    def jenkis_info(self, value):
        self.j_info = value
        self.j_info.subject = '<b>{}</b>'.format(self.j_info.subject)
        self.j_info.bind_property('subject', self.subject, 'label',
                                  GObject.BindingFlags.DEFAULT |
                                  GObject.BindingFlags.SYNC_CREATE)
        self.j_info.bind_property('description', self.description, 'label',
                                  GObject.BindingFlags.DEFAULT |
                                  GObject.BindingFlags.SYNC_CREATE)
        self.j_info.bind_property('url', self.url, 'uri',
                                  GObject.BindingFlags.DEFAULT |
                                  GObject.BindingFlags.SYNC_CREATE)
        self.j_info.connect('notify::verified', self.on_notify_verify)

    def on_notify_verify(self, obj, gparamstring):
        print 'Change status: {}'.format(obj.verified)
        if obj.verified:
            self.image.set_from_stock('gtk-yes', Gtk.IconSize.BUTTON)
        else:
            self.image.set_from_stock('gtk-no', Gtk.IconSize.BUTTON)
