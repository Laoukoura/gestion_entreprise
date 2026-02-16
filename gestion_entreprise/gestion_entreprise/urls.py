from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('employes/', include('gestion_emp.urls')),
    path('paie/', include('gestion_paie.urls'))
]
