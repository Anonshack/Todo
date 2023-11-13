from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('users.urls')),
    path('admin/', admin.site.urls),
    path('todos/', include('todo.urls')),
    path('', include('homepage.urls'))
]