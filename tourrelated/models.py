from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.shortcuts import reverse
# Create your models here.

class Tour(models.Model):
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
        while Tour.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('my_tour_details', args=[self.slug])
    def get_absolute_url_another(self):
        return reverse('all_tour_details', args=[self.slug])
    def get_absolute_url_join(self):
        return reverse('join_tour_manage', args=[self.slug])

class Member_on_tour(models.Model):
    tour=models.ForeignKey(Tour, on_delete=models.CASCADE)
    name= models.CharField(max_length=100)
    mail=models.CharField(max_length=200)
    p_money=models.CharField(max_length=10)
    due=models.CharField(max_length=10)



    def __str__(self):
        return self.name

class Finance_Board(models.Model):
    tour =models.ForeignKey(Tour, on_delete=models.CASCADE)
    total_expeted=models.IntegerField(default=0,blank=True,null=True)
    Current_money=models.IntegerField(default=0,blank=True,null=True)
    due=models.IntegerField(default=0,blank=True,null=True)
    expens=models.IntegerField(default=0,blank=True,null=True)

class Expense(models.Model):
    tour=models.ForeignKey(Tour, on_delete=models.CASCADE)
    title=models.CharField(max_length=100)
    description=models.CharField(max_length=200)
    ammount=models.IntegerField(default=0)
    time=models.DateTimeField(auto_now_add=True)

class Schedule(models.Model):
    tour=models.ForeignKey(Tour, on_delete=models.CASCADE)
    day=models.CharField(max_length=20)
    time=models.CharField(max_length=20)
    task=models.TextField(max_length=300)
