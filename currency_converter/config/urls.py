from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('api.openapi')),
    path('api/', include('api.urls'), name='api'),

]
