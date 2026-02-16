from django.urls import path
from . import views

urlpatterns = [
    path('', views.liste_employes, name='liste_employes'),
    path('ajouter/', views.ajouter_employe, name='ajouter_employe'),
    path('<int:pk>/', views.detail_employe, name='detail_employe'),
    path('<int:pk>/modifier/', views.modifier_employe, name='modifier_employe'),
    path('<int:pk>/supprimer/', views.supprimer_employe, name='supprimer_employe'),
]