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
            
            process_resume_text(text)
            
            context = {'text': text}
            return render(request, 'parsing/results.html', context)
    else:
        form = ResumeForm()
    return render(request, 'parsing/parser.html', {'form': form})