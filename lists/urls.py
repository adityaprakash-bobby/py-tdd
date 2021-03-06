from django.conf.urls import url
from lists import views

urlpatterns = [
    url(r'^new$', views.new_list, name='new_list'),
    url(r'^(\d+)/$', views.views_list, name='views_list'),
    url(r'^users/(.+)/$', views.my_lists, name='my_lists'),
]
