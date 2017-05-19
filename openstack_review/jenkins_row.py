from gi.repository import Gtk
from gi.repository import GObject

from jenkins_info import JenkinsInfo

import logging

LOG = logging.getLogger(__name__)


class JenkinsRow(Gtk.ListBoxRow):
    def __init__(self, j_info):
        css_class = '''
            #subject {
                font-weight: bold;
            }

        '''
        Gtk.ListBoxRow.__init__(self)
        # Red / Green image
        self.image = Gtk.Image.new_from_stock('gtk-no', Gtk.IconSize.BUTTON)

        # Subject label
        self.subject = Gtk.Label()
        self.subject.set_name('subject')
        self.subject.set_line_wrap(True)
        self.subject.set_xalign(0)
        context = self.subject.get_style_context()
        style_provider = Gtk.CssProvider()
        style_provider.load_from_data(css_class)
        context.add_provider(style_provider, Gtk.STYLE_PROVIDER_PRIORITY_USER)

        # Project label
        self.project = Gtk.Label()
        self.project.set_name('project')
        self.project.set_xalign(0)

        # Description text view
        self.description = Gtk.TextView()
        self.textbuffer = self.description.get_buffer()

        # Link button with url to open review
        self.url = Gtk.LinkButton()
        self.url.set_label('Review this change')

        # Boxes
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        hbox.pack_start(self.image, False, False, 6)
        vbox.pack_start(self.subject, False, False, 6)
        vbox.pack_start(self.project, False, False, 6)
        hbox.pack_start(vbox, False, False, 6)
        box.pack_start(hbox, True, True, 0)
        expander = Gtk.Expander.new('Details')
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_size_request(-1, 100)
        scrolled_window.add(self.description)
        hbox.pack_start(scrolled_window, True, True, 6)
        expander.add(hbox)
        box.pack_start(expander, True, True, 6)
        box.pack_start(self.url, True, True, 6)
        self.add(box)
        self.jenkins_info = j_info
        LOG.debug('Row created')

    @GObject.Property(type=JenkinsInfo)
    def jenkins_info(self):
        return self._j_info

    @jenkins_info.setter
    def jenkis_info(self, value):
        LOG.debug('Setting jenkins_info: {}'.format(value))
        self._j_info = value
        self._set_verified_image(self._j_info)
        self._j_info.bind_property('subject', self.subject, 'label',
                                   GObject.BindingFlags.DEFAULT |
                                   GObject.BindingFlags.SYNC_CREATE)
        self._j_info.bind_property('description', self.textbuffer, 'text',
                                   GObject.BindingFlags.DEFAULT |
                                   GObject.BindingFlags.SYNC_CREATE)
        self._j_info.bind_property('url', self.url, 'uri',
                                   GObject.BindingFlags.DEFAULT |
                                   GObject.BindingFlags.SYNC_CREATE)
        self._j_info.bind_property('project', self.project, 'label',
                                   GObject.BindingFlags.DEFAULT |
                                   GObject.BindingFlags.SYNC_CREATE)
        self._j_info.connect('notify::verified', self.on_notify_verify)

    def _set_verified_image(self, obj):
        if obj.verified:
            self.image.set_from_stock('gtk-yes', Gtk.IconSize.BUTTON)
        else:
            self.image.set_from_stock('gtk-no', Gtk.IconSize.BUTTON)

    def on_notify_verify(self, obj, gparamstring):
        self._set_verified_image(obj)
        self.changed()
