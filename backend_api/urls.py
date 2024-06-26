from django.contrib import admin
from django.urls import path , include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/',include('backend_api.product.urls')),
    path('api-auth/', include('backend_api.account.urls')),
    path('api-order/', include('backend_api.order_system.urls')),
    path('auth/',include('rest_framework.urls')),
]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)