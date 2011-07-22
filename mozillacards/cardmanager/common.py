# Common functions
import libxml2
import cairo
import rsvg
import tempfile
import os
import commands
import urllib2
import json

class FetchDataError(Exception):
    pass

class UserDoesNotExist(Exception):
    pass

def prepare_data(email, groups):
    URL = "http://wiki.mozilla.org/api.php?" \
          "action=ask&q=[[bugzillamail::%s]]&format=json&" \
          "po=bugzillamail|name|surname|twitter|identi.ca|website"
    try:
        reply = urllib2.urlopen(URL % email).read()

    except:
        raise FetchDataError

    try:
        reply = json.loads(reply)

    except ValueError:
        raise FetchDataError

    try:
        if reply['ask']['result'] == 'Success':
            if reply['ask'].get('results', 0) == 0:
                raise UserDoesNotExist

        else:
            raise FetchDataError

    except KeyError:
            raise FetchDataError

    try:
        data = reply['ask']['results']['items'][0]['properties']

    except (KeyError, IndexError), exc:
        raise FetchDataError

    # strip all data, to be safe

    for key, value in data.iteritems():
        data[key] = value.strip()

    data['fullname'] = "%s %s" % (data.get('name', ''), data.get('surname', ''))

    for group in groups:
        count = 0
        for value in group:
            if value not in data.keys():
                continue

            key = 'group-%s-item-%s-name' % (groups.index(group),
                                              count
                                              )
            data[key] = value

            key = 'group-%s-item-%s-value' % (groups.index(group),
                                              count
                                              )
            data[key] = data.get(value, '')

            count += 1

    return data

def parse_svg(svg, output, *args, **kwargs):
    svgdoc = libxml2.parseDoc(svg.read())

    # set default values for data
    for node in svgdoc.xpathEval("//*[@default]"):
        node.setContent(node.hasProp("default").content)

    # set values for user
    for key in kwargs.keys():
        try:
            field = svgdoc.xpathEval("//*[@id='%s']" % key)[0]
        except IndexError:
            # we didn't find the key, ignore
            continue

        field.setContent(kwargs[key])

    output.write(unicode(svgdoc))
    output.close()

def svg2pdf(svgfile, output):
    # something is wrong with this code on CentOS
    # maybe an old python issue

    # surface = cairo.PDFSurface(output, 301, 195)
    # context = cairo.Context(surface)
    # rsvg.Handle(svgfile.name).render_cairo(context)

    # surface.finish()
    # output.close()

    # workaround
    svgfile.close()
    output.close()
    COMMAND = "rsvg-convert -f pdf '%s' > '%s'"
    status, output = commands.getstatusoutput(COMMAND %\
                                              (svgfile.name, output.name))

class TempFile:
    def __init__(self):
        self.fd, self.filename = tempfile.mkstemp()
        self.file = os.fdopen(self.fd, 'w+b')

    @property
    def name(self):
        return self.filename

    def read(self, size=-1):
        return self.file.read(size)

    def seek(self, where):
        return self.file.seek(where)

    def tell(self):
        return self.file.tell()

    def write(self, what):
        return self.file.write(what)

    def close(self):
        return self.file.close()

    def delete(self):
        self.file.close()
        try:
            os.unlink(self.filename)
        except:
            pass
