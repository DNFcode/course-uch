from django.shortcuts import render

def run_files(request):
    files = request.POST.get('files', [])

    for file in files:
        
