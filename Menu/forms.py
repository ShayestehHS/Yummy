from django import forms

from Menu.models import Item


class MenuForm(forms.ModelForm):
    class Meta:
        model = Item
        exclude = ('menu',)
        widgets = {
            'description': forms.Textarea(
                attrs={
                    'style': 'resize:vertical',
                    'rows': 4,
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super(MenuForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
