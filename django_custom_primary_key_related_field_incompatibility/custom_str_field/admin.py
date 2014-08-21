from django.contrib import admin
from .models import FooStr, BarStr

admin.site.register(FooStr)
admin.site.register(BarStr)