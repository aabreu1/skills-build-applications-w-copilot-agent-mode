from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from djongo import models

from octofit_tracker import models as octo_models

from django.db import connection

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        User = get_user_model()
        # Eliminar datos existentes
        User.objects.all().delete()
        Team = self.get_or_create_team_model()
        Activity = self.get_or_create_activity_model()
        Leaderboard = self.get_or_create_leaderboard_model()
        Workout = self.get_or_create_workout_model()
        Team.objects.all().delete()
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()

        # Crear equipos
        marvel = Team.objects.create(name='Marvel')
        dc = Team.objects.create(name='DC')

        # Crear usuarios
        ironman = User.objects.create_user(username='ironman', email='ironman@marvel.com', password='1234', first_name='Tony', last_name='Stark')
        batman = User.objects.create_user(username='batman', email='batman@dc.com', password='1234', first_name='Bruce', last_name='Wayne')
        ironman.profile.team = marvel
        ironman.profile.save()
        batman.profile.team = dc
        batman.profile.save()

        # Crear actividades
        Activity.objects.create(user=ironman, type='run', duration=30, calories=300)
        Activity.objects.create(user=batman, type='cycle', duration=45, calories=400)

        # Crear leaderboard
        Leaderboard.objects.create(user=ironman, points=100)
        Leaderboard.objects.create(user=batman, points=120)

        # Crear workouts
        Workout.objects.create(name='Pushups', description='Do 20 pushups', difficulty='easy')
        Workout.objects.create(name='Squats', description='Do 30 squats', difficulty='medium')

        self.stdout.write(self.style.SUCCESS('octofit_db poblada con datos de prueba.'))

    def get_or_create_team_model(self):
        class Team(models.Model):
            name = models.CharField(max_length=100, unique=True)
            class Meta:
                app_label = 'octofit_tracker'
        return Team

    def get_or_create_activity_model(self):
        class Activity(models.Model):
            user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
            type = models.CharField(max_length=50)
            duration = models.IntegerField()
            calories = models.IntegerField()
            class Meta:
                app_label = 'octofit_tracker'
        return Activity

    def get_or_create_leaderboard_model(self):
        class Leaderboard(models.Model):
            user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
            points = models.IntegerField()
            class Meta:
                app_label = 'octofit_tracker'
        return Leaderboard

    def get_or_create_workout_model(self):
        class Workout(models.Model):
            name = models.CharField(max_length=100)
            description = models.TextField()
            difficulty = models.CharField(max_length=50)
            class Meta:
                app_label = 'octofit_tracker'
        return Workout
