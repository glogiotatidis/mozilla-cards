# Common functions
import libxml2
import cairo
import rsvg
import tempfile
import os
import sys

def parse_svg(svg, output, *args, **kwargs):
    svgdoc = libxml2.parseDoc(svg.read())

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
