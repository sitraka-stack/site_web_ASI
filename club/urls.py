    # Ajoutez d'autres URLs ici selon vos besoins

from django.urls import path
from . import views

app_name = 'club'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('calendar/', views.calendar_view, name='calendar'),
    path('contact/', views.contact, name='contact'),
    
    # Authentification
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    
    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Catégories
    path('categories/', views.categories_choice, name='categories_choice'),
    path('matchs/<str:genre>/<int:age_id>/', views.matchs_by_category, name='matchs_by_category'),
    
    # Historique
    path('historique/', views.historique, name='historique'),
    # Ajoutez vos autres URLs ici
]