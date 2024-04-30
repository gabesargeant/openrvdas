from django.db import models

class LibraryCollection(models.Model):
    
    collection_name = models.CharField(primary_key=True, max_length=100, null=False)
    description = models.TextField(blank=True, null=True)



#This is a helper for the kv_store
class TypeChoices(models.TextChoices):
    STRING = 'string', 'String'
    NUMBER = 'number', 'Number'

class KVStore(models.Model):
    # A REALLY big store of key value pairs for all loggers, readers and such and such.
    kv_id = models.AutoField(primary_key=True)
    fk_id = models.IntegerField(blank=False) # this is the forign key to the object, Reader, Writer, Transform etc
    key = models.TextField(blank=False) 
    value = models.TextField(blank=False) 
    type = models.CharField(max_length=10, choices=TypeChoices.choices, blank=True, null=True)

class Transforms(models.Model):
    transform_id = models.AutoField(primary_key=True)
    transform_name = models.TextField(blank=False) 
    transform_kwargs = models.ManyToManyField(KVStore)

class ComposedWriters():
    #I Hate these
    composed_writer_id = models.AutoField(primary_key=True)
    composed_writer_name = models.TextField(blank=False) 
    composed_writer_kwargs = models.ManyToManyField(KVStore)
    transform_ids = models.ManyToManyField(Transforms)

class Readers(models.Model):
    reader_id = models.AutoField(primary_key=True)
    reader_name = models.TextField(blank=False) 
    reader_kwargs = models.ManyToManyField(KVStore)
    

class Writers(models.Model):
    writer_id = models.AutoField(primary_key=True)
    writer_name = models.TextField(blank=False) 
    writer_kwargs = models.ManyToManyField(KVStore)

class Modes(models.Model):
    # globally shared.
    mode_id = models.AutoField(primary_key=True)
    mode_name = models.TextField(blank=False) 


class LoggerConfiguration(models.Model):
    logger_id = models.AutoField(primary_key=True)
    logger_name = models.TextField(blank=False) 
    collection_key = models.ForeignKey(LibraryCollection, on_delete=models.DO_NOTHING)
    readers = models.ForeignKey(Readers, on_delete=models.DO_NOTHING)






