from django.db import models
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from rest_framework.exceptions import ValidationError

import os

User = get_user_model()

def validate_file_size(file):
    max_size = 5 * 1024 * 1024  # 5MB
    if file.size > max_size:
        raise ValidationError("Image file too large ( > 5MB )")

# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    banner_image = models.ImageField(upload_to='banners/', 
                                     validators=[
                                        FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png']), 
                                        validate_file_size
                                    ])
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    

# ✅ delete file when article is deleted
@receiver(models.signals.post_delete, sender=Article)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `Article` object is deleted.
    """
    if instance.banner_image and instance.banner_image.path:
        if os.path.isfile(instance.banner_image.path):
            os.remove(instance.banner_image.path)


# ✅ also delete old file if banner_image is updated
@receiver(models.signals.pre_save, sender=Article)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when updating with a new file.
    """
    if not instance.pk:
        return False  # skip on create

    try:
        old_file = Article.objects.get(pk=instance.pk).banner_image
    except Article.DoesNotExist:
        return False

    new_file = instance.banner_image
    if old_file and old_file != new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)