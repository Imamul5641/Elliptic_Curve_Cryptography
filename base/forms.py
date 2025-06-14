from django import forms
from django.core.exceptions import ValidationError

class adp_form(forms.Form):
    opt_choices = (
    ('1', "Twisted Edwards"),
    ('2', "Short Weirstrass")
    )

    opt = forms.ChoiceField(choices = opt_choices)
    a = forms.IntegerField(min_value=2,label='a')
    d = forms.IntegerField(min_value=1,label='d')
    p = forms.IntegerField(min_value=3,label='p')

    def clean_d(self):
        a = self.cleaned_data['a']
        d = self.cleaned_data['d']
        if a == d:
            raise ValidationError("Values of a and b cannot be equal!")
        return d

class opt_form(forms.Form):
    opt_choices = (
    ('2', "Addition (+)"),
    ('3', "Subtraction (-)"),
    ('4', "Doubling (x2)"),
    ('5', "Scalar Multiplication (xScalar)"),
    ('6', 'Order of the Point'),
    ('7', 'Generator Points'),
    )
    opt = forms.ChoiceField(choices = opt_choices)
    x1 = forms.IntegerField()
    y1 = forms.IntegerField()
    x2 = forms.IntegerField(required=False)
    y2 = forms.IntegerField(required=False)

    def clean_x2(self):
        opt = self.cleaned_data['opt']
        x2 = self.cleaned_data['x2']
        if (opt == '2' or opt == '3' or opt == '5') and x2 == None:
            raise ValidationError("x2: Value required!")
        return x2
    
    def clean_y2(self):
        opt = self.cleaned_data['opt']
        y2 = self.cleaned_data['y2']
        if (opt == '2' or opt == '3') and y2 == None:
            raise ValidationError("y2: Value required!")
        return y2