# Common functions
import libxml2
import cairo
import rsvg

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
    surface = cairo.PDFSurface(output, 301, 195)
    context = cairo.Context(surface)
    rsvg.Handle(svgfile.name).render_cairo(context)

    surface.finish()
    output.close()

