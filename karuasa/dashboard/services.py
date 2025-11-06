# dashboard/services.py
import google.generativeai as genai
import json
import os
import re
from django.conf import settings

class CourseAIGenerator:
    def __init__(self):
        self.api_key = os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("❌ Gemini API key not found. Please set GEMINI_API_KEY environment variable.")
        
        try:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-pro')
            print("✅ Gemini AI configured successfully")
        except Exception as e:
            raise ValueError(f"❌ Failed to configure Gemini AI: {str(e)}")
    
    def generate_course_content(self, topic, level='beginner', duration='4 weeks'):
        """
        Generate course content using Gemini API
        """
        print(f"🚀 Generating course for topic: {topic}, level: {level}, duration: {duration}")
        
        prompt = f"""
        Create a COMPLETE actuarial science course about {topic} with detailed lessons and practical content.

        TOPIC: {topic}
        LEVEL: {level}
        DURATION: {duration}

        Create 6 detailed lessons with:
        - Comprehensive lesson content (500-800 words each)
        - Practical examples from insurance industry
        - Mathematical formulas and calculations
        - Real case studies
        - Practice exercises
        - Actuarial applications

        Return ONLY valid JSON:

        {{
            "title": "Specific and engaging course title about {topic} in actuarial science",
            "description": "2-3 sentence compelling description explaining why this course matters for actuaries",
            "topics": [
                "Topic 1 with specific focus",
                "Topic 2 with mathematical emphasis", 
                "Topic 3 with case studies",
                "Topic 4 with risk applications",
                "Topic 5 with industry insights",
                "Topic 6 with future trends"
            ],
            "learning_outcomes": [
                "Specific measurable outcome 1",
                "Practical skill outcome 2", 
                "Analytical ability outcome 3",
                "Industry application outcome 4"
            ],
            "prerequisites": [
                "Specific prerequisite knowledge 1",
                "Required mathematical background 2",
                "Recommended experience 3"
            ],
            "resources": [
                "Specific textbook: Title by Author",
                "Software: Specific tool with purpose",
                "Online: Specific website or platform",
                "Industry: Specific publication or journal"
            ],
            "lessons": [
                {{
                    "title": "Lesson 1: Specific title about foundational concepts",
                    "content": "Detailed lesson content (500-800 words) covering fundamental concepts with mathematical formulas, insurance examples, and practical exercises. Include specific actuarial applications and real-world scenarios.",
                    "exercises": [
                        "Practical exercise 1 with specific instructions",
                        "Calculation problem 2 with expected solution",
                        "Case analysis 3 with guiding questions"
                    ]
                }},
                {{
                    "title": "Lesson 2: Specific title about advanced applications", 
                    "content": "Detailed lesson content (500-800 words) building on previous concepts with more complex mathematical models, insurance case studies, and industry applications.",
                    "exercises": [
                        "Advanced exercise 1",
                        "Complex calculation 2", 
                        "Real-world analysis 3"
                    ]
                }},
                {{
                    "title": "Lesson 3: Specific title about risk modeling",
                    "content": "Detailed lesson content (500-800 words) focusing on risk assessment, probability models, and insurance pricing applications.",
                    "exercises": [
                        "Risk assessment exercise",
                        "Pricing model development",
                        "Probability calculation"
                    ]
                }},
                {{
                    "title": "Lesson 4: Specific title about data analysis",
                    "content": "Detailed lesson content (500-800 words) covering statistical methods, data interpretation, and decision-making in insurance contexts.",
                    "exercises": [
                        "Data analysis project",
                        "Statistical interpretation",
                        "Decision framework exercise"
                    ]
                }},
                {{
                    "title": "Lesson 5: Specific title about industry applications",
                    "content": "Detailed lesson content (500-800 words) with real insurance case studies, regulatory considerations, and business applications.",
                    "exercises": [
                        "Case study analysis",
                        "Regulatory compliance exercise",
                        "Business strategy development"
                    ]
                }},
                {{
                    "title": "Lesson 6: Specific title about emerging trends",
                    "content": "Detailed lesson content (500-800 words) exploring future developments, technological impacts, and evolving practices in actuarial science.",
                    "exercises": [
                        "Trend analysis project",
                        "Innovation proposal",
                        "Future scenario planning"
                    ]
                }}
            ],
            "detailed_content": "Overall course overview in HTML format with sections, examples, and comprehensive explanations."
        }}

        Make it PRACTICAL with:
        - Real actuarial examples from life insurance, health insurance, property & casualty
        - Mathematical formulas and calculations with explanations
        - Insurance industry case studies
        - Risk assessment methodologies
        - Pricing and reserving techniques
        - Data analysis approaches

        Focus on {topic} specifically and provide actionable knowledge for actuarial students.
        """
        
        try:
            print("📡 Sending request to Gemini AI...")
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.9,  # More creative
                    top_p=0.8,
                    top_k=40,
                    max_output_tokens=4096,  # Increased for longer content
                )
            )
            print("✅ Received response from Gemini AI")
            
            content = response.text.strip()
            print(f"📝 Raw AI response preview: {content[:300]}...")
            
            # More robust JSON extraction
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                content = json_match.group()
                print("✅ Extracted JSON from response")
            else:
                print("❌ No JSON found in response, using fallback")
                return self._get_fallback_course(topic, level, duration)
            
            print(f"🧹 Cleaned content preview: {content[:200]}...")
            
            course_data = json.loads(content)
            print("✅ Successfully parsed JSON response")
            
            # Validate that we got actual generated content, not fallback
            if self._is_fallback_content(course_data, topic):
                print("❌ Detected fallback-like content, trying again with different approach")
                return self._generate_with_alternative_prompt(topic, level, duration)
            
            return course_data
            
        except json.JSONDecodeError as e:
            print(f"❌ JSON parsing error: {e}")
            print(f"💡 Raw content that failed to parse: {content}")
            return self._generate_with_alternative_prompt(topic, level, duration)
        except Exception as e:
            print(f"❌ Error generating course: {e}")
            return self._generate_with_alternative_prompt(topic, level, duration)
    
    def _is_fallback_content(self, course_data, topic):
        """Check if the content looks like our fallback template"""
        title = course_data.get('title', '').lower()
        description = course_data.get('description', '').lower()
        
        # Check for generic phrases that indicate fallback content
        generic_phrases = [
            "introduction to",
            "comprehensive course on",
            "fundamental concepts",
            "this course provides",
            "designed for level students",
            "actuarial modeling:",
            "applications"
        ]
        
        for phrase in generic_phrases:
            if phrase in title.lower() or phrase in description.lower():
                return True
        return False
    
    def _generate_with_alternative_prompt(self, topic, level, duration):
        """Alternative prompt for better results"""
        print("🔄 Trying alternative prompt approach...")
        
        alternative_prompt = f"""
        Create a FRESH and SPECIFIC actuarial science course about {topic} with 6 detailed lessons. 
        Be CREATIVE and ORIGINAL. Include ACTUAL actuarial concepts, mathematical models, and insurance applications.
        
        Return ONLY this JSON structure with unique, topic-specific content including lessons:
        
        {{
            "title": "Innovative title combining {topic} with actuarial practice",
            "description": "Engaging description focusing on practical {topic} applications in insurance and risk management",
            "topics": [
                "Mathematical foundations of {topic}",
                "Risk modeling with {topic}",
                "{topic} in life insurance pricing",
                "{topic} in property insurance underwriting", 
                "Data analytics using {topic}",
                "Regulatory framework for {topic}"
            ],
            "learning_outcomes": [
                "Design {topic} models for insurance pricing",
                "Apply {topic} methodologies to risk assessment",
                "Analyze insurance data using {topic} techniques",
                "Develop {topic}-based risk management strategies"
            ],
            "prerequisites": [
                "Probability theory and statistics",
                "Financial mathematics basics",
                "Understanding of insurance products",
                "Basic data analysis skills"
            ],
            "resources": [
                "Textbook: Advanced {topic} in Actuarial Science",
                "Software: Statistical tools for {topic} analysis",
                "Online: Professional actuarial resources",
                "Industry: Insurance case studies repository"
            ],
            "lessons": [
                {{
                    "title": "Foundations of {topic} in Actuarial Science",
                    "content": "Comprehensive introduction to {topic} with mathematical foundations, basic concepts, and initial applications in insurance contexts. Include formulas, examples, and practical scenarios.",
                    "exercises": ["Basic calculation exercise", "Concept application problem", "Case study analysis"]
                }},
                {{
                    "title": "Advanced {topic} Modeling Techniques",
                    "content": "Deep dive into sophisticated {topic} models, advanced mathematical approaches, and complex insurance applications with detailed explanations and worked examples.",
                    "exercises": ["Model development exercise", "Complex calculation", "Scenario analysis"]
                }},
                {{
                    "title": "{topic} in Insurance Risk Assessment",
                    "content": "Practical application of {topic} for risk evaluation, probability calculations, and insurance decision-making with real industry examples.",
                    "exercises": ["Risk assessment project", "Probability exercise", "Underwriting simulation"]
                }},
                {{
                    "title": "Data Analysis with {topic} Methods",
                    "content": "Statistical techniques, data interpretation methods, and analytical approaches using {topic} for insurance data analysis and insights generation.",
                    "exercises": ["Data analysis task", "Statistical interpretation", "Insight development"]
                }},
                {{
                    "title": "Industry Applications of {topic}",
                    "content": "Real-world case studies, business applications, and practical implementations of {topic} across different insurance sectors and product types.",
                    "exercises": ["Case study evaluation", "Business application design", "Implementation planning"]
                }},
                {{
                    "title": "Future Trends in {topic} for Actuaries",
                    "content": "Emerging developments, technological impacts, and evolving practices in {topic} and their implications for future actuarial work and insurance industry.",
                    "exercises": ["Trend analysis", "Innovation proposal", "Strategic planning exercise"]
                }}
            ],
            "detailed_content": "<h2>Comprehensive {topic} Course for Actuarial Excellence</h2><p>Detailed course overview with practical focus and real-world applications.</p>"
        }}
        """
        
        try:
            response = self.model.generate_content(
                alternative_prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.9,
                    max_output_tokens=4096,
                )
            )
            content = response.text.strip()
            
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                content = json_match.group()
                course_data = json.loads(content)
                print("✅ Alternative prompt successful")
                return course_data
            else:
                raise ValueError("No JSON in alternative response")
                
        except Exception as e:
            print(f"❌ Alternative prompt also failed: {e}")
            return self._get_fallback_course(topic, level, duration)
    
    def _get_fallback_course(self, topic, level, duration):
        """Fallback course data if AI fails"""
        print("🔄 Using intelligent fallback course data with lessons")
        return {
            "title": f"Advanced {topic} for Actuarial Practice",
            "description": f"This comprehensive course provides deep practical knowledge of {topic} applications in actuarial science, featuring mathematical models, insurance case studies, and hands-on exercises for {level} level professionals.",
            "topics": [
                f"Mathematical foundations of {topic}",
                f"Risk modeling with {topic} techniques",
                f"{topic} in insurance pricing",
                f"Data analysis using {topic} methods",
                f"Regulatory aspects of {topic}",
                f"Future trends in {topic} applications"
            ],
            "learning_outcomes": [
                f"Master advanced {topic} mathematical models",
                f"Apply {topic} to complex risk assessment scenarios",
                f"Develop insurance products using {topic} insights",
                f"Analyze data with sophisticated {topic} techniques",
                f"Communicate {topic} findings to diverse stakeholders"
            ],
            "prerequisites": [
                "Intermediate probability and statistics",
                "Financial mathematics knowledge",
                "Basic understanding of insurance principles",
                "Familiarity with data analysis concepts"
            ],
            "resources": [
                f"Textbook: Advanced {topic} in Modern Actuarial Science",
                "Software: Statistical analysis tools (R, Python, Excel)",
                "Online: Professional actuarial databases and resources",
                "Industry: Insurance case studies and white papers"
            ],
            "lessons": [
                {
                    "title": f"Introduction to {topic} in Actuarial Context",
                    "content": f"This foundational lesson covers the basic principles of {topic} and their relevance to actuarial science. We explore core concepts, mathematical foundations, and initial applications in insurance settings. Students will learn key formulas and methodologies that form the basis for more advanced topics covered in subsequent lessons.\n\nKey topics include:\n- Fundamental principles of {topic}\n- Mathematical models and formulas\n- Basic insurance applications\n- Practical examples and case studies\n\nThis lesson establishes the groundwork for understanding how {topic} transforms actuarial practice and enhances risk assessment capabilities.",
                    "exercises": [
                        "Calculate basic risk metrics using provided formulas",
                        "Analyze simple insurance scenarios applying lesson concepts",
                        "Develop foundational models for basic risk assessment"
                    ]
                },
                {
                    "title": f"Advanced {topic} Modeling Techniques",
                    "content": f"Building on foundational knowledge, this lesson delves into sophisticated {topic} modeling approaches. We explore complex mathematical frameworks, advanced statistical methods, and their applications in insurance pricing and risk management.\n\nKey areas covered:\n- Advanced mathematical models for {topic}\n- Statistical inference techniques\n- Model validation and testing\n- Practical implementation strategies\n\nThrough detailed examples and case studies, students will develop the skills needed to create robust {topic} models for real-world actuarial applications.",
                    "exercises": [
                        "Develop advanced pricing models using lesson techniques",
                        "Validate model performance with test datasets",
                        "Create risk assessment frameworks for complex scenarios"
                    ]
                },
                {
                    "title": f"{topic} in Risk Assessment and Management",
                    "content": f"This lesson focuses on practical applications of {topic} in risk evaluation and management. We examine how {topic} methodologies enhance traditional risk assessment approaches and provide more accurate insights for insurance decision-making.\n\nCoverage includes:\n- Risk quantification using {topic} methods\n- Probability estimation techniques\n- Uncertainty modeling approaches\n- Decision framework development\n\nStudents will work through real insurance scenarios to apply {topic} techniques in risk assessment contexts.",
                    "exercises": [
                        "Conduct comprehensive risk assessments for insurance products",
                        "Develop probability models for uncertain events",
                        "Create risk management strategies based on analysis"
                    ]
                },
                {
                    "title": f"Data Analysis with {topic} Methods",
                    "content": f"Exploring the intersection of {topic} and data analytics, this lesson covers statistical techniques, data interpretation methods, and analytical approaches specifically tailored for insurance data analysis.\n\nKey components:\n- Statistical analysis techniques\n- Data interpretation frameworks\n- Insight generation methods\n- Analytical decision-making processes\n\nThrough hands-on exercises, students will learn to extract meaningful insights from insurance data using {topic} methodologies.",
                    "exercises": [
                        "Analyze insurance datasets using statistical methods",
                        "Interpret complex data patterns and trends",
                        "Develop data-driven recommendations for insurance decisions"
                    ]
                },
                {
                    "title": f"Industry Applications of {topic}",
                    "content": f"This lesson presents real-world case studies and practical implementations of {topic} across various insurance sectors. We examine successful applications, challenges faced, and lessons learned from industry implementations.\n\nCase studies cover:\n- Life insurance applications\n- Property and casualty implementations\n- Health insurance innovations\n- Reinsurance strategies\n\nStudents will analyze actual industry scenarios and develop implementation plans for {topic} applications.",
                    "exercises": [
                        "Evaluate real insurance case studies",
                        "Develop implementation plans for specific scenarios",
                        "Analyze business impacts of {topic} applications"
                    ]
                },
                {
                    "title": f"Future Trends in {topic} for Actuaries",
                    "content": f"Looking ahead, this lesson explores emerging trends, technological developments, and evolving practices in {topic} and their implications for the future of actuarial science and the insurance industry.\n\nFuture focus areas:\n- Technological innovations impacting {topic}\n- Regulatory developments and implications\n- Emerging applications and opportunities\n- Strategic planning for future readiness\n\nStudents will develop forward-looking perspectives on how {topic} will shape actuarial practice in coming years.",
                    "exercises": [
                        "Analyze emerging trends and their potential impacts",
                        "Develop innovation proposals for future applications",
                        "Create strategic plans for adopting new methodologies"
                    ]
                }
            ],
            "detailed_content": f"""
            <h2>Comprehensive {topic} Course for Actuarial Excellence</h2>
            
            <h3>Course Overview</h3>
            <p>This {duration} {level}-level course provides an in-depth exploration of {topic} and its transformative applications in modern actuarial science. Through a structured curriculum of six comprehensive lessons, students will develop advanced skills in mathematical modeling, risk assessment, data analysis, and practical implementation.</p>
            
            <h3>Learning Approach</h3>
            <p>The course combines theoretical knowledge with practical applications, featuring:</p>
            <ul>
                <li>Mathematical models and formulas with detailed explanations</li>
                <li>Real insurance case studies from multiple sectors</li>
                <li>Hands-on exercises and practical applications</li>
                <li>Industry insights and best practices</li>
                <li>Future trend analysis and strategic planning</li>
            </ul>
            
            <h3>Target Audience</h3>
            <p>This course is designed for {level} level actuarial students and professionals seeking to enhance their expertise in {topic} applications within insurance and risk management contexts.</p>
            
            <h3>Expected Outcomes</h3>
            <p>Upon completion, students will possess advanced skills in {topic} methodologies and their practical application to complex actuarial challenges, positioning them for success in evolving insurance landscapes.</p>
            """
        }