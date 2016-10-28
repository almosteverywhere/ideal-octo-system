from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse

from attacks.models import Attack 

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def map(request):
    attacks = Attack.objects.order_by('-date').exclude(lat=0).exclude(lat=-1).filter(date__gt='1999-01-01')
    context = {
        'attacks': attacks,
    }
    
    # attack = get_object_or_404(Attack, pk=attack_id)
    return render(request, 'maps/map.html', context)


def year(request, year_id):
    import pdb; pdb.set_trace()
    attacks = Attack.objects.order_by('-date').exclude(location__lat=0).exclude(location__lat=-1).filter(date__year=2001)

    # attacks = Attack.objects.exclude(location__lat=-1).filter(date__year = '2001')
    
    # attacks = Attack.objects.order_by('-date').exclude(lat=0).exclude(lat=-1).filter(date__gt='1999-01-01')
    context = {
        'attacks': attacks,
    }
    
    # attack = get_object_or_404(Attack, pk=attack_id)
    return render(request, 'maps/map.html', context)