import requests
import logging
import json

from django.conf import settings

logger = logging.getLogger(__name__)


class Newrelic:
    @staticmethod
    def create_deploy(newrelic_app_id, user, revision):
        Newrelic._log('create_deploy {} {} {}'
                      .format(newrelic_app_id, user, revision))
        newrelic_deploy_url = settings.DEIS_NEWRELIC_CREATE_DEPLOY_URL
        newrelic_deploy_api_key = settings.DEIS_NEWRELIC_CREATE_DEPLOY_API_KEY
        if (newrelic_app_id is not None and newrelic_app_id != '') and \
           (newrelic_deploy_url is not None and newrelic_deploy_url != '') and \
           (newrelic_deploy_api_key is not None and newrelic_deploy_api_key != ''):

            headers = {
                'Content-Type': 'application/json',
                'X-Api-Key': '{api_key}'.format(api_key=newrelic_deploy_api_key)
            }
            payload = {
                'deployment':
                    {
                        'user': user,
                        'revision': revision
                    }
            }

            r = requests.post(url=newrelic_deploy_url.format(application_id=newrelic_app_id),
                              headers=headers,
                              data=json.dumps(payload),
                              timeout=5)
            Newrelic._log('create_deploy done: {}'.format(r.text))
        else:
            Newrelic._log('create_deploy not doing')

    @staticmethod
    def _log(msg):
        logger.log(logging.DEBUG, '[Newrelic] {}'.format(msg))

