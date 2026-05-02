from django import forms
from .models import Game, Platform, Developer

class GameForm(forms.ModelForm):
    new_platform = forms.CharField(max_length=100, required=False, label="Or add new platform")
    new_developer = forms.CharField(max_length=100, required=False, label="Or add new developer")
    new_developer_country = forms.CharField(max_length=100, required=False, label="New developer country")
    rating = forms.IntegerField(min_value=1, max_value=10, required=False, label="Rating (1-10)")

    class Meta:
        model = Game
        fields = ['title', 'genre', 'release_year', 'price', 'platform', 'developer']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['platform'].required = False
        self.fields['platform'].queryset = Platform.objects.filter(game__isnull=False).distinct()
        self.fields['developer'].required = False
        self.fields['developer'].queryset = Developer.objects.filter(game__isnull=False).distinct()