from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

import mimetypes
import os

def svg_validator(value):
    path = os.path.join(settings.MEDIA_ROOT, value.name)
    mimetype = mimetypes.guess_type(path)[0]
    if not mimetype == 'image/svg+xml' and \
           (mimetype == None and value.name[:-4] != ".svg"):
                raise ValidationError("File not SVG")

    return value

class Template(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    template_front = models.FileField("Front", upload_to="templates/",
                                      validators=[svg_validator])
    template_back = models.FileField("Back", upload_to="templates/",
                                     validators=[svg_validator])
    default = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name

    @classmethod
    def _set_single_template_default(self, sender, instance, **kwargs):
        if Template.objects.count() == 1:
            if instance.default == False:
                instance.default = True
                instance.save()

        else:
            if instance.default == True:
                # unset other default templates
                Template.objects.all().exclude(pk=instance.pk).update(default=False)

    @classmethod
    def _set_default_on_delete(self, sender, instance, **kwargs):
        if instance.default == True:
            # we deleted a default template,
            # set the template with the closed updated time to now
            # as default
            try:
                template = Template.objects.all().order_by("-updated")[0]
            except IndexError:
                # no templates left, no worries
                return

            template.default = True
            template.save()

models.signals.post_save.connect(Template._set_single_template_default, sender=Template)
models.signals.post_delete.connect(Template._set_default_on_delete, sender=Template)
