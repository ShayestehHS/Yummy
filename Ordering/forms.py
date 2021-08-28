from datetime import datetime, timedelta

from django import forms
from Ordering.models import OrderDetail


def get_datetime_range_list():
    start = datetime(2021, 1, 1, hour=11, minute=30)
    end = datetime(2021, 1, 1, hour=20, minute=45)
    delta = timedelta(minutes=15)

    def get_datetime():
        current = start
        while current <= end:
            yield current
            current += delta

    datetime_range = [(dt.strftime('%H:%M'), dt.strftime('%H:%M')) for dt in get_datetime()]
    datetime_range.append(('Select time', 'Select time'))
    return datetime_range


class Step1Form(forms.ModelForm):
    delivery_time_choices = get_datetime_range_list()
    delivery_day_choices = [('Today', 'Today'),
                            ('Tomorrow', 'Tomorrow'),
                            ('Select day', 'Select day'), ]
    delivery_method_choices = [
        ('Delivery', 'Delivery'),
        ('TakeAway', 'TakeAway'),
        ('Select method', 'Select method')]

    delivery_time = forms.ChoiceField(choices=delivery_time_choices,
                                      widget=forms.Select(attrs={
                                          'class': 'form-control',
                                          'name': 'selected_dTime',
                                          'id': 'selected_dTime',
                                      }))
    delivery_day = forms.ChoiceField(choices=delivery_day_choices,
                                     widget=forms.Select(attrs={
                                         'class': 'form-control',
                                         'name': 'delivery_schedule_day',
                                         'id': 'delivery_schedule_day',
                                     }))
    delivery_method = forms.ChoiceField(choices=delivery_method_choices,
                                        widget=forms.Select(attrs={
                                            'class': 'form-control',
                                            'id': 'delivery_method',
                                            'name': 'method'
                                        }))

    class Meta:
        model = OrderDetail
        fields = ['telephone', 'full_address', 'postal_code',
                  'delivery_day', 'delivery_time', 'delivery_method',
                  'description']
        widgets = {
            'telephone': forms.NumberInput(attrs={
                'class': 'form-control',
                'name': 'tel_order',
                'id': 'tel_order',
                'label': 'Telephone/mobile',
            }),
            'full_address': forms.TextInput(attrs={
                'class': 'form-control',
                'name': 'address_order',
                'id': 'address_order',
                'maxlength': 120,
            }),
            'postal_code': forms.NumberInput(attrs={
                'class': 'form-control',
                'name': 'pcode_order',
                'id': 'pcode_order',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Any description for your order...',
                'name': 'notes',
                'id': 'notes',
                'style': "resize: vertical",
                'rows': 4,
            }),
        }

    def __init__(self,*args, **kwargs):
        super(Step1Form, self).__init__(*args, **kwargs)
        self.initial['delivery_time'] = 'Select time'
        self.initial['delivery_day'] = 'Select day'
        self.initial['delivery_method'] = 'Select method'
