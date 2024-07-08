from django.shortcuts import render
from .forms import ResumeForm
from .parse import extract_text
from .basic import process_resume_text

def upload_resume(request):
    if request.method == 'POST':
        form = ResumeForm(request.POST, request.FILES)
        if form.is_valid():
            resume = request.FILES['resume']
            text = extract_text(resume)
            print(f"Extracted text: {text}")  # Debugging line
            
            hr_data = process_resume_text(text)
            
            # Ensure all keys exist in hr_data, even if they are empty
            contact_info = hr_data.get('contact_section', {}).get('contact', {})
            summary_info = hr_data.get('summary_section', {})
            other_info = hr_data.get('otherinfo_section', {}).get('other_info', {})
            
            parsed_data = {
                'first_name': contact_info.get('first_name', ''),
                'last_name': contact_info.get('last_name', ''),
                'city_name': contact_info.get('city_name', ''),
                'state_name': contact_info.get('state_name', ''),
                'country_name': contact_info.get('country_name', ''),
                'zip_code': contact_info.get('zip_code', ''),
                'summary': summary_info.get('summary', 'N/A'),
                'education': [
                    f"{edu.get('school_name', '')} - {edu.get('degree', '')}, {edu.get('field_of_study', '')} ({edu.get('graduation_date', '')})" 
                    for edu in hr_data.get('education_section', {}).get('education', [])
                ],
                'experience': [
                    f"{exp.get('employer_name', '')} - {exp.get('job_title', '')} ({exp.get('start_date', '')}-{exp.get('end_date', '')})" 
                    for exp in hr_data.get('experience_section', {}).get('work_experience', [])
                ],
                'skills': hr_data.get('skills_section', {}).get('skills', []),
                'accomplishments': other_info.get('accomplishments', ''),
                'affiliations': other_info.get('affiliations', ''),
                'websites': other_info.get('websites', ''),
                'certifications': other_info.get('certifications', ''),
                'languages': other_info.get('languages', '')
            }
            
            context = {'parsed_data': parsed_data}
            return render(request, 'parsing/results.html', context)
    else:
        form = ResumeForm()
    return render(request, 'parsing/parser.html', {'form': form})