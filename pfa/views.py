from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.utils import timezone
from .models import ClassInstance
from .forms import DayOfWeekForm, CategoryFilterForm
import urllib.parse
import logging
import json
import socket
import datetime

logger = logging.getLogger('pfa')

def fitness_class_view(request):
    logger.info(f"Schedule view accessed by {request.user} from {request.META.get('REMOTE_ADDR')} via {request.META.get('HTTP_USER_AGENT')}")
    
    try:
        class_list = ClassInstance.objects.all()
        current_day = timezone.now().weekday() + 1
        
        # Get the selected day and category from URL parameters or default to current day and 'all'
        selected_day = int(request.GET.get('day', current_day))
        selected_category = request.GET.get('category', 'all')

        logger.debug(f"Initial query parameters: day={selected_day}, category={selected_category}")

        if request.method == 'POST':
            logger.info(f"POST request received with data: {json.dumps(dict(request.POST))}")
            day_form = DayOfWeekForm(request.POST)
            selected_category = request.POST.get('category', 'all')
            
            if day_form.is_valid():
                selected_day = day_form.cleaned_data['day_of_week']
                query_params = urllib.parse.urlencode({'day': selected_day, 'category': selected_category})
                logger.debug(f"Form valid, redirecting with params: {query_params}")
                return HttpResponseRedirect(f"{reverse('pfa')}?{query_params}")
            else:
                logger.warning(f"Form validation failed with errors: {day_form.errors}")
        else:
            day_form = DayOfWeekForm(initial={'day_of_week': selected_day})
        
        # Log filter operations
        logger.debug(f"Filtering by day={selected_day}, category={selected_category}")
        
        if selected_category == 'striking':
            class_list = class_list.filter(training_class__class_categories__category='Striking')
        elif selected_category == 'grappling':
            class_list = class_list.filter(training_class__class_categories__category='Grappling')
        
        class_list = class_list.filter(weekday=selected_day).order_by('start_time')
        
        # Log query results
        logger.debug(f"Query returned {class_list.count()} classes")
        
        for cls in class_list:
            logger.debug(f"Class in view: {cls.training_class} | {cls.get_weekday_display()} | {cls.start_time}-{cls.end_time} | Last updated: {cls.updated}")
        
        context = {
            'day_form': day_form,
            'class_list': class_list,
            'selected_day': selected_day,
            'selected_category': selected_category,
        }
        
        return render(request, 'pfa/index.html', context)
        
    except Exception as e:
        logger.error(f"Error in fitness_class_view: {str(e)}", exc_info=True)
        raise


# from django.shortcuts import render
# from django.utils import timezone
# from .models import ClassInstance
# from .forms import DayOfWeekForm, CategoryFilterForm
# import datetime
# 
# 	
# def fitness_class_view(request):
# 	class_list = ClassInstance.objects.all()
# 	selected_day = None
# 	selected_category = 'all'
# 	
# 	current_day = timezone.now().weekday() + 1
# 	
# 	if request.method == 'POST':
# 		day_form = DayOfWeekForm(request.POST)
# 		selected_category = request.POST.get('category', 'all')
# 		
# 		if day_form.is_valid():
# 			selected_day = day_form.cleaned_data['day_of_week']
# 			class_list = class_list.filter(weekday=selected_day).order_by('start_time')
# 			
# 		if selected_category == 'striking':
# 			class_list = class_list.filter(training_class__class_categories__category='Striking')
# 		elif selected_category == 'grappling':
# 			class_list = class_list.filter(training_class__class_categories__category='Grappling')
# 			
# 	else:
# 		day_form = DayOfWeekForm(initial={'day_of_week': current_day})
# 		selected_day = current_day
# 		class_list = class_list.filter(weekday=selected_day).order_by('start_time')
# 	
# 	context = {
# 		'day_form': day_form,
# 		'class_list': class_list,
# 		'selected_day': selected_day,
# 		'selected_category': selected_category,
# 	}
# 	return render(request, 'pfa/index.html', context)
# 		