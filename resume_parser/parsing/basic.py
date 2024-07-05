import ollama
from django.shortcuts import render
from .forms import ResumeForm
from .parse import extract_text
# Define the extracted text
# extracted_text = "I am a software engineer with experience in Python and Java programming. I have developed web applications using Django and Flask frameworks."

# Structured section prompts
STRUCTURED_SECTION_PROMPTS = {
    "contact_section": """Parse the resume below in HR-JSON 1.0.4 and return only contact information in the following structure:
    {{"contact": {{"first_name":"","last_name":"","city_name":"","state_name":"","country_name":"","zip_code":""}}}}
    Resume: {}""",
    
    "summary_section": """Parse the resume below in HR-JSON 1.0.4 and return only summary in the following structure:
    {{"summary": ""}}. If summary is not present in Resume return "N/A".
    Resume: {}""",
    

    "education_section": """Parse the resume below in HR-JSON 1.0.4 and return only education in the following structure:
    {{"education": [{{"school_name":"","school_location":"","degree":"","field_of_study":"","graduation_date":""}}]}}
    Resume: {}""",
    
    "experience_section": """Parse the resume below in HR-JSON 1.0.4 and return only work experience in the following structure:
    {{"work_experience": [{{"job_title":"","employer_name":"","company_city_name":"","company_country_name":"","start_date":"","end_date":"","description":""}}]}}
    Resume: {}""",
    
    "skills_section": """Parse the resume below in HR-JSON 1.0.4 and return only skills in the following structure:
    {{"skills": []}}. If skills are not present in Resume return "N/A".
    Resume: {}""",
    
    "otherinfo_section": """Parse the resume below in HR-JSON 1.0.4 and return only other info in the following structure:
    {{"other_info": {{"accomplishments":"","affiliations":"","websites":"","certifications":"","languages":""}}}}
    Resume: {}"""
}

# Function to call the ollama chat API with a specific prompt
def get_response(extract_text, structured_prompt):
    prompt = structured_prompt.format(extract_text)
    messages = [
        {'role': 'user', 'content': prompt},
    ]
    return ollama.chat(model='llama3', messages=messages)

# Dictionary to store responses
def process_resume_text(extract_text):
    # Dictionary to store parsed data
    parsed_data = {}

                                        
    # Call the API for each section
    for section, prompt in STRUCTURED_SECTION_PROMPTS.items():
        response = get_response(extract_text, prompt)
        parsed_data[section] = response.get('message', {}).get('content', '').strip()

    # Print the parsed data to the terminal
    for section, content in parsed_data.items():
        print(f"{section.replace('_', ' ').title()}:\n{content}\n")

