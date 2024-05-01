from django.db import models

class LibraryCollection(models.Model):
    
    collection_name = models.CharField(primary_key=True, max_length=100, null=False)
    description = models.TextField(blank=True, null=True)



#This is a helper for the kv_store
class TypeChoices(models.TextChoices):
    STRING = 'string', 'String'
    NUMBER = 'number', 'Number'


class Transforms(models.Model):
    transform_id = models.AutoField(primary_key=True)
    transform_name = models.CharField(blank=False, max_length=256) 
    
class ComposedWriters():
    #I Hate these
    composed_writer_id = models.AutoField(primary_key=True)
    composed_writer_name = models.CharField(blank=False, max_length=256) 
   
class Readers(models.Model):
    reader_id = models.AutoField(primary_key=True)
    reader_name = models.CharField(blank=False, max_length=256) 
    

class Writers(models.Model):
    writer_id = models.AutoField(primary_key=True)
    writer_name = models.CharField(blank=False, max_length=256) 
    



class TransformKVStore(models.Model):
    # A REALLY big store of key value pairs for each Writer, Readers, Transforms.
    kv_id = models.AutoField(primary_key=True)    
    key = models.CharField(blank=False, max_length=256) 
    value = models.CharField(blank=False, max_length=256) 
    type = models.CharField(max_length=10, choices=TypeChoices.choices, blank=True, null=True)   
    transform = models.ForeignKey(Transforms, related_name='key_values',on_delete=models.CASCADE)

class WriterKVStore(models.Model):
    # A REALLY big store of key value pairs for each Writer, Readers, Transforms.
    kv_id = models.AutoField(primary_key=True)    
    key = models.CharField(blank=False, max_length=256) 
    value = models.CharField(blank=False, max_length=256) 
    type = models.CharField(max_length=10, choices=TypeChoices.choices, blank=True, null=True)
    writer = models.ForeignKey(Writers, related_name='key_values',on_delete=models.CASCADE)


class ReaderKVStore(models.Model):
    # A REALLY big store of key value pairs for each Writer, Readers, Transforms.
    kv_id = models.AutoField(primary_key=True)    
    key = models.CharField(blank=False, max_length=256) 
    value = models.CharField(blank=False, max_length=256) 
    type = models.CharField(max_length=10, choices=TypeChoices.choices, blank=True, null=True)
    readers = models.ForeignKey(Readers, related_name='key_values',on_delete=models.CASCADE,)



class Modes(models.Model):
    # globally shared.
    mode_id = models.AutoField(primary_key=True)
    mode_name = models.CharField(blank=False, max_length=256) 


class LoggerConfiguration(models.Model):
    logger_id = models.AutoField(primary_key=True)
    logger_name = models.CharField(blank=False, max_length=256) 
    collection_key = models.ForeignKey(LibraryCollection, on_delete=models.DO_NOTHING)
    readers = models.ForeignKey(Readers, on_delete=models.DO_NOTHING)






