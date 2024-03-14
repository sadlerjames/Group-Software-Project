from django.shortcuts import render
import json
from matplotlib.patches import Circle

# Create your views here.
def scan(request):
    return render(request, "scan.html")

def validate(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        longitude = data['longitude']
        latitude = data['latitude']
        x = 0 #need to be based on the qr code coordinates
        y = 0
        circle = Circle((x,y),radius = 0.001) #a circle centering on the qr code with about a 40m radius
        if(circle.contains_point([longitude,latitude])):
            print("Within radius")
        else:
            print("Not within radius")
        return render(request,"scan.html")