from django import forms

class DayOfWeekForm(forms.Form):
	DAY_OF_THE_WEEK = [
            ('1', "Monday"),
            ('2', "Tuesday"),
            ('3', "Wednesday"),
            ('4', "Thursday"),
            ('5', "Friday"),
            ('6', "Saturday"),
            ('7', "Sunday"),
	]
	day_of_week = forms.ChoiceField(choices=DAY_OF_THE_WEEK, required=True)
	
class CategoryFilterForm(forms.Form):
    CATEGORY_CHOICES = [
        ('all', 'All'),
        ('striking', 'Striking'),
        ('grappling', 'Grappling'),
    ]
    category = forms.ChoiceField(choices=CATEGORY_CHOICES, widget=forms.RadioSelect, required=True)