import paho.mqtt.client as mqtt
import json
import re

from jenkins_info import JenkinsInfo


class OpenstackMqtt():
    def __init__(self, jenkins_list):
        self.client = mqtt.Client()
        self.jenkins_list = jenkins_list

        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def on_connect(self, client, userdata, flags, rc):
        print('Connected with result code ' + str(rc))
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
        print('New message: {}'.format(msg.topic)) 
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
        self.client.connect('firehose.openstack.org')
        self.client.loop_forever()
