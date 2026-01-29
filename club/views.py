from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.utils import timezone
from django.db.models import Q
from datetime import date
from .models import (
    MatchDay, 
    CategoryAge, 
    CategoryGenre, 
    ChampionnatCompetition, 
    Saison, 
    Joueur, 
    EquipeAdverse,
    PalmaresClub
)

def home(request):
    """Page d'accueil"""
    derniers_matchs = MatchDay.objects.select_related(
        'championnat', 'saison'
    ).prefetch_related('equipes_adverses').order_by('-date_rencontre')[:3]
    
    # Palmarès récents
    derniers_palmares = PalmaresClub.objects.select_related(
        'category'
    ).order_by('-annee')[:3]
    
    context = {
        'derniers_matchs': derniers_matchs,
        'palmares': derniers_palmares,  # ✅ Changé de 'derniers_palmares' à 'palmares'
    }
    return render(request, 'club/home.html', context)

def calendar(request):
    """Page calendrier avec filtres"""
    matchs = MatchDay.objects.select_related(
        'championnat', 'saison'
    ).prefetch_related('equipes_adverses').order_by('-date_rencontre')
    
    # Filtres
    saison_id = request.GET.get('saison')
    championnat_id = request.GET.get('championnat')
    categorie_age_id = request.GET.get('categorie_age')
    categorie_genre_id = request.GET.get('categorie_genre')
    
    if saison_id:
        matchs = matchs.filter(saison_id=saison_id)
    if championnat_id:
        matchs = matchs.filter(championnat_id=championnat_id)
    if categorie_age_id:
        matchs = matchs.filter(championnat__category_age_id=categorie_age_id)
    if categorie_genre_id:
        matchs = matchs.filter(championnat__category_genre_id=categorie_genre_id)
    
    # Pagination
    paginator = Paginator(matchs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'matchs': page_obj,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'saisons': Saison.objects.all(),
        'championnats': ChampionnatCompetition.objects.all(),
        'categories_age': CategoryAge.objects.all(),
        'categories_genre': CategoryGenre.objects.all(),
    }
    return render(request, 'club/calendar.html', context)

def contact(request):
    """Page de contact avec formulaire"""
    if request.method == 'POST':
        nom = request.POST.get('nom')
        email = request.POST.get('email')
        telephone = request.POST.get('telephone')
        sujet = request.POST.get('sujet')
        message_text = request.POST.get('message')
        
        # TODO: Envoyer email ou sauvegarder en base
        messages.success(request, '✅ Votre message a été envoyé avec succès !')
        return redirect('club:contact')
    
    return render(request, 'club/contact.html')

def login_view(request):
    """Page de connexion"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Essayer d'authentifier
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            # Vérifier si l'utilisateur a un profil Joueur
            try:
                joueur = Joueur.objects.get(id=user.id)
                messages.success(request, f'🎉 Bienvenue {joueur.prenom} {joueur.nom} !')
            except Joueur.DoesNotExist:
                messages.success(request, f'🎉 Bienvenue {user.username} !')
            return redirect('club:dashboard')
        else:
            messages.error(request, '❌ Identifiants incorrects.')
    
    return render(request, 'club/login.html')

def signup(request):
    """Page d'inscription"""
    if request.method == 'POST':
        nom = request.POST.get('nom')
        prenoms = request.POST.get('prenoms')
        date_naissance = request.POST.get('date_naissance')
        categorie_genre_id = request.POST.get('categorie_genre')
        email = request.POST.get('email')
        telephone = request.POST.get('telephone')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        
        # Vérifications
        if password != password_confirm:
            messages.error(request, '❌ Les mots de passe ne correspondent pas.')
            return redirect('club:signup')
        
        if not all([nom, prenoms, date_naissance, categorie_genre_id, email, telephone, password]):
            messages.error(request, '❌ Tous les champs obligatoires doivent être remplis.')
            return redirect('club:signup')
        
        # Vérifier si le joueur existe déjà par email
        if Joueur.objects.filter(email=email).exists():
            messages.error(request, '❌ Cet email est déjà utilisé.')
            return redirect('club:signup')
        
        try:
            # Calculer l'âge et déterminer la catégorie d'âge
            date_naiss = date.fromisoformat(date_naissance)
            today = date.today()
            age = today.year - date_naiss.year - ((today.month, today.day) < (date_naiss.month, date_naiss.day))
            
            # Trouver la catégorie d'âge correspondante
            category_age = CategoryAge.objects.filter(
                age_min__lte=age, 
                age_max__gte=age
            ).first()
            
            # Récupérer la catégorie de genre
            category_genre = CategoryGenre.objects.get(id=categorie_genre_id)
            
            # Créer le joueur avec email et téléphone
            joueur = Joueur.objects.create(
                nom=nom,
                prenom=prenoms,
                date_naissance=date_naiss,
                category=category_genre,
                category_age=category_age,
                email=email,
                telephone=telephone
            )
            
            messages.success(request, f'🎉 Inscription réussie ! Vous êtes dans la catégorie {category_genre} - {category_age if category_age else "Senior"}.')
            return redirect('club:login')
            
        except CategoryGenre.DoesNotExist:
            messages.error(request, '❌ Catégorie de genre invalide.')
        except Exception as e:
            messages.error(request, f'❌ Erreur : {str(e)}')
    
    # Récupérer les catégories pour le formulaire
    categories_genre = CategoryGenre.objects.all()
    
    context = {
        'categories_genre': categories_genre,
    }
    return render(request, 'club/signup.html', context)

@login_required
def dashboard(request):
    """Dashboard du joueur connecté"""
    try:
        joueur = Joueur.objects.get(id=request.user.id)
    except Joueur.DoesNotExist:
        messages.error(request, "❌ Aucun profil joueur trouvé.")
        return redirect('club:home')
    
    # Stats fictives basées sur la catégorie
    matchs_joues = MatchDay.objects.filter(
        championnat__category_genre=joueur.category,
        championnat__category_age=joueur.category_age,
        date_rencontre__lt=timezone.now()
    ).count()
    
    victoires = MatchDay.objects.filter(
        championnat__category_genre=joueur.category,
        championnat__category_age=joueur.category_age,
        sets_club=3
    ).count()
    
    defaites = matchs_joues - victoires if matchs_joues > 0 else 0
    pourcentage = round((victoires / matchs_joues * 100) if matchs_joues > 0 else 0)
    
    stats = {
        'matchs_joues': matchs_joues,
        'victoires': victoires,
        'defaites': defaites,
        'pourcentage': pourcentage,
    }
    
    # Derniers matchs
    derniers_matchs = MatchDay.objects.filter(
        championnat__category_genre=joueur.category,
        championnat__category_age=joueur.category_age
    ).select_related('championnat', 'saison').order_by('-date_rencontre')[:5]
    
    # Prochains matchs
    prochains_matchs = MatchDay.objects.filter(
        championnat__category_genre=joueur.category,
        championnat__category_age=joueur.category_age,
        date_rencontre__gte=timezone.now()
    ).select_related('championnat', 'saison').order_by('date_rencontre')[:3]
    
    context = {
        'joueur': joueur,
        'stats': stats,
        'derniers_matchs': derniers_matchs,
        'prochains_events': prochains_matchs,
    }
    return render(request, 'club/dashboard.html', context)

def logout_view(request):
    """Déconnexion"""
    logout(request)
    messages.success(request, '👋 Vous êtes déconnecté.')
    return redirect('club:home')

def categories_choice(request):
    """Page de choix des catégories"""
    categories_age = CategoryAge.objects.all()
    categories_genre = CategoryGenre.objects.all()
    
    # Compter les joueurs par catégorie
    categories_data = []
    for cat_genre in categories_genre:
        for cat_age in categories_age:
            nb_joueurs = Joueur.objects.filter(
                category=cat_genre,
                category_age=cat_age
            ).count()
            
            if nb_joueurs > 0:
                categories_data.append({
                    'genre': cat_genre,
                    'age': cat_age,
                    'nb_joueurs': nb_joueurs
                })
    
    context = {
        'categories_age': categories_age,
        'categories_genre': categories_genre,
        'categories_data': categories_data,
    }
    return render(request, 'club/categories_choice.html', context)


def matchs_by_category(request, genre, category_age_id):
    """Affiche les matchs d'une catégorie spécifique"""
    category_genre = get_object_or_404(CategoryGenre, genre=genre)
    category_age = get_object_or_404(CategoryAge, id=category_age_id)
    
    matchs = MatchDay.objects.filter(
        championnat__category_genre=category_genre,
        championnat__category_age=category_age
    ).select_related('championnat', 'saison').prefetch_related('equipes_adverses').order_by('-date_rencontre')
    
    paginator = Paginator(matchs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'matchs': page_obj,
        'page_obj': page_obj,
        'category_genre': category_genre,
        'category_age': category_age,
    }
    return render(request, 'club/matchs_by_category.html', context)

def historique(request):
    """Page d'historique (palmarès + matchs passés)"""
    # Palmarès
    palmares = PalmaresClub.objects.select_related('category').order_by('-annee')
    
    # Matchs passés avec résultats
    matchs_passes = MatchDay.objects.filter(
        date_rencontre__lt=timezone.now(),
        sets_club__isnull=False
    ).select_related('championnat', 'saison').prefetch_related('equipes_adverses').order_by('-date_rencontre')[:20]
    
    # Filtres
    annee = request.GET.get('annee')
    categorie_id = request.GET.get('categorie')
    
    if annee:
        palmares = palmares.filter(annee=annee)
    if categorie_id:
        palmares = palmares.filter(category_id=categorie_id)
    
    context = {
        'palmares': palmares,
        'matchs_passes': matchs_passes,
        'annees': range(2020, timezone.now().year + 1),
        'categories': CategoryGenre.objects.all(),
    }
    return render(request, 'club/historique.html', context)

def about(request):
    """Page À propos"""
    # Stats générales du club
    nb_joueurs = Joueur.objects.count()
    nb_matchs = MatchDay.objects.filter(date_rencontre__lt=timezone.now()).count()
    nb_victoires = MatchDay.objects.filter(sets_club=3).count()
    nb_titres = PalmaresClub.objects.count()
    
    context = {
        'nb_joueurs': nb_joueurs,
        'nb_matchs': nb_matchs,
        'nb_victoires': nb_victoires,
        'nb_titres': nb_titres,
    }
    return render(request, 'club/about.html', context)