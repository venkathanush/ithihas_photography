from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('gallery/', views.gallery, name='gallery'),
    path('portfolio/<int:pk>/', views.portfolio_detail, name='portfolio_detail'),
    path('contact/', views.contact, name='contact'),
    path('mentorship/', views.mentorship, name='mentorship'),
    path('sitemap.xml', views.sitemap_xml, name='sitemap'),
    path('robots.txt', views.robots_txt, name='robots'),
]
