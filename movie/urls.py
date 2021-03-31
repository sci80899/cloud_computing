from django.urls import path
from .import views
urlpatterns = [
    #localhost:8000:movie/
    #start with:movie/
    path('<movie_id>', views.movie_detail,name='movie_detail'),
    #path('/movie', views.movie_list,name='movie_list')
    path('', views.movie_list,name='movie_list'),
    path("chat/",views.chat)
]
