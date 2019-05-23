from django.conf.urls import url
from lists import views

urlpatterns = [
    url(r'^new$', views.new_list, name='new_list'),
    url(r'^(\d+)/$', views.views_list, name='views_list'),
    url(r'^(\d+)/add_item$', views.add_item, name='add_item')
]
