import json
import logging
import requests


LOG = logging.getLogger(__name__)
REVIEW = 'https://review.openstack.org'


def get_verified_from_gerrit(change_id):
    r = requests.get('{}/changes/{}/detail'.format(REVIEW, change_id))
    if r.status_code == 200:
        content = json.loads(r.content.replace(')]}\'', ''))
        users = content.get('labels', {}).get('Verified', {}).get('all', [])
        verified = -1
        for user in users:
            if user['username'] == 'jenkins':
                LOG.debug('User jenkins found')
                verified = user.get('value', -1)
                LOG.debug('Verified value: {}'.format(verified))
                break
        if verified == 1:
            return True
        return False
    else:
        return False
