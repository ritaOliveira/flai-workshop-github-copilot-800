from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from .models import User, Team, Activity, Leaderboard, Workout
from .serializers import (
    UserSerializer, TeamSerializer, ActivitySerializer, 
    LeaderboardSerializer, WorkoutSerializer
)


@api_view(['GET'])
def api_root(request, format=None):
    """
    API root endpoint that lists all available endpoints
    """
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'teams': reverse('team-list', request=request, format=format),
        'activities': reverse('activity-list', request=request, format=format),
        'leaderboard': reverse('leaderboard-list', request=request, format=format),
        'workouts': reverse('workout-list', request=request, format=format),
    })


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint for users
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def get_queryset(self):
        """
        Optionally filter users by team_id
        """
        queryset = User.objects.all()
        team_id = self.request.query_params.get('team_id', None)
        if team_id is not None:
            queryset = queryset.filter(team_id=team_id)
        return queryset


class TeamViewSet(viewsets.ModelViewSet):
    """
    API endpoint for teams
    """
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class ActivityViewSet(viewsets.ModelViewSet):
    """
    API endpoint for activities
    """
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    
    def get_queryset(self):
        """
        Optionally filter activities by user_id or activity_type
        """
        queryset = Activity.objects.all()
        user_id = self.request.query_params.get('user_id', None)
        activity_type = self.request.query_params.get('activity_type', None)
        
        if user_id is not None:
            queryset = queryset.filter(user_id=user_id)
        if activity_type is not None:
            queryset = queryset.filter(activity_type=activity_type)
        
        return queryset.order_by('-date')


class LeaderboardViewSet(viewsets.ModelViewSet):
    """
    API endpoint for leaderboard
    """
    queryset = Leaderboard.objects.all()
    serializer_class = LeaderboardSerializer
    
    def get_queryset(self):
        """
        Optionally filter leaderboard by team_id, ordered by rank
        """
        queryset = Leaderboard.objects.all()
        team_id = self.request.query_params.get('team_id', None)
        
        if team_id is not None:
            queryset = queryset.filter(team_id=team_id)
        
        return queryset.order_by('rank')


class WorkoutViewSet(viewsets.ModelViewSet):
    """
    API endpoint for workouts
    """
    queryset = Workout.objects.all()
    serializer_class = WorkoutSerializer
    
    def get_queryset(self):
        """
        Optionally filter workouts by category or difficulty
        """
        queryset = Workout.objects.all()
        category = self.request.query_params.get('category', None)
        difficulty = self.request.query_params.get('difficulty', None)
        
        if category is not None:
            queryset = queryset.filter(category=category)
        if difficulty is not None:
            queryset = queryset.filter(difficulty=difficulty)
        
        return queryset
