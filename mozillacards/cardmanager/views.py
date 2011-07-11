# Create your views here.
from django.shortcuts import render_to_response, redirect
from django.core.context_processors import csrf
from django.http import HttpResponse
from django.core.mail import send_mail, EmailMessage

from cardmanager import common
from cardmanager.models import Template

import json
import tempfile

def index(request):
    c = {}
    c.update(csrf(request))
    return render_to_response("index.html", c)

def generate(request):
    # if not request.is_ajax():
    #     return redirect("index")
    template = Template.objects.get(default=True)

    # fetch data from mozilla wiki
    data = { 'fullname': 'John Doe',
             'pemail': 'jdoe@mozilla.org',
             'website': 'http://johndoe.name',
             'twitter': '@johndoe',
             'identi.ca': '@johndoe',
             }

    svg_back = tempfile.NamedTemporaryFile(delete=False)
    svg_front = tempfile.NamedTemporaryFile(delete=False)
    pdf_front = tempfile.NamedTemporaryFile(delete=False)
    pdf_back = tempfile.NamedTemporaryFile(delete=False)

    # generate svg
    common.parse_svg(template.template_back, svg_back, **data)
    common.parse_svg(template.template_front, svg_front, **data)

    # generate pdf
    common.svg2pdf(svg_front, pdf_front)
    common.svg2pdf(svg_back, pdf_back)

    # email pdf
    email = EmailMessage('Your Mozilla Business Cards',
                         "Hi!\n\nEnjoy your new Mozilla Business Cards ;)"
                         "\n\nBest regards,\nThe MozoCard Robot\n",
                         'no-reply@mozilla.org', # from
                         [request.POST['email']], # to
                         )
    email.attach('card-front.pdf', open(pdf_front.name).read(), 'application/pdf')
    email.attach('card-back.pdf', open(pdf_back.name).read(), 'application/pdf')
    email.send()

    try:
        os.unlink(svg_back)
        os.unlink(svg_front)
        os.unlink(pdf_backname)
        os.unlink(pdf_front.name)
    except:
        pass

    data = "Check your inbox for your business cards!"

    return HttpResponse(data)
