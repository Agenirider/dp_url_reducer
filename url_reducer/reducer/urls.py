from django.urls import path
from . import views

urlpatterns = [
    path('set_url', views.set_url),
    path('get_url/page=<int:page_num>', views.get_url),
    path('delete_url/<int:url_id>', views.delete_url),
    path('redirect/<str:domain>/<str:domain_subpart>', views.redirect_url),
]
