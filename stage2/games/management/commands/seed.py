from django.core.management.base import BaseCommand
from games.models import Platform, Developer, Game, Review
from datetime import date

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        Platform.objects.all().delete()
        Developer.objects.all().delete()

        platforms = {
            'PC': Platform.objects.create(name='PC'),
            'PS5': Platform.objects.create(name='PlayStation 5'),
            'Switch': Platform.objects.create(name='Nintendo Switch'),
            'Xbox': Platform.objects.create(name='Xbox Series X'),
        }
        devs = {
            'Nintendo': Developer.objects.create(name='Nintendo', country='Japan'),
            'FromSoft': Developer.objects.create(name='FromSoftware', country='Japan'),
            'Valve': Developer.objects.create(name='Valve', country='USA'),
            'CDPR': Developer.objects.create(name='CD Projekt Red', country='Poland'),
            'Naughty Dog': Developer.objects.create(name='Naughty Dog', country='USA'),
        }
        games = [
            ('Elden Ring', 'RPG', 2022, 59.99, 'PS5', 'FromSoft'),
            ('The Legend of Zelda: TOTK', 'Adventure', 2023, 69.99, 'Switch', 'Nintendo'),
            ('Counter-Strike 2', 'Shooter', 2023, 0.00, 'PC', 'Valve'),
            ('Cyberpunk 2077', 'RPG', 2020, 39.99, 'PC', 'CDPR'),
            ('The Last of Us Part I', 'Action', 2022, 59.99, 'PS5', 'Naughty Dog'),
            ('Dark Souls III', 'RPG', 2016, 29.99, 'PC', 'FromSoft'),
            ('Mario Kart 8 Deluxe', 'Racing', 2017, 49.99, 'Switch', 'Nintendo'),
            ('Half-Life: Alyx', 'Shooter', 2020, 59.99, 'PC', 'Valve'),
            ('Phantom Liberty', 'RPG', 2023, 29.99, 'Xbox', 'CDPR'),
            ('Sekiro', 'Action', 2019, 39.99, 'PS5', 'FromSoft'),
            ('Portal 2', 'Puzzle', 2011, 9.99, 'PC', 'Valve'),
            ('Breath of the Wild', 'Adventure', 2017, 59.99, 'Switch', 'Nintendo'),
        ]
        created_games = []
        for title, genre, year, price, plat, dev in games:
            g = Game.objects.create(
                title=title, genre=genre, release_year=year,
                price=price, platform=platforms[plat], developer=devs[dev]
            )
            created_games.append(g)

        reviews = [
            (0, 10, 'Masterpiece, best game ever made.'),
            (0, 9, 'Incredible open world, slight performance issues.'),
            (1, 10, 'Zelda at its absolute peak.'),
            (2, 7, 'Fun but very competitive.'),
            (3, 8, 'Great story, rough at launch but much better now.'),
            (4, 9, 'Emotional and gorgeous.'),
            (5, 9, 'Brutally hard but fair.'),
            (6, 8, 'Perfect party game.'),
            (7, 10, 'Best VR game ever made.'),
            (8, 8, 'Great expansion, worth it for RPG fans.'),
            (9, 10, 'The most refined FromSoft game.'),
            (10, 9, 'Timeless puzzle design.'),
            (11, 10, 'Changed open world games forever.'),
        ]
        for idx, rating, text in reviews:
            Review.objects.create(
                game=created_games[idx], rating=rating,
                text=text, date=date.today()
            )
        self.stdout.write('Seeded successfully!')