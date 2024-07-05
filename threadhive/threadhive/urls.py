
from django.contrib import admin
from django.urls import path, include

# username:yashas
# password:yashas123

#username:sooraj
#password:sooraj123

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('base.urls')),
    
]