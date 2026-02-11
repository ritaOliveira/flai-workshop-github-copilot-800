from rest_framework import serializers
from .models import User, Team, Activity, Leaderboard, Workout


class UserSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='_id', read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'team_id', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def to_representation(self, instance):
        """Convert ObjectId to string"""
        representation = super().to_representation(instance)
        if hasattr(instance, '_id'):
            representation['id'] = str(instance._id)
        return representation


class TeamSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='_id', read_only=True)
    
    class Meta:
        model = Team
        fields = ['id', 'name', 'description', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def to_representation(self, instance):
        """Convert ObjectId to string"""
        representation = super().to_representation(instance)
        if hasattr(instance, '_id'):
            representation['id'] = str(instance._id)
        return representation


class ActivitySerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='_id', read_only=True)
    
    class Meta:
        model = Activity
        fields = ['id', 'user_id', 'activity_type', 'duration', 'calories_burned', 
                  'distance', 'date', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def to_representation(self, instance):
        """Convert ObjectId to string"""
        representation = super().to_representation(instance)
        if hasattr(instance, '_id'):
            representation['id'] = str(instance._id)
        return representation


class LeaderboardSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='_id', read_only=True)
    
    class Meta:
        model = Leaderboard
        fields = ['id', 'user_id', 'team_id', 'total_calories', 'total_activities', 
                  'rank', 'updated_at']
        read_only_fields = ['id', 'updated_at']
    
    def to_representation(self, instance):
        """Convert ObjectId to string"""
        representation = super().to_representation(instance)
        if hasattr(instance, '_id'):
            representation['id'] = str(instance._id)
        return representation


class WorkoutSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='_id', read_only=True)
    
    class Meta:
        model = Workout
        fields = ['id', 'name', 'description', 'category', 'difficulty', 
                  'duration', 'calories_per_session']
        read_only_fields = ['id']
    
    def to_representation(self, instance):
        """Convert ObjectId to string"""
        representation = super().to_representation(instance)
        if hasattr(instance, '_id'):
            representation['id'] = str(instance._id)
        return representation
