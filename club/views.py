from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.utils import timezone
from .models import (
    MatchDay, ChampionnatCompetition, Saison, EquipeAdverse,
    Joueur, PalmaresClub, CategoryAge, CategoryGenre
)

# ============================================
# PAGES PUBLIQUES (sans authentification)
# ============================================

def home(request):
    """Page d'accueil"""
    derniers_matchs = MatchDay.objects.all().order_by('-date_rencontre')[:3]
    palmares = PalmaresClub.objects.all().order_by('-annee')[:5]
    
    context = {
        'derniers_matchs': derniers_matchs,
        'palmares': palmares,
    }
    return render(request, 'home.html', context)

def about(request):
    """Page À propos"""
    return render(request, 'about.html')

def calendar_view(request):
    """Calendrier des matchs"""
    matchs = MatchDay.objects.all().order_by('-date_rencontre')
    
    # Filtres optionnels
    saison_id = request.GET.get('saison')
    genre_id = request.GET.get('genre')
    
    if saison_id:
        matchs = matchs.filter(saison_id=saison_id)
    if genre_id:
        matchs = matchs.filter(championnat__category_genre_id=genre_id)
    
    context = {
        'matchs': matchs,
        'saisons': Saison.objects.all(),
        'genres': CategoryGenre.objects.all(),
    }
    return render(request, 'calendar.html', context)

def contact(request):
    """Page Contact"""
    if request.method == 'POST':
        # Traitement du formulaire de contact
        nom = request.POST.get('nom')
        email = request.POST.get('email')
        message = request.POST.get('message')
        
        # Tu peux envoyer un email ou enregistrer en base
        messages.success(request, 'Votre message a été envoyé avec succès!')
        return redirect('contact')
    
    return render(request, 'contact.html')

# ============================================
# AUTHENTIFICATION
# ============================================

def login_view(request):
    """Page de connexion"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Connexion réussie!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Identifiants incorrects')
    
    return render(request, 'login.html')

def logout_view(request):
    """Déconnexion"""
    logout(request)
    messages.success(request, 'Vous êtes déconnecté')
    return redirect('home')

def signup_view(request):
    """Inscription (si tu veux permettre l'inscription publique)"""
    if request.method == 'POST':
        # Traitement de l'inscription
        pass
    
    return render(request, 'signup.html')

# ============================================
# DASHBOARD (réservé aux membres connectés)
# ============================================

@login_required
def dashboard(request):
    """Tableau de bord membre"""
    joueur = Joueur.objects.filter(
        nom__iexact=request.user.last_name,
        prenom__iexact=request.user.first_name
    ).first()
    
    context = {
        'joueur': joueur,
        'prochains_matchs': MatchDay.objects.filter(
            date_rencontre__gte=timezone.now()
        ).order_by('date_rencontre')[:5]
    }
    return render(request, 'dashboard.html', context)

# ============================================
# PAGES DE SÉLECTION DE CATÉGORIES
# ============================================

def categories_choice(request):
    """Page de choix des catégories"""
    categories_age = CategoryAge.objects.all().order_by('age_min')
    categories_genre = CategoryGenre.objects.all()
    
    context = {
        'categories_age': categories_age,
        'categories_genre': categories_genre,
    }
    return render(request, 'categories_choice.html', context)

def matchs_by_category(request, genre, age_id):
    """Affiche les matchs d'une catégorie spécifique"""
    category_age = get_object_or_404(CategoryAge, id=age_id)
    category_genre = get_object_or_404(CategoryGenre, genre=genre.upper())
    
    matchs = MatchDay.objects.filter(
        championnat__category_age=category_age,
        championnat__category_genre=category_genre
    ).order_by('-date_rencontre')
    
    context = {
        'category_age': category_age,
        'category_genre': category_genre,
        'matchs': matchs,
    }
    return render(request, 'matchs_by_category.html', context)

# ============================================
# HISTORIQUES
# ============================================

def historique(request):
    """Page historique du club"""
    palmares = PalmaresClub.objects.all().order_by('-annee')
    
    context = {
        'palmares': palmares,
    }
    return render(request, 'historique.html', context)