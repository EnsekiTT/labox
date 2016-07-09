# -*- coding:utf-8 -*-
# LaBox makes answer

import pycurl

try:
    from io import BytesIO
except ImportError:
    from StringIO import StringIO as BytesIO

headers = {}
def header_function(header_line):
    header_line = header_line.decode('iso-8859-1')
    if ':' not in header_line:
        return

    name, value = header_line.split(':', 1)

    name = name.strip()
    name = name.lower()

    value = value.strip()

    headers[name] = value

buffer = BytesIO()
c = pycurl.Curl()
c.setopt(c.URL, 'http://ensekitt.org/')
c.setopt(c.WRITEDATA, buffer)
c.setopt(c.HEADERFUNCTION, header_function)
c.perform()
c.close()

body = buffer.getvalue()
print(headers)
type_code = headers['content-type'].split(';')[1].split('=')[1].strip().lower()

print(body.decode(type_code))
