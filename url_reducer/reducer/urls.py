from django.urls import path
from . import views
from .views import UrlList

urlpatterns = [
    path('set_url', views.set_url),
    path('get_domains', views.get_domains),
    path('get_url/page=<int:page_num>', UrlList.as_view()),
    path('delete_url/<int:url_id>', views.delete_url),
    path('redirect/<str:domain>/<str:domain_subpart>', views.redirect_url),
]