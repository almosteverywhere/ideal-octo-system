from django.shortcuts import render, get_object_or_404

from django.http import HttpResponse
from .models import Attack

def index(request):
    # return HttpResponse("Hello, world. You're at the attacks index.")
    latest_attack_list = Attack.objects.order_by('-date')
    context = {
        'latest_attack_list': latest_attack_list,
    }
    return render(request, 'attacks/index.html', context)

def detail(request, attack_id):
    attack = get_object_or_404(Attack, pk=attack_id)
    return render(request, 'attacks/detail.html', {'attack': attack})

def map(request):
    latest_attack_list = Attack.objects.order_by('-date')
    context = {
        'latest_attack_list': latest_attack_list,
    }
    
    # attack = get_object_or_404(Attack, pk=attack_id)
    return render(request, 'attacks/map.html')

