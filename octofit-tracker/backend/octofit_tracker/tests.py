from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import User, Team, Activity, Leaderboard, Workout
from datetime import date


class TeamModelTest(TestCase):
    """Test cases for Team model"""
    
    def setUp(self):
        self.team = Team.objects.create(
            name='Test Team',
            description='A test team'
        )
    
    def test_team_creation(self):
        """Test team creation"""
        self.assertEqual(self.team.name, 'Test Team')
        self.assertEqual(self.team.description, 'A test team')
        self.assertIsNotNone(self.team._id)
    
    def test_team_str(self):
        """Test team string representation"""
        self.assertEqual(str(self.team), 'Test Team')


class UserModelTest(TestCase):
    """Test cases for User model"""
    
    def setUp(self):
        self.team = Team.objects.create(name='Test Team')
        self.user = User.objects.create(
            name='Test User',
            email='test@example.com',
            team_id=str(self.team._id)
        )
    
    def test_user_creation(self):
        """Test user creation"""
        self.assertEqual(self.user.name, 'Test User')
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertIsNotNone(self.user._id)
    
    def test_user_str(self):
        """Test user string representation"""
        self.assertEqual(str(self.user), 'Test User')


class ActivityModelTest(TestCase):
    """Test cases for Activity model"""
    
    def setUp(self):
        self.team = Team.objects.create(name='Test Team')
        self.user = User.objects.create(
            name='Test User',
            email='test@example.com',
            team_id=str(self.team._id)
        )
        self.activity = Activity.objects.create(
            user_id=str(self.user._id),
            activity_type='Running',
            duration=30,
            calories_burned=300,
            distance=5.0,
            date=date.today()
        )
    
    def test_activity_creation(self):
        """Test activity creation"""
        self.assertEqual(self.activity.activity_type, 'Running')
        self.assertEqual(self.activity.duration, 30)
        self.assertEqual(self.activity.calories_burned, 300)
        self.assertIsNotNone(self.activity._id)


class WorkoutModelTest(TestCase):
    """Test cases for Workout model"""
    
    def setUp(self):
        self.workout = Workout.objects.create(
            name='Test Workout',
            description='A test workout',
            category='Cardio',
            difficulty='Medium',
            duration=30,
            calories_per_session=250
        )
    
    def test_workout_creation(self):
        """Test workout creation"""
        self.assertEqual(self.workout.name, 'Test Workout')
        self.assertEqual(self.workout.category, 'Cardio')
        self.assertEqual(self.workout.difficulty, 'Medium')
        self.assertIsNotNone(self.workout._id)


class APIEndpointTest(APITestCase):
    """Test cases for API endpoints"""
    
    def setUp(self):
        """Set up test data"""
        self.team = Team.objects.create(
            name='Test Team',
            description='A test team'
        )
        self.user = User.objects.create(
            name='Test User',
            email='test@example.com',
            team_id=str(self.team._id)
        )
    
    def test_api_root(self):
        """Test API root endpoint"""
        url = reverse('api-root')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('users', response.data)
        self.assertIn('teams', response.data)
        self.assertIn('activities', response.data)
        self.assertIn('leaderboard', response.data)
        self.assertIn('workouts', response.data)
    
    def test_team_list(self):
        """Test team list endpoint"""
        url = reverse('team-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
    
    def test_user_list(self):
        """Test user list endpoint"""
        url = reverse('user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
    
    def test_workout_list(self):
        """Test workout list endpoint"""
        url = reverse('workout-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_activity_list(self):
        """Test activity list endpoint"""
        url = reverse('activity-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_leaderboard_list(self):
        """Test leaderboard list endpoint"""
        url = reverse('leaderboard-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
