from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import Profile
from records.models import TestRecord
from flashcards.models import Flashcard
from points.utils import award_points
from datetime import date, timedelta
import random

def create_sample_data():
    """Create sample users and data for testing"""
    
    # Create a teacher
    teacher = User.objects.create_user('teacher1', 'teacher@acadex.com', 'password123')
    Profile.objects.create(user=teacher, is_teacher=True)
    print("✅ Created teacher: teacher1")
    
    # Create students
    students = []
    student_names = ['alice', 'bob', 'charlie', 'diana', 'eve']
    
    for name in student_names:
        user = User.objects.create_user(f'{name}', f'{name}@acadex.com', 'password123')
        profile = Profile.objects.create(user=user, is_teacher=False)
        students.append(user)
        print(f"✅ Created student: {name}")
    
    # Create sample test records
    subjects = ['Mathematics', 'Science', 'History', 'English', 'Geography']
    
    for student in students:
        for subject in subjects:
            # Create 3-5 tests per subject for each student
            num_tests = random.randint(3, 5)
            base_score = random.randint(60, 95)
            
            for i in range(num_tests):
                # Simulate some improvement over time
                score = min(100, base_score + random.randint(-10, 15))
                test_date = date.today() - timedelta(days=random.randint(1, 90))
                
                TestRecord.objects.create(
                    student=student,
                    teacher=teacher,
                    subject=subject,
                    score=score,
                    max_score=100,
                    test_date=test_date
                )
                
                # Award points for the test
                award_points(student, int(score/10), 'test', f'Test in {subject}: {score}/100')
    
    print("✅ Created sample test records")
    
    # Create sample flashcards
    flashcard_data = [
        ('Mathematics', 'What is 2 + 2?', '4'),
        ('Mathematics', 'What is the square root of 16?', '4'),
        ('Science', 'What is the chemical symbol for water?', 'H2O'),
        ('Science', 'How many bones are in the human body?', '206'),
        ('History', 'In which year did World War II end?', '1945'),
        ('History', 'Who was the first President of the United States?', 'George Washington'),
        ('English', 'What is the plural of "mouse"?', 'mice'),
        ('Geography', 'What is the capital of France?', 'Paris'),
    ]
    
    for subject, question, answer in flashcard_data:
        creator = random.choice(students)
        Flashcard.objects.create(
            creator=creator,
            subject=subject,
            question=question,
            answer=answer,
            is_public=True
        )
        # Award points for creating flashcard
        award_points(creator, 5, 'study', f'Created flashcard in {subject}')
    
    print("✅ Created sample flashcards")
    
    # Add some streak bonuses
    for student in students[:3]:  # Give streaks to first 3 students
        streak_days = random.randint(3, 10)
        profile = student.profile
        profile.streak_days = streak_days
        profile.save()
        
        # Award streak bonus points
        streak_points = streak_days * 5
        award_points(student, streak_points, 'streak', f'{streak_days} day streak bonus!')
    
    print("✅ Added streak bonuses")
    
    # Display final stats
    print("\n🎯 SAMPLE DATA CREATED SUCCESSFULLY!")
    print("=" * 40)
    print(f"Teachers created: 1")
    print(f"Students created: {len(students)}")
    print(f"Test records: {TestRecord.objects.count()}")
    print(f"Flashcards: {Flashcard.objects.count()}")
    print("\nLogin credentials:")
    print("Teacher: teacher1 / password123")
    print("Students: alice, bob, charlie, diana, eve / password123")
    print("\n🚀 Ready to explore Acadex!")

if __name__ == '__main__':
    create_sample_data()
