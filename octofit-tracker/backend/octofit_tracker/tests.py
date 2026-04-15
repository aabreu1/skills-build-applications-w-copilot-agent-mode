from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Team, Activity, Leaderboard, Workout

class BasicModelTests(TestCase):
    def setUp(self):
        self.team = Team.objects.create(name='Test Team')
        self.user = get_user_model().objects.create_user(username='testuser', email='test@example.com', password='testpass')
        self.activity = Activity.objects.create(user=self.user, type='run', duration=10, calories=100)
        self.leaderboard = Leaderboard.objects.create(user=self.user, points=50)
        self.workout = Workout.objects.create(name='Test Workout', description='Desc', difficulty='easy')

    def test_team(self):
        self.assertEqual(self.team.name, 'Test Team')
    def test_user(self):
        self.assertEqual(self.user.username, 'testuser')
    def test_activity(self):
        self.assertEqual(self.activity.type, 'run')
    def test_leaderboard(self):
        self.assertEqual(self.leaderboard.points, 50)
    def test_workout(self):
        self.assertEqual(self.workout.name, 'Test Workout')
