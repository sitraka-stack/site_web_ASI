from django.urls import path
from . import views

app_name = 'club'

urlpatterns = [
    path('', views.home, name='home'),
    path('calendar/', views.calendar, name='calendar'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('categories/', views.categories_choice, name='categories_choice'),
    path('matchs/<str:genre>/<int:category_age_id>/', views.matchs_by_category, name='matchs_by_category'),
    path('historique/', views.historique, name='historique'),
]