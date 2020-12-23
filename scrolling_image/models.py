from django.db import models

class ScrollingImage(models.Model):
    name = models.CharField(max_length=50, null=True)
    image = models.FileField(upload_to='scrolling-images/');

    def __str__(self):
        return self.name
