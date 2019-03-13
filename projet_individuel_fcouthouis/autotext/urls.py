from django.urls import path, include
from . import views

app_name = 'autotext'
urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.signup, name='signup'),
    path('accounts/', include('django.contrib.auth.urls')),
    # path('myReferences', views.myReferences, name='myReferences'),
    # path('myRefs',  include('user_admin_site.urls')),
]
