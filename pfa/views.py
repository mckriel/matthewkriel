from django.shortcuts import render
from django.utils import timezone
from .models import ClassInstance
from .forms import DayOfWeekForm, CategoryFilterForm
import datetime

	
def fitness_class_view(request):
	class_list = ClassInstance.objects.all()
	selected_day = None
	selected_category = 'all'
	
	current_day = timezone.now().weekday() + 1
	
	if request.method == 'POST':
		day_form = DayOfWeekForm(request.POST)
		selected_category = request.POST.get('category', 'all')
		
		if day_form.is_valid():
			selected_day = day_form.cleaned_data['day_of_week']
			class_list = class_list.filter(weekday=selected_day).order_by('start_time')
			
		if selected_category == 'striking':
			class_list = class_list.filter(training_class__class_categories__category='Striking')
		elif selected_category == 'grappling':
			class_list = class_list.filter(training_class__class_categories__category='Grappling')
			
	else:
		day_form = DayOfWeekForm(initial={'day_of_week': current_day})
		selected_day = current_day
		class_list = class_list.filter(weekday=selected_day).order_by('start_time')
	
	context = {
		'day_form': day_form,
		'class_list': class_list,
		'selected_day': selected_day,
		'selected_category': selected_category,
	}
	return render(request, 'pfa/index.html', context)
		