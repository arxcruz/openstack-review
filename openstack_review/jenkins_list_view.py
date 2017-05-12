import logging

from gi.repository import Gtk

from jenkins_row import JenkinsRow

LOG = logging.getLogger(__name__)


class JenkinsListBox(Gtk.ListBox):
    def __init__(self, info_list):
        Gtk.ListBox.__init__(self)
        self.info_list = info_list
        self.info_list.connect('jenkins-info-added',
                               self.on_jenkins_info_added_cb)
        self.info_list.connect('jenkins-info-deleted',
                               self.on_jenkins_info_deleted_cb)
        self.set_sort_func(self.sort_func, None, False)

    def on_jenkins_info_added_cb(self, obj, jenkins_info):
        LOG.debug('Row added with info: {}'.format(jenkins_info))
        row = JenkinsRow(jenkins_info)
        self.insert(row, 0)
        row.show_all()

    def on_jenkins_info_deleted_cb(self, obj, jenkins_info):
        LOG.debug('Row deleted with info: {}'.format(jenkins_info))
        childrens = self.get_children()
        for row in childrens:
            print 'Checking to delete change: {}'.format(
                    row.jenkins_info.change_id)
            if row.jenkins_info == jenkins_info:
                row.destroy()

    def sort_func(self, row1, row2, data, notify_destroy):
        LOG.debug('Entering sort_func')
        LOG.debug('Row 1: {}'.format(row1.jenkins_info))
        LOG.debug('Row 2: {}'.format(row2.jenkis_info))
        if row1.jenkins_info.verified > row2.jenkis_info.verified:
            return -1
        elif row1.jenkis_info.verified < row2.jenkis_info.verified:
            return 1
        else:
            return 0
