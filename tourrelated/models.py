from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

# Create your models here.
class CreateTour(models.Model):
    creator= models.ForeignKey(User, on_delete=models.CASCADE)
    title= models.CharField(max_length=200)
    slug=models.SlugField(unique=True,blank=True)
    location= models.CharField(max_length=200)
    duration= models.CharField(max_length=50)
    fee=models.CharField(max_length=10)
    date_of_tour=models.CharField(max_length=100)
    short_description=models.CharField(max_length=300)

    def __str__(self):
        return self.title+' by '+str(self.creator)
    def _get_unique_slug(self):
        slug = slugify(self.title)
        unique_slug = slug
        num = 1
        while CreateTour.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)
