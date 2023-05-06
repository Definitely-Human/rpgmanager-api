from django.contrib import admin
from djangoapps.manager import models


admin.site.register(models.Task)
admin.site.register(models.Tag)  # TODO Set up all models in admin
admin.site.register(models.Category)  # TODO Set up all models in admin
