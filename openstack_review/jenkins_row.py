from gi.repository import Gtk
from gi.repository import GObject

from gi_composites import GtkTemplate

from jenkins_info import JenkinsInfo

import logging
import sys
from os.path import join, dirname
sys.path.insert(0, join(dirname(__file__), '..', '..'))

LOG = logging.getLogger(__name__)


@GtkTemplate('data/gtk/jenkins_row.ui')
class JenkinsRow(Gtk.ListBoxRow):

    __gtype_name__ = 'JenkinsRow'
    subject = GtkTemplate.Child()
    description = GtkTemplate.Child()
    revealer = GtkTemplate.Child()
    project = GtkTemplate.Child()
    verified = GtkTemplate.Child()
    url = GtkTemplate.Child()
    reveal_description = GtkTemplate.Child()

    def __init__(self, j_info):
        super(Gtk.ListBoxRow, self).__init__()
        self.init_template()

        self.url.set_label('Review this change')
        self.textbuffer = self.description.get_buffer()
        self.jenkins_info = j_info

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

    @GtkTemplate.Callback
    def on_reveal_description_toggled(self, widget):
        toggled = self.reveal_description.get_active()
        if toggled:
            self.reveal_description.set_label('Hide details')
        else:
            self.reveal_description.set_label('Show details')
        self.revealer.set_reveal_child(toggled)

    def _set_verified_image(self, obj):
        if obj.verified:
            self.verified.set_from_stock('gtk-yes', Gtk.IconSize.BUTTON)
        else:
            self.verified.set_from_stock('gtk-no', Gtk.IconSize.BUTTON)

    def on_notify_verify(self, obj, gparamstring):
        self._set_verified_image(obj)
        self.changed()
