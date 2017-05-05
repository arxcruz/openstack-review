from gi.repository import Gtk

from jenkins_row import JenkinsRow


class JenkinsListBox(Gtk.ListBox):
    def __init__(self, info_list):
        Gtk.ListBox.__init__(self)
        self.info_list = info_list
        self.info_list.connect('jenkins-info-added',
                               self.on_jenkins_info_added_cb)
        self.info_list.connect('jenkins-info-deleted',
                               self.on_jenkins_info_deleted_cb)

    def on_jenkins_info_added_cb(self, obj, jenkins_info):
        # Add row
        print 'Entrou'
        row = JenkinsRow(jenkins_info)
        self.insert(row, 0)
        row.show_all()

    def on_jenkins_info_deleted_cb(self, obj, jenkins_info):
        childrens = self.get_children()
        for row in childrens:
            print 'Checking to delete change: {}'.format(
                    row.jenkins_info.change_id)
            if row.jenkins_info == jenkins_info:
                row.destroy()
