from gi.repository import GObject

from jenkins_info import JenkinsInfo


class JenkinsInfoList(GObject.GObject):

    __gsignals__ = {
        'jenkins-info-changed': (GObject.SIGNAL_RUN_LAST, None,
                                 (JenkinsInfo,)),
        'jenkins-info-added': (GObject.SIGNAL_RUN_LAST, None, (JenkinsInfo,)),
        'jenkins-info-deleted': (GObject.SIGNAL_RUN_LAST, None, (JenkinsInfo,))
    }

    def __init__(self):
        GObject.GObject.__init__(self)
        self.jenkins_dict = dict()

    def contains(self, info):
        return info.change_id in self.jenkins_dict

    def update_jenkins_info(self, info):
        if type(info) is JenkinsInfo:
            old_info = self.jenkins_dict[info.change_id]
            old_info.url = info.url
            old_info.description = info.description
            old_info.subject = info.subject
            old_info.verified = info.verified

            self.emit('jenkins-info-changed', info)

    def add_jenkins_info(self, info):
        if type(info) is JenkinsInfo:
            if self.contains(info):
                self.update_jenkins_info(info)
            else:
                self.jenkins_dict[info.change_id] = info
                self.emit('jenkins-info-added', info)

    def del_jenkins_info(self, info):
        if type(info) is JenkinsInfo:
            del self.jenkins_dict[info.change_id]
            self.emit('jenkins-info-deleted', info)

    def del_jenkins_info_by_change_id(self, change_id):
        if change_id in self.jenkins_dict:
            info = self.jenkins_dict[change_id]
            del self.jenkins_dict[change_id]
            self.emit('jenkins-info-deleted', info)
