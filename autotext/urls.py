from django.urls import path, include
from . import views

app_name = 'autotext'
urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.signup, name='signup'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('myReferences', views.myReferences, name='myReferences'),
    path('myReferences/addReference', views.addReference, name='addReference'),
    path('myReferences/editReference', views.editReference, name='editReference'),
    path('myReferences/deleteReference',
         views.deleteReference, name='deleteReference'),
    path('myReferences/addManyReferences',
         views.addManyReferences, name='addManyReferences'),
    path('myReferences/setWebography', views.setWebography, name='setWebography'),
    path('myReferences/addWebography', views.addWebography, name='addWebography'),
    path('myReferences/editWebography',
         views.editWebography, name='editWebography'),
    path('myReferences/deleteWebography',
         views.deleteWebography, name='deleteWebography'),



]
