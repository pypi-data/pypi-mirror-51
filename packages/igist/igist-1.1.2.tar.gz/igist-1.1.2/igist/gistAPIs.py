import json
import requests
import logging

logging.basicConfig(level=logging.INFO,
                    # filename='igist.log',
                    datefmt='%Y/%m/%d %H:%M:%S  ',
                    format='%(asctime)s - %(levelname)s - %(message)s')


class Gist():
    def __init__(self, usrname, password, token,
                 is_public=True, description="This gist is created by python"):
        # when creating a Gist class, a existing gist token should be specified
        # ``token``
        # - an existing gist token under this user, or a pulic one
        # - '?' to chose from existing gists
        # - '+' to create a new gist
        self.usrname = usrname
        self.password = password
        self.gist_token = ''
        if token == '?':
            # chose from gist list
            gists = self._list_gists()
            tokens = list(gists.keys())
            for index, g_token in enumerate(tokens):
                print("【{}】. {} : {}".format(index, g_token, gists[g_token]))
            usr_input = input(
                "input a numeber to chose [ or '+' to create ] a gist: ")

            if usr_input.isdigit() and 0 <= int(usr_input) < len(tokens):
                self.gist_token = tokens[int(usr_input)]
            elif usr_input == '+':
                token = '+'

        if token == '+':
            self.gist_token = self._create_a_gist(
                is_public=is_public, description=description)
        elif self._is_gist_valid(token=token):
            self.gist_token = token

        if self.gist_token:
            logging.info('gist class is bound with:{}'.format(self.gist_token))
        else:
            logging.critical('creating gist class error!')
            raise Exception('creating gist class error!')

    def _create_a_gist(self,
                       is_public=True,
                       description="This gist is created by python"):
        # gist api allows to add a new gist with one or more files
        logging.info('creating new gist...')
        r = requests.post(
            'https://api.github.com/gists',
            json.dumps({
                "description": description,
                "public": is_public,
                'files': {"InitialFile": {"content": 'Initial text'}},
            }),
            auth=requests.auth.HTTPBasicAuth(self.usrname, self.password)
        )
        if r.status_code == 201:
            token = r.json()['html_url'].split('/')[-1]
            # delete InitialFile
            self.delete('InitialFile', token=token)
            logging.info('new gist token:{}'.format(token))
            return token

    def _is_gist_valid(self, token=''):
        if not token:
            token = self.gist_token
        else:
            r = requests.get(
                'https://api.github.com/gists/{}'.format(token),
                auth=requests.auth.HTTPBasicAuth(self.usrname, self.password)
            )
        if r.status_code == 200:
            return r.json()['id'] == token

    def _list_gists(self):
        # list all the gists of an authorized account, or public gists if no acount been authorized.
        # gists' token and file names under each are returned
        r = requests.get(
            'https://api.github.com/gists',
            auth=requests.auth.HTTPBasicAuth(self.usrname, self.password)
        )
        if r.status_code == 200:
            gists = {gist['id']: list(gist['files'].keys())
                     for gist in r.json()}
            return gists

    def write(self, file_name, file_content, token=''):
        if not token:
            token = self.gist_token
        r = requests.post(
            'https://api.github.com/gists/{}'.format(self.gist_token),
            json.dumps({'files': {file_name: {'content': file_content}}}),
            auth=requests.auth.HTTPBasicAuth(self.usrname, self.password)
        )
        if r.status_code == 200:
            logging.info('write succeed: {}'.format(file_name))
        else:
            logging.error('write failed: {}'.format(file_name))

    def delete(self, file_name, token=''):
        if not token:
            token = self.gist_token
        r = requests.post(
            'https://api.github.com/gists/{}'.format(token),
            json.dumps({'files': {file_name: None}}),
            auth=requests.auth.HTTPBasicAuth(self.usrname, self.password)
        )
        if r.status_code == 200:
            logging.info('{} deleted.'.format(file_name))
        else:
            logging.error('file {} deleting failed'.format(file_name))

    def read(self, filename, token=''):
        if not token:
            token = self.gist_token
        r = requests.get(
            'https://api.github.com/gists/{}'.format(token),
            auth=requests.auth.HTTPBasicAuth(self.usrname, self.password)
        )
        if r.status_code == 200:
            try:
                files = r.json()['files']
                content = files[filename]['content']
                return content
            except:
                logging.error('file not found!')

    def ls(self, token='', detail=False):
        # list file of a gist
        if not token:
            token = self.gist_token
        r = requests.get(
            'https://api.github.com/gists/{}'.format(token),
            auth=requests.auth.HTTPBasicAuth(self.usrname, self.password)
        )
        if r.status_code == 200:
            if detail:
                return r.json()['files']
            else:
                files = r.json()['files']
                names = [name for name in files]
                return names

    def remove_gist(self, token=''):
        if not token:
            token = self.gist_token
        r = requests.delete(
            'https://api.github.com/gists/{}'.format(token),
            auth=requests.auth.HTTPBasicAuth(self.usrname, self.password)
        )
        if r.status_code == 204:
            logging.info('gist removed succeed: {}'.format(token))
        else:
            logging.error('failed to remove: {}'.format(token))


if __name__ == "__main__":
    # import os
    # usr = os.getenv('github_username')
    # psw = os.getenv('github_password')

