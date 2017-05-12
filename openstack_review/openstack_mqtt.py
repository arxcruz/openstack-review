import logging
import paho.mqtt.client as mqtt
import json
import re

import gerrit

from gi.repository import GLib

from jenkins_info import JenkinsInfo

LOG = logging.getLogger(__name__)


class OpenstackMqtt():
    def __init__(self, jenkins_list):
        self.client = mqtt.Client()
        self.jenkins_list = jenkins_list

        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        self.client.connect('firehose.openstack.org')

    def on_connect(self, client, userdata, flags, rc):
        LOG.debug('Connected with result code ' + str(rc))
        self.add_subscribe('openstack/tripleo-quickstart')
        self.add_subscribe('openstack/tripleo-quickstart-extras')
        self.add_subscribe('openstack/nova')

    def add_subscribe(self, project):
        self.client.subscribe('gerrit/{}/change-abandoned'.format(project))
        self.client.subscribe('gerrit/{}/change-merged'.format(project))
        self.client.subscribe('gerrit/{}/comment-added'.format(project))
        self.client.subscribe('gerrit/{}/topic-changed'.format(project))
        self.client.subscribe('gerrit/{}/merge-failed'.format(project))

    def on_message(self, client, userdata, msg):
        GLib.idle_add(self._on_message, client, userdata, msg)

    def _on_message(self, client, userdata, msg):
        LOG.debug('New message received: {}'.format(msg.topic))
        payload = json.loads(str(msg.payload))
        topic = msg.topic[msg.topic.rfind('/')+1:]
        info = None

        if payload.get('change', None):
            info = JenkinsInfo()
            info.url = payload['change']['url']
            info.change_id = payload['change']['id']
            info.verified = self.is_verified(payload)
            info.subject = payload['change']['subject']
            info.description = self.parse_commit_message(
                    payload['change']['commitMessage'])

        if not self.jenkins_list.contains(info):
            info.verified = gerrit.get_verified_from_gerrit(info.change_id)
        if topic == 'change-merged':
            self.jenkins_list.del_jenkins_info(info)
        else:
            self.jenkins_list.add_jenkins_info(info)

    def is_verified(self, payload):
        comment = payload.get('comment', None)
        author = payload.get('author', {}).get('username', None)

        if not comment or not author:
            return False

        if 'Verified+1' in comment and author == 'jenkins':
            print 'Verified'
            return True
        else:
            return False

    def parse_commit_message(self, commit_message):
        new_message = re.sub(r'^.*\n', '', commit_message)
        new_message = re.sub(r'\nChange-Id.*', '', new_message)
        return new_message

    def start(self):
        self.client.loop_start()
