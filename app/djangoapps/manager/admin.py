from django.contrib import admin
from djangoapps.manager import models


admin.site.register(models.Task)
admin.site.register(models.Tag)
