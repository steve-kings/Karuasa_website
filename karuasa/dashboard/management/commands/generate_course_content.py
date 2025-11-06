from django.core.management.base import BaseCommand
from dashboard.models import Course
import google.generativeai as genai
import os

class Command(BaseCommand):
    help = 'Generate course content using Gemini API'
    
    def handle(self, *args, **options):
        gemini_api_key = os.getenv('GEMINI_API_KEY', '')
        if not gemini_api_key:
            self.stdout.write(self.style.ERROR('Gemini API key not configured'))
            return
            
        genai.configure(api_key=gemini_api_key)
        model = genai.GenerativeModel('gemini-pro')
        
        for course in Course.objects.filter(content=''):
            prompt = f"""
            Generate comprehensive educational content for the actuarial science course: {course.name}
            
            Include:
            1. Course overview and objectives
            2. Key concepts and theories
            3. Practical applications
            4. Study tips and resources
            5. Sample problems and solutions
            
            Format the content in HTML with proper headings and sections.
            """
            
            try:
                response = model.generate_content(prompt)
                course.content = response.text
                course.save()
                self.stdout.write(self.style.SUCCESS(f'Generated content for {course.name}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error generating content for {course.name}: {str(e)}'))