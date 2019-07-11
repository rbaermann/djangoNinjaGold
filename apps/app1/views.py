from django.shortcuts import render, redirect, HttpResponse
import random

def index(request):
    if 'gold' not in request.session:
        request.session['gold'] = 0
    if 'moves' not in request.session:
        request.session['moves'] = 0
    if 'messages' not in request.session:
        request.session['messages'] = []
    if 'colors' not in request.session:
        request.session['colors'] = []
    request.session['moves'] += 1

    context = {}
    context['gold'] = request.session['gold']
    context['moves'] = request.session['moves'] - 1
    context['messages'] = request.session['messages']

    if request.session['moves'] >= 16:
        return render(request, 'app1/score.html', context)

    return render(request, 'app1/index.html', context)

def process(request):
    if 'reset' in request.POST:
        request.session['reset'] = request.POST['reset']
    
    if 'reset' in request.session:
        del request.session['reset']
        request.session['gold'] = 0
        request.session['moves'] = 0
        request.session['messages'] = []
        request.session['colors'] = []
        return redirect('/')

    if request.method == 'POST':
        gold = request.session['gold']
        loc = request.POST['location']
        if loc == 'farm':
            gold = random.randint(10, 20)
        elif loc == 'cave':
            gold = random.randint(5, 10)
        elif loc == 'house':
            gold = random.randint(2, 5)
        elif loc == 'casino':
            gold = random.randint(-50, 50)
        
        if gold > 0:
            request.session['messages'].insert(0, 'You have earned ' + str(gold) + ' gold from the ' + loc)
            request.session['colors'].insert(0, 'green')
        elif gold == 0:
            request.session['messages'].insert(0, 'You have broken even, left with ' + str(gold) + ' gold from the ' + loc)
            request.session['colors'].insert(0, 'black')
        else:
            request.session['messages'].insert(0, 'You have been robbed by the ' + loc + '... ' + str(gold * -1) + ' was taken from your total gold')
            request.session['colors'].insert(0, 'red')

        request.session['gold'] += gold

        if request.session['gold'] < 0 and gold < 0:
            request.session['messages'].insert(0, 'You now owe money, lose 1 moves')
            request.session['moves'] += 1


        return redirect('/')
