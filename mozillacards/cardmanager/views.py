# Create your views here.
from django.shortcuts import render_to_response, redirect
from django.core.context_processors import csrf
from django.http import HttpResponse
from django.core.mail import send_mail, EmailMessage
from django.conf import settings

from cardmanager import common
from cardmanager.models import Template

import json

def index(request):
    c = {}
    c.update(csrf(request))
    return render_to_response("index.html", c)

def generate(request):
    if not settings.DEBUG and not request.is_ajax():
        return redirect("index")

    try:
        template = Template.objects.get(default=True)
    except Template.DoesNotExist:
        return HttpResponse("Something went really bad. "
                            "Did you create templates first?"
                            )

    # fetch data from mozilla wiki
    try:
        data = common.prepare_data(request.POST['email'],
                                   eval("(%s)" % template.groups)
                                   )

    except common.FetchDataError:
        return HttpResponse("Error fetching data. Please try again")

    except common.UserDoesNotExist:
        return HttpResponse("User does not exist! "
                            "Are you sure you have a Remo page?")

    # cannot use that, CentOS comes with an ancient python :(
    # svg_back = tempfile.NamedTemporaryFile(delete=False)
    # svg_front = tempfile.NamedTemporaryFile(delete=False)
    # pdf_front = tempfile.NamedTemporaryFile(delete=False)
    # pdf_back = tempfile.NamedTemporaryFile(delete=False)
    svg_back = common.TempFile()
    svg_front = common.TempFile()
    pdf_front = common.TempFile()
    pdf_back = common.TempFile()

    # generate svg
    common.parse_svg(template.template_back, svg_back, **data)
    common.parse_svg(template.template_front, svg_front, **data)

    # generate pdf
    common.svg2pdf(svg_front, pdf_front)
    common.svg2pdf(svg_back, pdf_back)

    # email pdf
    email = EmailMessage('Your Mozilla Reps Business Card',
                         "Hi!\n\nEnjoy your new Mozilla Reps Business Card ;)"
                         "\n\nBest regards,\nThe ReMo bot\n",
                         'no-reply@mozillareps.org', # from
                         [request.POST['email']], # to
                         )
    email.attach('card-front.pdf', open(pdf_front.name).read(), 'application/pdf')
    email.attach('card-back.pdf', open(pdf_back.name).read(), 'application/pdf')
    email.send()

    try:
        svg_back.delete()
        svg_front.delete()
        pdf_back.delete()
        pdf_front.delete()
    except:
        pass

    data = "Check your inbox for your business card!"

    return HttpResponse(data)
