from django.shortcuts import render, redirect, get_object_or_404
from .models import Game, Platform, Developer, Review
from .forms import GameForm
from django.db.models import Avg
from datetime import date
from django.db import transaction

def game_list(request):
    games = Game.objects.annotate(avg_rating=Avg('review__rating'))
    platforms = Platform.objects.filter(game__isnull=False).distinct()  # only platforms with at least 1 game

    # Get filter values from the URL query string
    genre = request.GET.get('genre', '')
    platform_id = request.GET.get('platform', '')
    min_year = request.GET.get('min_year', '')
    max_year = request.GET.get('max_year', '')
    min_rating = request.GET.get('min_rating', '')

    # Apply filters one by one if they were provided
    if genre:
        games = games.filter(genre=genre)
    if platform_id:
        games = games.filter(platform_id=platform_id)
    if min_year:
        games = games.filter(release_year__gte=int(min_year))
    if max_year:
        games = games.filter(release_year__lte=int(max_year))
    if min_rating:
        games = games.filter(review__rating__gte=int(min_rating)).distinct()

    # Build genre list dynamically from DB for the dropdown
    genres = Game.objects.values_list('genre', flat=True).distinct()

    return render(request, 'games/game_list.html', {
        'games': games,
        'platforms': platforms,
        'genres': genres,
        # Pass filter values back so the form remembers what was selected
        'selected_genre': genre,
        'selected_platform': platform_id,
        'min_year': min_year,
        'max_year': max_year,
        'min_rating': min_rating,
    })

def game_add(request):
    if request.method == 'POST':
        form = GameForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                new_platform = form.cleaned_data.get('new_platform')
                if new_platform:
                    platform, _ = Platform.objects.get_or_create(name=new_platform)
                else:
                    platform = form.cleaned_data.get('platform')

                new_developer = form.cleaned_data.get('new_developer')
                if new_developer:
                    country = form.cleaned_data.get('new_developer_country') or 'Unknown'
                    developer, _ = Developer.objects.get_or_create(name=new_developer, defaults={'country': country})
                else:
                    developer = form.cleaned_data.get('developer')

                game = form.save(commit=False)
                game.platform = platform
                game.developer = developer
                game.save()

                rating = form.cleaned_data.get('rating')
                if rating:
                    Review.objects.create(game=game, rating=rating, text='', date=date.today())

            return redirect('game_list')
    else:
        form = GameForm()
    return render(request, 'games/game_form.html', {'form': form, 'action': 'Add'})

def game_edit(request, pk):
    game = get_object_or_404(Game, pk=pk)
    if request.method == 'POST':
        form = GameForm(request.POST, instance=game)
        if form.is_valid():
            new_platform = form.cleaned_data.get('new_platform')
            if new_platform:
                platform, _ = Platform.objects.get_or_create(name=new_platform)
            else:
                platform = form.cleaned_data.get('platform')

            new_developer = form.cleaned_data.get('new_developer')
            if new_developer:
                country = form.cleaned_data.get('new_developer_country') or 'Unknown'
                developer, _ = Developer.objects.get_or_create(name=new_developer, defaults={'country': country})
            else:
                developer = form.cleaned_data.get('developer')

            game = form.save(commit=False)
            game.platform = platform
            game.developer = developer
            game.save()
            return redirect('game_list')
    else:
        form = GameForm(instance=game)
    return render(request, 'games/game_form.html', {'form': form, 'action': 'Edit'})

def game_delete(request, pk):
    game = get_object_or_404(Game, pk=pk)
    if request.method == 'POST':
        game.delete()
        return redirect('game_list')
    return render(request, 'games/game_confirm_delete.html', {'game': game})