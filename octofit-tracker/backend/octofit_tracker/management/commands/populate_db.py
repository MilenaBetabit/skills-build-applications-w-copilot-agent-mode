from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from djongo import models
from octofit_tracker import models as app_models

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Delete all data
        User = get_user_model()
        User.objects.all().delete()
        app_models.Team.objects.all().delete()
        app_models.Activity.objects.all().delete()
        app_models.Leaderboard.objects.all().delete()
        app_models.Workout.objects.all().delete()

        # Create teams
        marvel = app_models.Team.objects.create(name='Marvel')
        dc = app_models.Team.objects.create(name='DC')

        # Create users (super heroes)
        users = [
            {'email': 'tony@marvel.com', 'username': 'IronMan', 'team': marvel},
            {'email': 'steve@marvel.com', 'username': 'CaptainAmerica', 'team': marvel},
            {'email': 'bruce@marvel.com', 'username': 'Hulk', 'team': marvel},
            {'email': 'clark@dc.com', 'username': 'Superman', 'team': dc},
            {'email': 'bruce@dc.com', 'username': 'Batman', 'team': dc},
            {'email': 'diana@dc.com', 'username': 'WonderWoman', 'team': dc},
        ]
        user_objs = []
        for u in users:
            user = User.objects.create_user(email=u['email'], username=u['username'], password='password', team=u['team'])
            user_objs.append(user)

        # Create activities
        for user in user_objs:
            app_models.Activity.objects.create(user=user, type='Running', duration=30)
            app_models.Activity.objects.create(user=user, type='Cycling', duration=45)

        # Create workouts
        for user in user_objs:
            app_models.Workout.objects.create(user=user, name='Morning Cardio', description='Cardio session', duration=40)

        # Create leaderboard
        for team in [marvel, dc]:
            app_models.Leaderboard.objects.create(team=team, points=100)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
