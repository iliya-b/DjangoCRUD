from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('rcoffee/', include('rcoffee.urls')),
    path('admin/', admin.site.urls),
]