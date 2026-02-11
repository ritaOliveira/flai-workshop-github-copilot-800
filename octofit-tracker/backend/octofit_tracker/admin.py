from django.contrib import admin
from .models import User, Team, Activity, Leaderboard, Workout


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'team_id', 'created_at')
    search_fields = ('name', 'email')
    list_filter = ('team_id', 'created_at')
    ordering = ('-created_at',)


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at')
    search_fields = ('name',)
    ordering = ('-created_at',)


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'activity_type', 'duration', 'calories_burned', 'date', 'created_at')
    search_fields = ('user_id', 'activity_type')
    list_filter = ('activity_type', 'date', 'created_at')
    ordering = ('-date', '-created_at')


@admin.register(Leaderboard)
class LeaderboardAdmin(admin.ModelAdmin):
    list_display = ('rank', 'user_id', 'team_id', 'total_calories', 'total_activities', 'updated_at')
    search_fields = ('user_id', 'team_id')
    list_filter = ('team_id', 'rank')
    ordering = ('rank',)


@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'difficulty', 'duration', 'calories_per_session')
    search_fields = ('name', 'category')
    list_filter = ('category', 'difficulty')
    ordering = ('name',)
