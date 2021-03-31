from django.contrib import admin
from .models import Movie
# Register your models here.
# admin.site.register(Movie)
@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('id','title','poster','level','duration','score','director','stars','story')
    #倒序写-id
    ordering = ('id',)