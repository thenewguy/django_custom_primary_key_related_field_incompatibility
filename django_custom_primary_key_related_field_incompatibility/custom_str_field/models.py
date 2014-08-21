from django.db import models
from random import choice

class CustomStrFieldValue(str):
    def __new__(cls, value):
        # verify types are acceptable
        value = str(value)
        
        obj = super(CustomStrFieldValue, cls).__new__(cls, value.upper())
        obj.db_value = value.lower()
        
        return obj

valid_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHJKMNPQRSTVWXYZ"
class CustomStrField(models.CharField):
    __metaclass__ = models.SubfieldBase
    
    def pre_save(self, obj, add):
        if add and getattr(obj, self.attname) in (None, ""):
            value = self.random()
            setattr(obj, self.attname, value)
            return getattr(obj, self.attname)
        else:
            return super(CustomStrField, self).pre_save(obj, add)
    
    def random(self):
        return "".join([choice(valid_chars) for _ in xrange(self.max_length)])
        
    def to_python(self, value):
        if value is not None and not isinstance(value, CustomStrFieldValue):
            value = super(CustomStrField, self).to_python(value)
            value = CustomStrFieldValue(value)
        
        return value
    
    def get_prep_value(self, value):
        if value is not None:
            if not isinstance(value, CustomStrFieldValue):
                value = self.to_python(value)
            value = value.db_value
        return value

class FooStr(models.Model):
    id = CustomStrField(primary_key=True, max_length=10, editable=False)
    
    def __unicode__(self):
        return u"%s" % self.pk

class BarStr(models.Model):
    id = models.OneToOneField(FooStr, primary_key=True)
    fk = models.ForeignKey(FooStr, related_name="+")
    m2m = models.ManyToManyField(FooStr, related_name="+")
    
    def __unicode__(self):
        return u"Linked to %s" % self.pk