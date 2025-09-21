from django.db import models
from core_utils.utils.generics.generic_models import CoreGenericModel
# Create your models here.
from django.conf import settings
class TimepassModel(CoreGenericModel):
    name = models.CharField(max_length=100)
    description = models.TextField()
    
