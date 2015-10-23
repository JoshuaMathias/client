import requests
import api_uri
import utils
from logger import logger


class ApiCalls:
    def __init__(self, host, access_token):
        self.host = host
        self.headers = {'Authorization': 'bearer ' + access_token}
        # self.cert = ('lingotek.crt', 'lingotek.key')

    def list_communities(self):
        """ gets the communities that a user is in """
        uri = api_uri.API_URI['community']
        payload = {'limit': 100}
        r = requests.get(self.host + uri, headers=self.headers, params=payload)
        api_log = '{method} {api} {status} {content_length}'.format(method='GET', api=uri, status=r.status_code,
                                                                    content_length=r.headers['content-length'])
        logger.api_call(api_log)
        return r

    def list_projects(self, community_id):
        """ gets the projects a user has """
        uri = api_uri.API_URI['project']
        payload = {'community_id': community_id, 'limit': 100}
        r = requests.get(self.host + uri, headers=self.headers, params=payload)
        api_log = '{method} {api} {status} {content_length}'.format(method='GET', api=uri, status=r.status_code,
                                                                    content_length=r.headers['content-length'])
        logger.api_call(api_log)
        return r

    def add_project(self, project_name, community_id, workflow_id):
        """ adds a project """
        uri = api_uri.API_URI['project']
        payload = {'title': project_name, 'community_id': community_id, 'workflow_id': workflow_id}
        r = requests.post(self.host + uri, headers=self.headers, data=payload)
        api_log = '{method} {api} {status} {content_length}'.format(method='POST', api=uri, status=r.status_code,
                                                                    content_length=r.headers['content-length'])
        logger.api_call(api_log)
        return r

    def patch_project(self, project_id, workflow_id):
        """ updates a project """
        uri = (api_uri.API_URI['project_id'] % locals())
        payload = {'project_id': project_id}
        if workflow_id:
            payload['workflow_id'] = workflow_id
        r = requests.patch(self.host + uri, headers=self.headers, data=payload)
        api_log = '{method} {api} {status} {content_length}'.format(method='PATCH', api=uri, status=r.status_code,
                                                                    content_length=r.headers['content-length'])
        logger.api_call(api_log)
        return r

    def add_target_project(self, project_id, locale, due_date):
        """ adds a target to all documents within a project """
        uri = (api_uri.API_URI['project_translation'] % locals())
        payload = {'id': project_id, 'locale_code': locale}
        if due_date:
            payload['due_date'] = due_date
        r = requests.post(self.host + uri, headers=self.headers, data=payload)
        api_log = '{method} {api} {status} {content_length}'.format(method='POST', api=uri, status=r.status_code,
                                                                    content_length=r.headers['content-length'])
        logger.api_call(api_log)
        return r

    def project_status(self, project_id):
        """ gets the status of a project """
        uri = (api_uri.API_URI['project_status'] % locals())
        r = requests.get(self.host + uri, headers=self.headers)
        api_log = '{method} {api} {status} {content_length}'.format(method='GET', api=uri, status=r.status_code,
                                                                    content_length=r.headers['content-length'])
        logger.api_call(api_log)
        return r

    def delete_project(self, project_id):
        """ deletes a project """
        uri = (api_uri.API_URI['project_id'] % locals())
        r = requests.delete(self.host + uri, headers=self.headers)
        api_log = '{method} {api} {status} {content_length}'.format(method='DELETE', api=uri, status=r.status_code,
                                                                    content_length=r.headers['content-length'])
        logger.api_call(api_log)
        return r

    def add_document(self, file_name, locale, project_id, title, **kwargs):
        """ adds a document """
        uri = api_uri.API_URI['document']
        payload = {'locale_code': locale, 'project_id': project_id, 'title': title}
        for key, value in kwargs.iteritems():
            if kwargs[key]:
                payload[key] = value
        detected_format = utils.detect_format(file_name)
        if not kwargs['format'] and detected_format != 'PLAINTEXT_OKAPI':
            payload['format'] = detected_format
        files = {'content': (file_name, open(file_name, 'rb'))}
        r = requests.post(self.host + uri, headers=self.headers, data=payload, files=files)
        api_log = '{method} {api} {status} {content_length}'.format(method='POST', api=uri, status=r.status_code,
                                                                    content_length=r.headers['content-length'])
        logger.api_call(api_log)
        return r

    def add_target_document(self, document_id, locale, workflow_id=None, due_date=None):
        """ adds a target to existing document, starts the workflow """
        uri = (api_uri.API_URI['document_translation'] % locals())
        payload = {'locale_code': locale, 'id': document_id}
        if workflow_id:
            payload['workflow_id'] = workflow_id
        if due_date:
            payload['due_date'] = due_date
        r = requests.post(self.host + uri, headers=self.headers, data=payload)
        api_log = '{method} {api} {status} {content_length}'.format(method='POST', api=uri, status=r.status_code,
                                                                    content_length=r.headers['content-length'])
        logger.api_call(api_log)
        return r

    def list_documents(self, project_id):
        """ lists all documents a user has access to, could be filtered by project id """
        uri = api_uri.API_URI['document']
        payload = {}
        if project_id:
            payload = {'project_id': project_id}
        r = requests.get(self.host + uri, headers=self.headers, params=payload)
        api_log = '{method} {api} {status} {content_length}'.format(method='GET', api=uri, status=r.status_code,
                                                                    content_length=r.headers['content-length'])
        logger.api_call(api_log)
        return r

    def document_status(self, document_id):
        """ gets the status of a document """
        uri = (api_uri.API_URI['document_status'] % locals())
        payload = {'document_id': document_id}
        r = requests.get(self.host + uri, headers=self.headers, params=payload)
        # logger.debug(r.url)
        api_log = '{method} {api} {status} {content_length}'.format(method='GET', api=uri, status=r.status_code,
                                                                    content_length=r.headers['content-length'])
        logger.api_call(api_log)
        return r

    def document_translation_status(self, document_id):
        """ gets the status of document translations """
        uri = (api_uri.API_URI['document_translation'] % locals())
        r = requests.get(self.host + uri, headers=self.headers)
        api_log = '{method} {api} {status} {content_length}'.format(method='GET', api=uri, status=r.status_code,
                                                                    content_length=r.headers['content-length'])
        logger.api_call(api_log)
        return r

    def document_content(self, document_id, locale_code, auto_format):
        """ downloads the translated document """
        uri = (api_uri.API_URI['document_content'] % locals())
        payload = {}
        if locale_code:
            payload['locale_code'] = locale_code
        if auto_format:
            payload['auto_format'] = auto_format
        r = requests.get(self.host + uri, headers=self.headers, params=payload, stream=True)
        api_log = '{method} {api} {status} {content_length}'.format(method='GET', api=uri, status=r.status_code,
                                                                    content_length=r.headers['content-length'])
        logger.api_call(api_log)
        return r

    def document_update(self, document_id, file_name=None, **kwargs):
        uri = (api_uri.API_URI['document_id'] % locals())
        payload = {'id': document_id}
        for key, value in kwargs.iteritems():
            if kwargs[key]:
                payload[key] = value
        if file_name:
            files = {'content': (file_name, open(file_name, 'rb'))}
            r = requests.patch(self.host + uri, headers=self.headers, data=payload, files=files)
        else:
            r = requests.patch(self.host + uri, headers=self.headers, data=payload)
        api_log = '{method} {api} {status} {content_length}'.format(method='PATCH', api=uri, status=r.status_code,
                                                                    content_length=r.headers['content-length'])
        logger.api_call(api_log)
        return r

    def delete_document(self, document_id):
        uri = (api_uri.API_URI['document_id'] % locals())
        r = requests.delete(self.host + uri, headers=self.headers)
        api_log = '{method} {api} {status} {content_length}'.format(method='DELETE', api=uri, status=r.status_code,
                                                                    content_length=r.headers['content-length'])
        logger.api_call(api_log)
        return r

    def list_workflows(self, community_id):
        uri = api_uri.API_URI['workflow']
        payload = {'community_id': community_id}
        r = requests.get(self.host + uri, headers=self.headers, params=payload)
        api_log = '{method} {api} {status} {content_length}'.format(method='GET', api=uri, status=r.status_code,
                                                                    content_length=r.headers['content-length'])
        logger.api_call(api_log)
        return r

    def list_locales(self):
        uri = 'http://gmc.lingotek.com/v1/locales'
        r = requests.get(uri)
        return r

    def get_project_info(self, community_id):
        response = self.list_projects(community_id)
        if response.status_code != 200:
            print 'error when listing projects for community'
            # todo raise error
        else:
            info = {}
            if int(response.json()['properties']['total']) == 0:
                return info
            entities = response.json()['entities']
            for entity in entities:
                info[entity['properties']['id']] = entity['properties']['title']
            return info

    def get_communities_info(self):
        response = self.list_communities()
        if response.status_code != 200:
            print response.json()
            print 'error getting community ids'
            # todo raise error
        entities = response.json()['entities']
        # ids = []
        # titles = []
        info = {}
        for entity in entities:
            info[entity['properties']['id']] = entity['properties']['title']
            # ids.append(entity['properties']['id'])
            # titles.append(entity['properties']['title'])
        # return ids, titles
        return info

    # def test(project_id):
    # project_id = "123"
    # print (api_uri.API_CALLS['project_id'] % locals())

    # if __name__ == '__main__':
    #     code = delete_project('5daa76ff-3a88-4466-a970-812edc79cb66')
    #     print code
    # test('9873249283')

# list_communities()
