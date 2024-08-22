from django.contrib import admin
from django.urls import include, path
from search.views import search_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('invoices.urls')),
    path('search/', search_view, name='search'),
]
