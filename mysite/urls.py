"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
#from django.urls import path
from django.urls import include, path
import locations

urlpatterns = [
    path('api/', include('locations.urls')),
    path('api/store/<str:person_id>/<str:tracked_id>/<int:timestamp>', locations.views.store_get),
    path('api/store/<str:person_id>/<str:tracked_id>', locations.views.store_get),
    path('api/store/<str:person_id>', locations.views.store),
    path('api/get/<str:person_id>/<int:time_sub>', locations.views.track),
    path('api/test', locations.views.test),
    path('api/locations/all', locations.views.known_locations),
    path('api/locations/store', locations.views.store_known_locations),
    path('admin/', admin.site.urls),
]
