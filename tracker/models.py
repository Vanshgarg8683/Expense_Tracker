from django.db import models
import uuid
from django.contrib.auth.models import User
# Create your models here.



class basemodel(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    created = models.DateField(auto_now=True)
    updated = models.DateField(auto_now_add=True)
    
    class Meta:
        abstract = True
        
class transaction(basemodel):
    description = models.CharField(max_length=100)
    amount = models.FloatField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    class Meta:
        ordering = ('description',)
        
    def isnegative(self):
        return self.amount<0
