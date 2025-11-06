from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
import google.generativeai as genai
import os
from dashboard.models import Competition

class Command(BaseCommand):
    help = 'Generate monthly actuarial competitions using Gemini API'
    
    def handle(self, *args, **options):
        gemini_api_key = os.getenv('GEMINI_API_KEY', '')
        if not gemini_api_key:
            self.stdout.write(self.style.ERROR('Gemini API key not configured'))
            return
            
        genai.configure(api_key=gemini_api_key)
        model = genai.GenerativeModel('gemini-pro')
        
        # Deactivate old competitions
        Competition.objects.filter(is_active=True).update(is_active=False)
        
        # Generate new competition
        prompt = """
        Create an interesting and challenging actuarial science competition problem for university students.
        The problem should:
        1. Be related to practical actuarial applications
        2. Require mathematical and statistical reasoning
        3. Be solvable within 2-3 hours
        4. Include clear evaluation criteria
        5. Be appropriate for undergraduate actuarial students
        
        Provide the problem statement and evaluation criteria.
        """
        
        try:
            response = model.generate_content(prompt)
            
            competition = Competition.objects.create(
                title=f"Actuarial Challenge {timezone.now().strftime('%B %Y')}",
                description="Monthly actuarial competition testing your problem-solving skills",
                problem_statement=response.text,
                start_date=timezone.now(),
                end_date=timezone.now() + timedelta(days=30),
                is_active=True
            )
            
            self.stdout.write(self.style.SUCCESS(f'Created competition: {competition.title}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error generating competition: {str(e)}'))