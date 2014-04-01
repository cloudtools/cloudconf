from email.message import Message
from email.mime.multipart import MIMEMultipart
from collections import MutableMapping
import base64

import yaml

BOUNDARY = '--===============BOUNDARY==--'


class UserData(object):
    def __init__(self, boundary=None):
        self.parts = []
        self.boundary = boundary or BOUNDARY

    def add_part(self, mimetype, content=None, file_or_fd=None):
        _contents = None
        if content and file_or_fd:
            raise Exception("'content' and 'file_or_fd' arguments are "
                            "mutually exclusive.")
        if content:
            _contents = content
        elif file_or_fd:
            _contents = self.get_file_contents(file_or_fd)
        else:
            raise Exception("Must specify either 'content' or 'file_or_fd' "
                            "arguments.")
        self.parts.append((mimetype, _contents))

    def get_file_contents(self, file_or_fd):
        try:
            return file_or_fd.read()
        except AttributeError:
            with open(file_or_fd) as fd:
                return fd.read()

    def add_shell_script(self, content=None, file_or_fd=None):
        self.add_file_or_fd_part('text/x-shellscript', content, file_or_fd)

    def add_handler(self, content=None, file_or_fd=None):
        self.add_file_or_fd_part('text/part-handler', content, file_or_fd)

    def add_include_url(self, url):
        self.add_part('text/x-include-url', url)

    def add_cloudconfig(self, content=None, file_or_fd=None):
        if content and isinstance(content, MutableMapping):
            content = yaml.dump(content)
        self.add_part('text/cloud-config', content, file_or_fd)

    def add_boothook(self, content=None, file_or_fd=None):
        self.add_file_or_fd_part('text/cloud-boothook', content, file_or_fd)

    def _new_mime_part(self, container, content_type, payload):
        message = Message()
        message.set_payload(payload)
        message.set_type(content_type)
        message.set_charset('utf-8')
        container.attach(message)

    def to_mime_text(self):
        container = MIMEMultipart(boundary=self.boundary)
        for part in self.parts:
            self._new_mime_part(container, part[0], part[1])
        return container.as_string()

    def to_base64(self):
        return base64.b64encode(self.to_mime_text())
