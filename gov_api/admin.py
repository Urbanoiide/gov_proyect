from django.contrib import admin
from . import models

for name, model in models.__dict__.items():
    if isinstance(model, type):
        try:
            admin.site.register(model)
        except admin.sites.AlreadyRegistered:
            pass
