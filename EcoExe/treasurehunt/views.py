from django.shortcuts import render

# Create your views here.
def scan(request):
    return render(request, "scan.html")

def validate(request):
    if request.method == 'POST':
        print(request.POST)
        return render(request,"scan.html")