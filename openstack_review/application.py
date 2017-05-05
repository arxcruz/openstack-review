import gi

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk
from jenkins_list_view import JenkinsListBox
from jenkins_info_list import JenkinsInfoList
from gobject_worker import GObjectWorker
from openstack_mqtt import OpenstackMqtt


class ListBoxWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Openstack Review")
        self.set_border_width(10)
        info_list = JenkinsInfoList()

        box_outer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(box_outer)

        listbox = JenkinsListBox(info_list)
        listbox.set_selection_mode(Gtk.SelectionMode.NONE)

        scroll = Gtk.ScrolledWindow()
        scroll.set_vexpand(False)
        box_outer.pack_start(scroll, True, True, 0)
        scroll.add(listbox)

        self.worker = GObjectWorker()
        self.mqtt = OpenstackMqtt(info_list)
        self.worker.send(self.mqtt.start)
        self.set_default_size(300, 600)


win = ListBoxWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
