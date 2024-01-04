from django.contrib import admin
from django.urls import path, include
from registration.views import CustomLoginView, CustomLogoutView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    # path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('registration.urls')),  
    path('vendedor/', include('vendedor.urls')),
    path('jefeVentas/', include('jefeVentas.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)