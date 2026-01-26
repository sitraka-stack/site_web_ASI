from django.db import models

# Create your models here.
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.







"""
LES TYPES DE CATEGORIES : Age et Genre 
"""

class CategoryAge(models.Model):
    nom = models.CharField(max_length=50)
    age_min = models.IntegerField(blank=True, null=True)
    age_max = models.IntegerField(blank=True, null=True)
    
    def __str__(self):
        if self.age_min and self.age_max:
            return f"{self.nom} ({self.age_min}-{self.age_max} ans)"
        return self.nom

    class Meta:
        managed = True  # ✅ Changé
        db_table = 'category_age'
        verbose_name = 'Catégorie d\'âge'
        verbose_name_plural = 'Catégories d\'âge'
        ordering = ['age_min']
        
        
class CategoryGenre(models.Model):
    """Catégorie de genre : M (Masculin), F (Féminin)"""
    GENRE_CHOICES = [
        ('M', 'Masculin'),
        ('F', 'Féminin'),
    ]
    genre = models.CharField(max_length=1, unique=True, choices=GENRE_CHOICES)

    def __str__(self):
        return self.get_genre_display()

    class Meta:
        managed = True  # ✅ Changé
        db_table = 'category_genre'
        verbose_name = 'Catégorie de genre'
        verbose_name_plural = 'Catégories de genre'



"""
Les competition et championnat,  et saison 
"""

class ChampionnatCompetition(models.Model):
    """Championnat ou compétition"""
    nom = models.CharField(max_length=150)
    date_champ = models.DateField(verbose_name='Date du championnat')
    lieu_deroulement = models.CharField(max_length=150, verbose_name='Lieu')
    category_age = models.ForeignKey(
        CategoryAge, 
        on_delete=models.SET_NULL,  # ✅ Changé
        blank=True, 
        null=True,
        verbose_name='Catégorie d\'âge'
    )
    category_genre = models.ForeignKey(
        CategoryGenre, 
        on_delete=models.SET_NULL,  # ✅ Changé
        blank=True, 
        null=True,
        verbose_name='Genre'
    )

    def __str__(self):
        return f"{self.nom} - {self.date_champ.year}"

    class Meta:
        managed = True  # ✅ Changé
        db_table = 'championnat_competition'
        verbose_name = 'Championnat/Compétition'
        verbose_name_plural = 'Championnats/Compétitions'
        ordering = ['-date_champ']
        

        
        
class Saison(models.Model):
    """Saison sportive : 2023-2024, 2024-2025, etc."""
    periode = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.periode

    class Meta:
        managed = True  # ✅ Changé
        db_table = 'saison'
        verbose_name = 'Saison'
        verbose_name_plural = 'Saisons'
        ordering = ['-periode']

""" 
Les equipes adverses 
"""
class EquipeAdverse(models.Model):
    """Équipe adverse rencontrée"""
    nom = models.CharField(max_length=150)
    category_genre = models.ForeignKey(
        CategoryGenre, 
        on_delete=models.SET_NULL,  # ✅ Changé
        blank=True, 
        null=True,
        verbose_name='Genre'
    )
    category_age = models.ForeignKey(
        CategoryAge, 
        on_delete=models.SET_NULL,  # ✅ Changé
        blank=True, 
        null=True,
        verbose_name='Catégorie d\'âge'
    )

    def __str__(self):
        return self.nom

    class Meta:
        managed = True  # ✅ Changé
        db_table = 'equipe_adverse'
        verbose_name = 'Équipe adverse'
        verbose_name_plural = 'Équipes adverses'
        ordering = ['nom']

"""Les joueurs du club"""

class Joueur(models.Model):
    """Joueur du club"""
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    date_naissance = models.DateField()
    category = models.ForeignKey(
        CategoryGenre, 
        on_delete=models.PROTECT,  # ✅ Changé
        verbose_name='Genre'
    )
    category_age = models.ForeignKey(
        CategoryAge, 
        on_delete=models.SET_NULL,  # ✅ Changé
        blank=True, 
        null=True,
        verbose_name='Catégorie d\'âge'
    )

    def __str__(self):
        return f"{self.prenom} {self.nom}"

    def age(self):
        """Calcule l'âge du joueur"""
        from datetime import date
        today = date.today()
        return today.year - self.date_naissance.year - (
            (today.month, today.day) < (self.date_naissance.month, self.date_naissance.day)
        )

    class Meta:
        managed = True  # ✅ Changé
        db_table = 'joueur'
        verbose_name = 'Joueur'
        verbose_name_plural = 'Joueurs'
        ordering = ['nom', 'prenom']
        
        
"""Matchs"""
class MatchDay(models.Model):
    """Match / Rencontre"""
    date_rencontre = models.DateTimeField(verbose_name='Date de la rencontre')
    lieu_rencontre = models.CharField(max_length=150, verbose_name='Lieu')
    championnat = models.ForeignKey(
        ChampionnatCompetition, 
        on_delete=models.CASCADE,  # ✅ Changé
        verbose_name='Championnat'
    )
    saison = models.ForeignKey(
        Saison, 
        on_delete=models.CASCADE,  # ✅ Changé
        verbose_name='Saison'
    )
    equipes_adverses = models.ManyToManyField(
        EquipeAdverse,
        through='MatchDayEquipeAdverse',
        verbose_name='Équipes adverses'
    )
      # ✅ Résultat en sets
    sets_club = models.IntegerField(
        blank=True, 
        null=True,
        verbose_name='Sets gagnés par notre club'
    )
    sets_adverse = models.IntegerField(
        blank=True, 
        null=True,
        verbose_name='Sets gagnés par l\'adversaire'
    )
    
    # ✅ NOUVEAU : Scores détaillés par set
    set1_club = models.IntegerField(blank=True, null=True, verbose_name='Set 1 - Club')
    set1_adverse = models.IntegerField(blank=True, null=True, verbose_name='Set 1 - Adverse')
    
    set2_club = models.IntegerField(blank=True, null=True, verbose_name='Set 2 - Club')
    set2_adverse = models.IntegerField(blank=True, null=True, verbose_name='Set 2 - Adverse')
    
    set3_club = models.IntegerField(blank=True, null=True, verbose_name='Set 3 - Club')
    set3_adverse = models.IntegerField(blank=True, null=True, verbose_name='Set 3 - Adverse')
    
    set4_club = models.IntegerField(blank=True, null=True, verbose_name='Set 4 - Club')
    set4_adverse = models.IntegerField(blank=True, null=True, verbose_name='Set 4 - Adverse')
    
    set5_club = models.IntegerField(blank=True, null=True, verbose_name='Set 5 - Club (Tie-break)')
    set5_adverse = models.IntegerField(blank=True, null=True, verbose_name='Set 5 - Adverse (Tie-break)')

    def __str__(self):
        if self.sets_club is not None and self.sets_adverse is not None:
            return f"Match du {self.date_rencontre.strftime('%d/%m/%Y')} - {self.sets_club}:{self.sets_adverse}"
        return f"Match du {self.date_rencontre.strftime('%d/%m/%Y')} - {self.lieu_rencontre}"
    
    def resultat(self):
        """Retourne Victoire ou Défaite"""
        if self.sets_club is None or self.sets_adverse is None:
            return "À venir"
        if self.sets_club == 3:
            return "✅ Victoire"
        else:
            return "❌ Défaite"
    
    def score_detaille(self):
        """Affiche le score détaillé de tous les sets joués"""
        scores = []
        for i in range(1, 6):
            club = getattr(self, f'set{i}_club')
            adverse = getattr(self, f'set{i}_adverse')
            if club is not None and adverse is not None:
                scores.append(f"{club}-{adverse}")
        return " / ".join(scores) if scores else "Pas de score"

    def __str__(self):
        return f"Match du {self.date_rencontre.strftime('%d/%m/%Y')} - {self.lieu_rencontre}"

    class Meta:
        managed = True  # ✅ Changé
        db_table = 'match_day'
        verbose_name = 'Match'
        verbose_name_plural = 'Matchs'
        ordering = ['-date_rencontre']
        
class MatchDayEquipeAdverse(models.Model):
    """Table de liaison entre Match et Équipe Adverse"""
    match_day = models.ForeignKey(
        MatchDay, 
        on_delete=models.CASCADE  # ✅ Changé
    )
    equipe_adverse = models.ForeignKey(
        EquipeAdverse, 
        on_delete=models.CASCADE  # ✅ Changé
    )

    def __str__(self):
        return f"{self.match_day} - {self.equipe_adverse}"

    class Meta:
        managed = True  # ✅ Changé
        db_table = 'match_day_equipe_adverse'
        verbose_name = 'Match - Équipe adverse'
        verbose_name_plural = 'Matchs - Équipes adverses'
        unique_together = [['match_day', 'equipe_adverse']]


"""Palmares du club ASI"""

class PalmaresClub(models.Model):
    """Palmarès du club"""
    titre = models.CharField(max_length=200)
    competition = models.CharField(max_length=200)
    annee = models.IntegerField(verbose_name='Année')
    category = models.ForeignKey(
        CategoryGenre, 
        on_delete=models.PROTECT,  # ✅ Changé
        verbose_name='Genre'
    )

    def __str__(self):
        return f"{self.titre} - {self.competition} ({self.annee})"

    class Meta:
        managed = True  # ✅ Changé
        db_table = 'palmares_club'
        verbose_name = 'Palmarès'
        verbose_name_plural = 'Palmarès'
        ordering = ['-annee']


