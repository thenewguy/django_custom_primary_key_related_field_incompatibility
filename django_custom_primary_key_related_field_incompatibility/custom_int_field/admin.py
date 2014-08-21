from django.contrib import admin
from .models import FooInt, BarInt 

admin.site.register(FooInt)
admin.site.register(BarInt)