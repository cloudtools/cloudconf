from email.message import Message
from email.mime.multipart import MIMEMultipart
from collections import MutableMapping
import base64

import yaml


class UserData(object):
    def __init__(self, shell_scripts=[], handler_files=[], include_urls=[]):
        self.parts = []

        for f in shell_scripts:
            self.add_shell_script(f)

        for f in handler_files:
            self.add_handler(f)

        for u in include_urls:
            self.add_include_url(u)

    def add_part(self, mimetype, content):
        self.parts.append((mimetype, content))

    def add_shell_script(self, filename):
        self.add_part('text/x-shellscript', open(filename).read())

    def add_handler(self, filename):
        self.add_part('text/part-handler', open(filename).read())

    def add_include_url(self, url):
        self.add_part('text/x-include-url', url)

    def add_cloudconfig(self, config):
        if isinstance(config, MutableMapping):
            config = yaml.dump(config)
        self.add_part('text/cloud-config', config)

    def _new_mime_part(self, container, content_type, payload):
        message = Message()
        message.set_payload(payload)
        message.set_type(content_type)
        message.set_charset('utf-8')
        container.attach(message)

    def to_mime_text(self):
        container = MIMEMultipart(boundary='--===============BOUNDARY==--')
        container._unixfrom = '## not necessary'
        for part in self.parts:
            self._new_mime_part(container, part[0], part[1])
        return container.as_string()

    def to_base64(self):
        return base64.b64encode(self.to_mime_text())
