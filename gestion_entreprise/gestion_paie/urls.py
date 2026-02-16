from django.urls import path
from . import views

urlpatterns = [
    # Tableau de bord
    path('', views.tableau_bord_paie, name='tableau_bord_paie'),
    
    # Bulletins
    path('bulletins/', views.liste_bulletins, name='liste_bulletins'),
    path('bulletins/creer/', views.creer_bulletin, name='creer_bulletin'),
    path('bulletins/<int:pk>/', views.detail_bulletin, name='detail_bulletin'),
    path('bulletins/<int:pk>/modifier/', views.modifier_bulletin, name='modifier_bulletin'),
    path('bulletins/<int:pk>/supprimer/', views.supprimer_bulletin, name='supprimer_bulletin'),
    path('bulletins/<int:pk>/payer/', views.marquer_paye, name='marquer_paye'),
    
    # Éléments de paie
    path('bulletins/<int:bulletin_pk>/ajouter-element/', views.ajouter_element, name='ajouter_element'),
    path('elements/<int:pk>/supprimer/', views.supprimer_element, name='supprimer_element'),
    
    # Génération en masse
    path('generer-masse/', views.generer_bulletins_masse, name='generer_bulletins_masse'),
    
    # Historique employé
    path('historique/<int:employe_pk>/', views.historique_employe, name='historique_employe'),
]