# code of views.py
from django import forms
from django.shortcuts import render
from base import forms
from base.curves import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# from base.curves import *
from sympy import nextprime
import time
import math


# Create your views here.
# a = 0
# d = 0
# p = 0
# new_p = 0
# set = False

def home(request):
    # global a,d,p,new_p,set
    new_p = 0
    prime = 0

    adp_form = forms.adp_form()

    if request.method == "POST":

        adp_form = forms.adp_form(request.POST)

        if adp_form.is_valid():

            opt = request.session['opt'] = adp_form.cleaned_data['opt']
            type_opt = request.session['type_opt'] = adp_form.cleaned_data['type_opt']
            a = request.session['a'] = adp_form.cleaned_data['a']
            d = request.session['d'] = adp_form.cleaned_data['d']
            p = request.session['p'] = adp_form.cleaned_data['p']
            request.session['set'] = True
            new_p = request.session['new_p'] = nextprime(p - 1)
            lo = request.session['lo'] = int(new_p + 1 - 2 * (new_p ** 0.5))
            hi = request.session['hi'] = int(new_p + 1 + 2 * (new_p ** 0.5))
            prime = (new_p == p)

            # Show warning if prime is too large
            if type_opt == '2' and p > 100_000_007:
                # You should handle this via messages framework or add a flag to context
                return render(request, 'base/home.html', {
                    'adp_form': adp_form,
                    'stage': 1,
                    'alert': "Computation takes a large amount of time"
                })

            return render(request, 'base/home.html',
                          {'adp_form': adp_form, 'stage': 2, 'a': a, 'd': d, 'p': p, 'new_p': new_p, 'lo': lo, 'hi': hi,
                           'prime': prime})
    return render(request, 'base/home.html', {'adp_form': adp_form, 'stage': 1})


# @csrf_exempt
def proceed(request):
    x1 = request.GET.get('x1')
    y1 = request.GET.get('y1')
    x2 = request.GET.get('x2')
    y2 = request.GET.get('y2')

    # Check if parameters are set
    if not request.session.get('set', False):
        return render(request, 'base/notset.html')

        # Validate that all inputs are present and valid numbers
    try:
        x1 = int(x1)
        y1 = int(y1)
        x2 = int(x2)
        y2 = int(y2)
    except (TypeError, ValueError):
        return JsonResponse({'success': False, 'error': 'Invalid input numbers'}, status=400)

    curr = time.time()

    # Get current parameters
    a = request.session['a']
    d = request.session['d']
    new_p = request.session['new_p']

    # Determine curve type
    if request.session['opt'] == '1':
        curve = t_edwards
    else:
        curve = s_curve

    no_of_points = request.session['no_of_points']
    x_res, y_res = curve.addpoints(a, d, new_p, (x1, y1), (x2, y2), no_of_points)

    return JsonResponse({
        'success': True,
        'x_res': x_res,
        'y_res': y_res
    })


def calc(request, start=0):
    # Check if parameters are set
    if not request.session.get('set', False):
        return render(request, 'base/notset.html')

    curr = time.time()
    # Get current parameters
    a = request.session['a']
    d = request.session['d']
    new_p = request.session['new_p']
    start = int(start)

    # Determine curve type
    if request.session['opt'] == '1':
        curve = t_edwards
    else:
        curve = s_curve

    # Calculate current parameters hash
    current_hash = hash((a, d, new_p))

    limit = new_p <= 100000007
    # Check if we need to recalculate no_of_points
    if limit and ('params_hash' not in request.session or
                  'no_of_points' not in request.session or
                  request.session['params_hash'] != current_hash):
        # Recalculate and cache the number of points
        request.session['no_of_points'] = curve.num_points(a, d, new_p)
        request.session['params_hash'] = current_hash

    # Get the cached number of points
    no_of_points = request.session['no_of_points']

    # Generate points for current chunk
    if request.session['type_opt'] == '1':
        points = curve.points_on_curve(a, d, new_p, start)

    elif request.session['type_opt'] == '2':
        array = curve.generatePoints(a, d, new_p, start)
        points = curve.generator_points(a, d, new_p, no_of_points, array)

    # Handle POST operations
    if request.method == "POST":
        opt_form = forms.opt_form(request.POST)
        if opt_form.is_valid():
            opt = opt_form.cleaned_data['opt']
            x1 = opt_form.cleaned_data['x1']
            y1 = opt_form.cleaned_data['y1']
            x2 = opt_form.cleaned_data['x2']
            y2 = opt_form.cleaned_data['y2']

            x_res, y_res = 0, 0
            if opt == '2':
                x_res, y_res = curve.addpoints(a, d, new_p, (x1, y1), (x2, y2), no_of_points)
            elif opt == '3':
                x_res, y_res = curve.substractpoints(a, d, new_p, (x1, y1), (x2, y2), no_of_points)
            elif opt == '4':
                x_res, y_res = curve.doublepoint(a, d, new_p, (x1, y1), no_of_points)
            elif opt == '5':
                x_res, y_res = curve.multiplypoint(a, d, new_p, (x1, y1), x2, no_of_points)
            elif opt == '6':
                x_res, y_res = curve.order_of_point(a, d, new_p, (x1, y1), no_of_points)

            return render(request, 'base/calculate.html', {
                'opt_form': opt_form,
                'a': a,
                'd': d,
                'p': new_p,
                'no_of_points': no_of_points,
                'xarray': points[0],
                'yarray': points[1],
                'plot1': '123',
                'plot2': '678',
                'xarray2': points[0],
                'yarray2': points[1],
                'Array': zip(points[0], points[1]),
                'Array2': [(0, 1), (1, 2), (3, 4)],
                'start2': 0,
                'end2': 0,
                'point_count2': 2,
                'point_count': len(points[0]),
                'x_res': x_res,
                'y_res': y_res,
                'result': True,
                'start': start,
                'end': min(new_p - 1, start + 999),
                'prev': max(0, start - 1000),
                'next': min(new_p - 1, start + 1000),
                'p_minus_1': new_p - 1,
                'curve': request.session['opt'],
                'limit': limit,
                'time': round((time.time() - curr) * 1000, 3)
            })

    # Handle GET request
    opt_form = forms.opt_form()
    return render(request, 'base/calculate.html', {
        'opt_form': opt_form,
        'a': a,
        'd': d,
        'p': new_p,
        'no_of_points': no_of_points,
        'xarray': points[0],
        'yarray': points[1],
        'plot1': '123',
        'plot2': '678',
        'xarray2': points[0],
        'yarray2': points[1],
        'Array': zip(points[0], points[1]),
        'Array2': zip(points[0], points[1]),
        'start2': start,
        'end2': min(new_p - 1, start + 999),
        'point_count2': len(points[0]),
        'point_count': len(points[0]),
        'start': start,
        'end': min(new_p - 1, start + 999),
        'prev': max(0, start - 1000),
        'next': min(new_p - 1, start + 1000),
        'p_minus_1': new_p - 1,
        'curve': request.session['opt'],
        'limit': limit,
        'time': round((time.time() - curr) * 1000, 3),
    })

