from django.urls import path
from .views import homePageView, results, homePost

urlpatterns = [
    path('', homePageView, name='home'),
    path('homePost/', homePost, name='homePost'),
    path('<int:education>/<int:credit>/<int:married>/<int:co_inc>/<int:prop>/results/', results, name='results'),
]