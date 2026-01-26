from django.contrib import admin
from .models import (
    CategoryGenre, CategoryAge, Saison, Joueur, ChampionnatCompetition, EquipeAdverse, MatchDay, MatchDayEquipeAdverse, PalmaresClub
)

# ==================== CATÉGORIES ====================

@admin.register(CategoryGenre)
class CategoryGenreAdmin(admin.ModelAdmin):
    list_display = ['genre']
    search_fields = ['genre']


@admin.register(CategoryAge)
class CategoryAgeAdmin(admin.ModelAdmin):
    list_display = ['nom', 'age_min', 'age_max']
    search_fields = ['nom']
    list_filter = ['age_min', 'age_max']
    
    
# ==================== SAISONS ====================
@admin.register(Saison)
class SaisonAdmin(admin.ModelAdmin):
    list_display = ['periode']
    search_fields = ['periode']
    
# ==================== JOUEURS ====================

@admin.register(Joueur)
class JoueurAdmin(admin.ModelAdmin):
    list_display = ['prenom', 'nom', 'date_naissance', 'category', 'category_age']
    list_filter = ['category', 'category_age']
    search_fields = ['nom', 'prenom']
    date_hierarchy = 'date_naissance'
    
    fieldsets = (
        ('Informations personnelles', {
            'fields': ('nom', 'prenom', 'date_naissance')
        }),
        ('Catégories', {
            'fields': ('category', 'category_age')
        }),
    )


# ==================== COMPÉTITIONS ====================

@admin.register(ChampionnatCompetition)
class ChampionnatCompetitionAdmin(admin.ModelAdmin):
    list_display = ['nom', 'date_champ', 'lieu_deroulement', 'category_age', 'category_genre']
    list_filter = ['category_age', 'category_genre', 'date_champ']
    search_fields = ['nom', 'lieu_deroulement']
    date_hierarchy = 'date_champ'


# ==================== ÉQUIPES ====================

@admin.register(EquipeAdverse)
class EquipeAdverseAdmin(admin.ModelAdmin):
    list_display = ['nom', 'category_genre', 'category_age']
    list_filter = ['category_genre', 'category_age']
    search_fields = ['nom']


# ==================== MATCHS ====================

class MatchDayEquipeAdverseInline(admin.TabularInline):
    model = MatchDayEquipeAdverse
    extra = 1


@admin.register(MatchDay)
class MatchDayAdmin(admin.ModelAdmin):
    list_display = ['date_rencontre', 'lieu_rencontre', 'championnat', 'saison', 'sets_club', 'sets_adverse', 'score_detaille', 'resultat']
    list_filter = ['saison', 'championnat', 'date_rencontre']
    search_fields = ['lieu_rencontre']
    date_hierarchy = 'date_rencontre'
    inlines = [MatchDayEquipeAdverseInline]
    
    fieldsets = (
        ('Informations du match', {
            'fields': ('date_rencontre', 'lieu_rencontre', 'championnat', 'saison')
        }),
        ('Résultat global', {
            'fields': ('sets_club', 'sets_adverse'),
            'description': 'Nombre de sets gagnés (le premier à 3 gagne)'
        }),
        ('Set 1', {
            'fields': ('set1_club', 'set1_adverse'),
            'classes': ('collapse',),
        }),
        ('Set 2', {
            'fields': ('set2_club', 'set2_adverse'),
            'classes': ('collapse',),
        }),
        ('Set 3', {
            'fields': ('set3_club', 'set3_adverse'),
            'classes': ('collapse',),
        }),
        ('Set 4', {
            'fields': ('set4_club', 'set4_adverse'),
            'classes': ('collapse',),
        }),
        ('Set 5 (Tie-break)', {
            'fields': ('set5_club', 'set5_adverse'),
            'classes': ('collapse',),
        }),
    )


# ==================== PALMARÈS ====================

@admin.register(PalmaresClub)
class PalmaresClubAdmin(admin.ModelAdmin):
    list_display = ['titre', 'competition', 'annee', 'category']
    list_filter = ['category', 'annee']
    search_fields = ['titre', 'competition']