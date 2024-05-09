from django.db import models
from django.utils import timezone

class LibraryCollection(models.Model):    
    collection_name = models.CharField(primary_key=True, max_length=100, null=False)
    description = models.TextField(blank=True, null=True)
    



class ConfigObjectStore(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    class_name = models.CharField(max_length=100)
    json_object = models.TextField()
    creation_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name