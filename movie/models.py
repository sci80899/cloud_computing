from django.db import models

# Create your models here.
class Movie(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    poster = models.CharField(max_length=200, blank=True, null=True)
    title = models.CharField(max_length=40, blank=True, null=True)
    level = models.CharField(max_length=40, blank=True, null=True)
    score = models.CharField(max_length=40, blank=True, null=True)
    duration = models.CharField(max_length=40, blank=True, null=True)
    director = models.CharField(max_length=100, blank=True, null=True)
    stars = models.CharField(max_length=100, blank=True, null=True)
    story = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'movie'


class User(models.Model):
    username=models.CharField(max_length=80)
    password=models.CharField(max_length=80)
    phone=models.CharField(max_length=80)

    class Meta:
        managed = False
        db_table = 'movie_user'
class Review(models.Model):
    movie_id=models.CharField(max_length=40)
    username=models.CharField(max_length=40)
    score=models.CharField(max_length=40)
    review = models.CharField(max_length=300)

    class Meta:
        managed = False
        db_table = 'movie_review'
class Pal(models.Model):
    movie_id=models.CharField(max_length=40)
    username=models.CharField(max_length=40)
    score=models.CharField(max_length=40)
    review = models.CharField(max_length=500)

    class Meta:
        managed = False
        db_table = 'movie_pal'