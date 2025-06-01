from django import forms
from django.shortcuts import render
from base import forms
from base.curves import *
from django.http import JsonResponse
from django.template.loader import render_to_string

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
            a = request.session['a'] = adp_form.cleaned_data['a']
            d = request.session['d'] = adp_form.cleaned_data['d']
            p = request.session['p'] = adp_form.cleaned_data['p']
            request.session['set'] = True
            new_p = request.session['new_p'] = nextprime(p-1)
            lo = request.session['lo'] = int(new_p + 1 - 2*(new_p**0.5))
            hi = request.session['hi'] = int(new_p + 1 + 2*(new_p**0.5))
            prime = (new_p == p)

            return render(request, 'base/home.html', {'adp_form': adp_form, 'stage': 2, 'a': a, 'd': d, 'p': p, 'new_p': new_p, 'lo': lo, 'hi': hi, 'prime': prime})
    return render(request, 'base/home.html', {'adp_form': adp_form, 'stage': 1})

# Find Points on the curve
def point(request):
    start = request.GET.get('start')
    if start != "":
        start = int(start)
    else:
        start =0

    print("callling inside views",start)

    # Check if parameters are set
    if not request.session.get('set', False):
        return render(request, 'base/notset.html')

    # Get current parameters
    a = request.session['a']
    d = request.session['d']
    new_p = request.session['new_p']

    # Determine curve type
    if request.session['opt'] == '1':
        curve = t_edwards
    else:
        curve = s_curve

    # Get the cached number of points
    no_of_points = request.session['no_of_points']

    points = curve.points_on_curve(a, d, new_p, start)
    Array = list(zip(points[0], points[1]))

    print("callling inside views", start)

    context = {
        'start' : start,
        'end' : min(new_p - 1, start + 999),
        'point_count': len(points[0]),
        'Array' : Array,
        'plot_id' : 'point_plot',
        'name': 'Points'
    }
    # Render templates
    points_html = render_to_string('base/point.html', context)

    return JsonResponse({
        'success': True,
        'point_html': points_html,
        'xarray': points[0],
        'yarray': points[1],
        'p': new_p,
        'plot1':'123',
        'Array': Array,
        'point_count': len(points[0]),
        'start': start,
        'end': min(new_p - 1, start + 999),
        'prev': max(0, start - 1000),
        'next': min(new_p - 1, start + 1000),
    })

# Find Generator Points In the curve
def proceed(request):
    x1 = request.GET.get('x1')
    y1 = request.GET.get('y1')
    x2 = request.GET.get('x2')
    y2 = request.GET.get('y2')
    opt = request.GET.get('opt')
    start = request.GET.get('start')
    start = int(start)

    # Check if parameters are set
    if not request.session.get('set', False):
        return render(request, 'base/notset.html')

        # Validate that all inputs are present and valid numbers

    if x1 !="":
        x1 = int(x1)
    if y1 != "":
        y1 = int(y1)
    if x2 != "":
        x2 = int(x2)
    if y2 != "":
        y2 = int(y2)

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

    if new_p > 100000007:
        no_of_points = 0

    Time = time.time()

    if opt == "2":
        print(no_of_points)
        x_res, y_res = curve.addpoints(a, d, new_p, (x1, y1), (x2, y2), no_of_points)
        Time = time.time() -Time

    elif opt == "3":
        x_res, y_res = curve.substractpoints(a, d, new_p, (x1, y1), (x2, y2), no_of_points)
        Time = time.time() -Time

    elif opt == "4":
        x_res, y_res = curve.doublepoint(a, d, new_p, (x1, y1), no_of_points)
        Time = time.time() -Time

    elif opt == "5":
        x_res, y_res = curve.multiplypoint(a, d, new_p, (x1, y1), x2, no_of_points)
        Time = time.time() -Time

    elif opt == "6":
        if new_p>100000007 :
            return JsonResponse({
                'success': True,
                'type': 1,
                'order': "Unable to find point order",
                'Time': round((time.time() - Time) * 1000, 3),
            })
        x_res, y_res = curve.order_of_point(a, d, new_p, (x1, y1), no_of_points)
        Time = time.time() -Time
        if y_res == -1:
            return JsonResponse({
                'success': True,
                'type': 1,
                'order': "Inverse Doesn't Exist",
                'Time': round((Time)*1000, 3),
            })
        return JsonResponse({
            'success': True,
            'type':1,
            'order': x_res,
            'Time': round((Time)*1000, 3)
        })

    else:
        if new_p > 100000007:
            return JsonResponse({
                'success': True,
                'type': 4,
                'out': 'Take large time to compute',
                'Time': round((time.time() - Time) * 1000, 3)
            })
        array = curve.generatePoints(a, d, new_p, start)
        gen_points = curve.generator_points(a, d, new_p, no_of_points, array)
        Time =  time.time() - Time
        Array= zip(gen_points[0], gen_points[1])

        if len(gen_points[0])==0:
            return JsonResponse({
                'success': True,
                'type': 4,
                'out': 'No Generator Point',
                'Time': round((time.time() - Time) * 1000, 3)
            })
        # Prepare context
        context = {
            'xarray': gen_points[0],
            'yarray': gen_points[1],
            'plot_id': 'generator_plot',  # make sure unique
            'start': start,
            'end': min(new_p - 1, start + 999),
            'point_count': len(gen_points[0]),
            'Array': Array,
            'curve': request.session.get('opt'),  # if needed by graph.html
            'p': new_p,  # modulus value, needed for title
            'name': 'Generator Points'
        }

        # Render templates
        graph_html = render_to_string('base/graph.html', context)
        points_html = render_to_string('base/point.html', context)

        return JsonResponse({
            'success': True,
            'type': 3,
            'point_html': points_html,
            'p': new_p,  # Required for graph title
            'xarray': gen_points[0],
            'yarray': gen_points[1],
            'Array': list(Array),
            'name': 'generator_plot',
            'point_count': len(gen_points[0]),
            'start':start,
            'end':min(new_p - 1, start + 999),
            'Time': round((Time)*1000, 3)
        })

    if y_res == -1:
        return JsonResponse({
            'success': True,
            'type': 1,
            'order': "Inverse Doesn't Exist",
            'Time': round((Time) * 1000, 3),
        })

    return JsonResponse({
        'success': True,
        'type': 2,
        'x_res': x_res,
        'y_res': y_res,
        'Time': round((Time)*1000, 3)
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

    limit = new_p<= 100000007
    # Check if we need to recalculate no_of_points
    if limit and ('params_hash' not in request.session or
            'no_of_points' not in request.session or
            request.session['params_hash'] != current_hash):
        # Recalculate and cache the number of points
        request.session['no_of_points'] = curve.num_points(a, d, new_p)
        request.session['params_hash'] = current_hash

    # Get the cached number of points
    no_of_points = request.session['no_of_points']

    points = curve.points_on_curve(a, d, new_p, start)

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
        'plot1':'123',
        'Array': zip(points[0], points[1]),
        'point_count': len(points[0]),
        'start': start,
        'end': min(new_p - 1, start + 999),
        'prev': max(0, start - 1000),
        'next': min(new_p - 1, start + 1000),
        'p_minus_1': new_p - 1,
        'curve': request.session['opt'],
        'limit': limit,
        'time': round((time.time() - curr)*1000, 3),
    })

