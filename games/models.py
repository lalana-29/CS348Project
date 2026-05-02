from django.db import models

class Platform(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self): return self.name

class Developer(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    def __str__(self): return self.name

class Game(models.Model):
    title = models.CharField(max_length=200)
    genre = models.CharField(max_length=100, db_index=True)
    release_year = models.IntegerField(db_index=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    platform = models.ForeignKey(Platform, on_delete=models.CASCADE, db_index=True)
    developer = models.ForeignKey(Developer, on_delete=models.CASCADE)
    def __str__(self): return self.title

class Review(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, db_index=True)
    rating = models.IntegerField(db_index=True)  # 1-10
    text = models.TextField()
    date = models.DateField()
    def __str__(self): return f"{self.game} - {self.rating}/10"