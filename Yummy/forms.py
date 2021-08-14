from django import forms
from django.forms import RadioSelect

import Users.models as users_models
import Yummy.models as yummy_models


class DriverForm(forms.ModelForm):
    Choice = [(True, 'Yes'), (False, 'No')]
    motorbike = forms.BooleanField(widget=RadioSelect(choices=Choice))
    student = forms.BooleanField(widget=RadioSelect(choices=Choice))
    driver_lic = forms.BooleanField(widget=RadioSelect(choices=Choice))
    mobile = forms.BooleanField(widget=RadioSelect(choices=Choice))
    phone_number = forms.IntegerField()

    class Meta:
        model = users_models.Driver
        fields = (
            'phone_number', 'motorbike', 'student', 'driver_lic', 'mobile')

    def __init__(self, *args, **kwargs):
        super(DriverForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if type(field).__name__ == "BooleanField":
                field.initial = True


class SubmitRestaurantForm(forms.ModelForm):
    class Meta:
        model = yummy_models.Restaurant
        fields = ('phone_number', 'name',
                  'website_url', 'is_delivery', 'is_take_away',
                  'long', 'lat', 'postal_code',)


class NewReviewForm(forms.ModelForm):
    Rating = [
        (5, "Perfect"),
        (4, "Good"),
        (3, "Not bad"),
        (2, "Bad"),
        (1, "Too bad"),
        (0, "Awful"),
    ]
    food_quality = forms.ChoiceField()
    price = forms.ChoiceField()
    punctuality = forms.ChoiceField()
    courtesy = forms.ChoiceField()

    class Meta:
        model = yummy_models.RestaurantReview
        fields = (
            'food_quality', 'price', 'punctuality', 'courtesy', 'description')
        widgets = {
            'description': forms.Textarea(
                attrs={'style': 'resize:vertical', 'rows': 4})
        }

    def __init__(self, *args, **kwargs):
        super(NewReviewForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if type(field).__name__ == "ChoiceField":
                field.choices = NewReviewForm.Rating
                field.widgets = forms.Select
