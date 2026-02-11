from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout
from datetime import date, timedelta
import random


class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING('Clearing existing data...'))
        
        # Delete all existing data
        User.objects.all().delete()
        Team.objects.all().delete()
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()
        
        self.stdout.write(self.style.SUCCESS('Existing data cleared!'))
        
        # Create Teams
        self.stdout.write(self.style.WARNING('Creating teams...'))
        team_marvel = Team.objects.create(
            name='Team Marvel',
            description='The mightiest heroes of the Marvel Universe'
        )
        team_dc = Team.objects.create(
            name='Team DC',
            description='The legendary heroes of the DC Universe'
        )
        self.stdout.write(self.style.SUCCESS(f'Created teams: {team_marvel.name}, {team_dc.name}'))
        
        # Create Users (Superheroes)
        self.stdout.write(self.style.WARNING('Creating superhero users...'))
        marvel_heroes = [
            {'name': 'Iron Man', 'email': 'tony.stark@marvel.com'},
            {'name': 'Captain America', 'email': 'steve.rogers@marvel.com'},
            {'name': 'Thor', 'email': 'thor.odinson@marvel.com'},
            {'name': 'Black Widow', 'email': 'natasha.romanoff@marvel.com'},
            {'name': 'Hulk', 'email': 'bruce.banner@marvel.com'},
            {'name': 'Spider-Man', 'email': 'peter.parker@marvel.com'},
        ]
        
        dc_heroes = [
            {'name': 'Batman', 'email': 'bruce.wayne@dc.com'},
            {'name': 'Superman', 'email': 'clark.kent@dc.com'},
            {'name': 'Wonder Woman', 'email': 'diana.prince@dc.com'},
            {'name': 'The Flash', 'email': 'barry.allen@dc.com'},
            {'name': 'Aquaman', 'email': 'arthur.curry@dc.com'},
            {'name': 'Green Lantern', 'email': 'hal.jordan@dc.com'},
        ]
        
        marvel_users = []
        for hero in marvel_heroes:
            user = User.objects.create(
                name=hero['name'],
                email=hero['email'],
                team_id=str(team_marvel._id)
            )
            marvel_users.append(user)
        
        dc_users = []
        for hero in dc_heroes:
            user = User.objects.create(
                name=hero['name'],
                email=hero['email'],
                team_id=str(team_dc._id)
            )
            dc_users.append(user)
        
        all_users = marvel_users + dc_users
        self.stdout.write(self.style.SUCCESS(f'Created {len(all_users)} superhero users!'))
        
        # Create Workouts
        self.stdout.write(self.style.WARNING('Creating workout plans...'))
        workouts_data = [
            {
                'name': 'Super Soldier Sprint',
                'description': 'High-intensity interval training inspired by Captain America',
                'category': 'Cardio',
                'difficulty': 'Hard',
                'duration': 30,
                'calories_per_session': 400
            },
            {
                'name': 'Asgardian Strength Training',
                'description': 'Heavy lifting worthy of Thor himself',
                'category': 'Strength',
                'difficulty': 'Expert',
                'duration': 45,
                'calories_per_session': 350
            },
            {
                'name': 'Web-Slinger Agility',
                'description': 'Flexibility and agility training like Spider-Man',
                'category': 'Flexibility',
                'difficulty': 'Medium',
                'duration': 25,
                'calories_per_session': 200
            },
            {
                'name': 'Batcave Circuit',
                'description': 'Full-body circuit training from the Dark Knight',
                'category': 'Circuit',
                'difficulty': 'Hard',
                'duration': 40,
                'calories_per_session': 450
            },
            {
                'name': 'Speed Force Run',
                'description': 'Lightning-fast cardio workout inspired by The Flash',
                'category': 'Cardio',
                'difficulty': 'Expert',
                'duration': 35,
                'calories_per_session': 500
            },
            {
                'name': 'Amazonian Warrior Training',
                'description': 'Combat and strength training from Wonder Woman',
                'category': 'Strength',
                'difficulty': 'Hard',
                'duration': 50,
                'calories_per_session': 400
            },
        ]
        
        workouts = []
        for workout_data in workouts_data:
            workout = Workout.objects.create(**workout_data)
            workouts.append(workout)
        
        self.stdout.write(self.style.SUCCESS(f'Created {len(workouts)} workout plans!'))
        
        # Create Activities
        self.stdout.write(self.style.WARNING('Creating activity logs...'))
        activity_types = ['Running', 'Swimming', 'Cycling', 'Weightlifting', 'Yoga', 'Boxing']
        activities_created = 0
        
        for user in all_users:
            # Create 5-10 random activities for each user over the past 30 days
            num_activities = random.randint(5, 10)
            for _ in range(num_activities):
                activity_date = date.today() - timedelta(days=random.randint(0, 30))
                duration = random.randint(20, 90)
                calories = duration * random.randint(5, 12)
                
                Activity.objects.create(
                    user_id=str(user._id),
                    activity_type=random.choice(activity_types),
                    duration=duration,
                    calories_burned=calories,
                    distance=round(random.uniform(2, 15), 2),
                    date=activity_date
                )
                activities_created += 1
        
        self.stdout.write(self.style.SUCCESS(f'Created {activities_created} activity logs!'))
        
        # Create Leaderboard entries
        self.stdout.write(self.style.WARNING('Calculating leaderboard...'))
        leaderboard_entries = []
        
        for user in all_users:
            # Calculate total calories and activities for each user
            user_activities = Activity.objects.filter(user_id=str(user._id))
            total_calories = sum(activity.calories_burned for activity in user_activities)
            total_activities = user_activities.count()
            
            leaderboard_entry = Leaderboard.objects.create(
                user_id=str(user._id),
                team_id=user.team_id,
                total_calories=total_calories,
                total_activities=total_activities,
                rank=0  # Will be calculated below
            )
            leaderboard_entries.append(leaderboard_entry)
        
        # Sort by total calories and assign ranks
        leaderboard_entries.sort(key=lambda x: x.total_calories, reverse=True)
        for rank, entry in enumerate(leaderboard_entries, start=1):
            entry.rank = rank
            entry.save()
        
        self.stdout.write(self.style.SUCCESS(f'Created {len(leaderboard_entries)} leaderboard entries!'))
        
        # Summary
        self.stdout.write(self.style.SUCCESS('\n' + '='*50))
        self.stdout.write(self.style.SUCCESS('DATABASE POPULATION COMPLETE!'))
        self.stdout.write(self.style.SUCCESS('='*50))
        self.stdout.write(f'Teams: {Team.objects.count()}')
        self.stdout.write(f'Users: {User.objects.count()}')
        self.stdout.write(f'Activities: {Activity.objects.count()}')
        self.stdout.write(f'Workouts: {Workout.objects.count()}')
        self.stdout.write(f'Leaderboard Entries: {Leaderboard.objects.count()}')
        self.stdout.write(self.style.SUCCESS('='*50 + '\n'))
