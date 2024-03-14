from django.shortcuts import render


# Create your views here.
def scan(request):
    return render(request, "scan.html")

def validate(request):
    print("HELLO")

    print(request.body)

    if request.method == 'POST':
        return render(request,"scan.html")