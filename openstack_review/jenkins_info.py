from gi.repository import GObject


class JenkinsInfo(GObject.GObject):
    url = GObject.Property(type=str, flags=GObject.PARAM_READWRITE)
    change_id = GObject.Property(type=str, flags=GObject.PARAM_READWRITE)
    verified = GObject.Property(type=bool, flags=GObject.PARAM_READWRITE,
                                default=True)
    description = GObject.Property(type=str, flags=GObject.PARAM_READWRITE)
    subject = GObject.Property(type=str, flags=GObject.PARAM_READWRITE)

    def __init__(self):
        GObject.GObject.__init__(self)

    def __str__(self):
        return 'Change-ID: {}, Subject: {}, Verified: {}'.format(self.change_id,
                                                   self.subject, self.verified)
