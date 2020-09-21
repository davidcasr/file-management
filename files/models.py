from django.db import models
import os
from django.core.exceptions import ValidationError

"""
	Example of Method to generate a path
"""
def generate_path(instance, filename):
 
    folder = "model_" + str(instance.user) 
    return os.path.join("files", folder, filename)

"""
	Example of method to validate the extensions of image files
"""
def valid_extension_images(value):
    if (not value.name.endswith('.png') and
        not value.name.endswith('.jpeg') and 
        not value.name.endswith('.gif') and
        not value.name.endswith('.bmp') and 
        not value.name.endswith('.jpg')):
 
        raise ValidationError("Allowed files: .jpg, .jpeg, .png, .gif, .bmp")

def valid_extension(value):
    if (not value.name.endswith('.txt')):
        raise ValidationError("Allowed files: .txt")

class File(models.Model):
	name 				= models.CharField(max_length=50, null=False, blank=True)
	file     			= models.FileField(upload_to="files", null=False, blank=True, validators=[valid_extension])

	def __str__(self):
		return self.name
