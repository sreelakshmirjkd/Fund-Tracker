from django import forms

from expense.models import Transaction

from django.contrib.auth.models import User

# Using forms
# ===========

# class ExpenseCreateForm(forms.Form):

#     title = forms.CharField() # max length is mandatory in models.py 

#     # date and time should come automatically. So it's not an input.

#     amount = forms.FloatField()

#     category = forms.ChoiceField(choices=Transaction.CATEGORY_OPTIONS) 

#     # 2nd option -- copy pasting the CATEGORY_OPTIONS with the variables and then equating it to choices inside the paranthesis.

#     payment_method = forms.ChoiceField(choices=Transaction.PAYMENT_OPTIONS)

#     priority = forms.ChoiceField(choices=Transaction.PRIORITY_OPTIONS)

# ----------------------------------------------------------------------------------------------------


# Using ModelForm - create, update --- Meta, model, fields --- Don't change these variables.
# ===============

class ExpenseCreateForm(forms.ModelForm):

    class Meta:

        model = Transaction

        fields = ["title", "amount", "category", "payment_method", "priority"]

        # Style model form - widgets - dictionary with name and input fiels

        widgets = {
            
            "title": forms.TextInput(attrs={"class":"form-control mb-2"}),

            "amount": forms.NumberInput(attrs={"class":"form-control mb-2"}),
            
            "category": forms.Select(attrs={"class":"form-control form-select mb-2"}),

            "payment_method": forms.Select(attrs={"class":"form-control form-select mb-2"}),

            "priority": forms.Select(attrs={"class":"form-control form-select mb-4"})
        
        }


class SignUpForm(forms.ModelForm):

    class Meta:

        model = User

        fields = ["username", "email", "password"]

# Use Form to not create or update

class LoginForm(forms.Form):

    username = forms.CharField()

    password = forms.CharField()