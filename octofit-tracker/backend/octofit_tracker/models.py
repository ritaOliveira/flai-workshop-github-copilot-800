from django.db import models
from djongo import models as djongo_models


class User(models.Model):
    _id = djongo_models.ObjectIdField(primary_key=True)
    email = models.EmailField(unique=True, max_length=255)
    name = models.CharField(max_length=255)
    team_id = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'users'
    
    def __str__(self):
        return self.name


class Team(models.Model):
    _id = djongo_models.ObjectIdField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'teams'
    
    def __str__(self):
        return self.name


class Activity(models.Model):
    _id = djongo_models.ObjectIdField(primary_key=True)
    user_id = models.CharField(max_length=255)
    activity_type = models.CharField(max_length=100)
    duration = models.IntegerField()  # in minutes
    calories_burned = models.IntegerField()
    distance = models.FloatField(null=True, blank=True)  # in kilometers
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'activities'
    
    def __str__(self):
        return f"{self.activity_type} - {self.date}"


class Leaderboard(models.Model):
    _id = djongo_models.ObjectIdField(primary_key=True)
    user_id = models.CharField(max_length=255)
    team_id = models.CharField(max_length=255)
    total_calories = models.IntegerField(default=0)
    total_activities = models.IntegerField(default=0)
    rank = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'leaderboard'
    
    def __str__(self):
        return f"Rank {self.rank} - User {self.user_id}"


class Workout(models.Model):
    _id = djongo_models.ObjectIdField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=100)
    difficulty = models.CharField(max_length=50)
    duration = models.IntegerField()  # in minutes
    calories_per_session = models.IntegerField()
    
    class Meta:
        db_table = 'workouts'
    
    def __str__(self):
        return self.name
