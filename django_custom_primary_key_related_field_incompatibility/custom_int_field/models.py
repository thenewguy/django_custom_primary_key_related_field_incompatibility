from django.db import models
from random import randint

ADJUSTMENT = 200

class CustomIntFieldValue(str):
    def __new__(cls, value):
        # verify types are acceptable
        value = int(value)
        
        if value < 0:
            display_value = value + ADJUSTMENT
            db_value = value
        else:
            display_value = value
            db_value = value - ADJUSTMENT
        
        # so we have equal length identifiers like "001" instead of "1"
        display_str = str(display_value).zfill(3)
        
        obj = super(CustomIntFieldValue, cls).__new__(cls, display_str)
        obj.display_value = display_value
        obj.db_value = db_value
        
        return obj
    
    def __int__(self):
        return self.display_value

class CustomIntField(models.IntegerField):
    __metaclass__ = models.SubfieldBase
    
    def pre_save(self, obj, add):
        if add and getattr(obj, self.attname) in (None, ""):
            value = self.random()
            setattr(obj, self.attname, value)
            return getattr(obj, self.attname)
        else:
            return super(CustomIntField, self).pre_save(obj, add)
    
    def random(self):
        return randint(-1*ADJUSTMENT, -1)
        
    def to_python(self, value):
        if value is not None and not isinstance(value, CustomIntFieldValue):
            value = super(CustomIntField, self).to_python(value)
            value = CustomIntFieldValue(value)
        
        return value
    
    def get_prep_value(self, value):
        if value is not None:
            if not isinstance(value, CustomIntFieldValue):
                value = self.to_python(value)
            value = value.db_value
        return value

class FooInt(models.Model):
    id = CustomIntField(primary_key=True, editable=False)
    
    def __unicode__(self):
        return u"%s" % self.pk

class BarInt(models.Model):
    id = models.OneToOneField(FooInt, primary_key=True)
    fk = models.ForeignKey(FooInt, related_name="+")
    m2m = models.ManyToManyField(FooInt, related_name="+")
    
    def __unicode__(self):
        return u"Linked to %s" % self.pk