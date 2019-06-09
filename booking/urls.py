from django.urls import path, include
from django.views.generic.base import RedirectView


urlpatterns = [
    path('', RedirectView.as_view(url='api-auth/login', permanent=False)),
    path('api/', include('airplanes_info.urls')),
    path('api-auth/', include('rest_framework.urls'))
]
