from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.conf import settings
import os
from functools import partial

DOMAIN = [('student','student'), ('staff','staff')]
FACE_DIR = 'face_images/'
SIGN_DIR = "sign_images/"

def _update_filename(instance, filename, path):	
	ext = filename.split('.')[-1]
	filename = '{}.{}'.format(instance.matric_no, ext)
	return os.path.join(path, filename)

def upload_to(path):
	return partial(_update_filename, path=path)

# Create your models here.
class User(models.Model):
	matric_no = models.CharField(max_length=20)
	name = models.CharField(max_length=200)
	domain = models.CharField(max_length=20, choices = DOMAIN)
	face_image = models.ImageField(upload_to=upload_to(FACE_DIR))
	sign_image = models.ImageField(upload_to=upload_to(SIGN_DIR), blank=True)

	def __str__(self):
		return self.matric_no

@receiver(models.signals.post_delete, sender=User)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.face_image:
        if os.path.isfile(instance.face_image.path):
            os.remove(instance.face_image.path)
    if instance.sign_image:
        if os.path.isfile(instance.sign_image.path):
            os.remove(instance.sign_image.path)

@receiver(pre_save, sender=User)
def file_update(sender, **kwargs):
    upload_folder_instance = kwargs['instance']
    if FACE_DIR not in upload_folder_instance.face_image.name:
        filename = upload_folder_instance.face_image.name
        # print(f"face image is {filename}")
        path = _update_filename(instance = upload_folder_instance, filename = filename, path = FACE_DIR)
        path = os.path.join(settings.MEDIA_ROOT, path)
        try:
        	os.remove(path)
        except:
        	pass
    if SIGN_DIR not in upload_folder_instance.sign_image.name:
    	filename = upload_folder_instance.sign_image.name
    	# print(f"sign image is {filename}")
    	path = _update_filename(instance = upload_folder_instance, filename = filename, path = SIGN_DIR)
    	path = os.path.join(settings.MEDIA_ROOT, path)
    	try:
    		os.remove(path)
    	except:
    		pass

class UserLogin(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	username = models.CharField(max_length = 20)
	password = models.CharField(max_length = 100)

	def __str__(self):
		return f'{self.user.matric_no}-{self.username}'


