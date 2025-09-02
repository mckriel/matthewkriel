from django.contrib import admin
from django.contrib.admin.models import LogEntry
from django.utils.html import format_html
from django.db.models import Q
from django.shortcuts import render
from django.urls import path
from django.http import HttpResponse
from django.template.response import TemplateResponse
from .models import Class, ClassCategory, ClassInstance
import logging

logger = logging.getLogger('pfa')

class LoggingAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if change:
            operation = 'Updated'
            logger.info(f"ADMIN ACTION: {operation} {obj._meta.model_name} {obj.pk} by {request.user.username}")
        else:
            operation = 'Created'
            logger.info(f"ADMIN ACTION: {operation} {obj._meta.model_name} by {request.user.username}")
        super().save_model(request, obj, form, change)
    
    def delete_model(self, request, obj):
        logger.info(f"ADMIN ACTION: Deleted {obj._meta.model_name} {obj.pk} by {request.user.username}")
        super().delete_model(request, obj)

class ClassInstanceInline(admin.TabularInline):
    model = ClassInstance
    extra = 1
    fields = ('weekday', 'start_time', 'end_time', 'time_span')
    readonly_fields = ('time_span',)
    
    def get_queryset(self, request):
        """Order instances by weekday and start time"""
        return super().get_queryset(request).order_by('weekday', 'start_time')

class ClassInstanceAdmin(LoggingAdmin):
    list_display = (
        'class_name_colored', 'weekday_display', 'time_display', 
        'duration_display', 'categories_display', 'last_updated'
    )
    list_filter = (
        'weekday', 
        'training_class__class_categories',
        'training_class',
        'start_time',
    )
    search_fields = ('training_class__name',)
    ordering = ('weekday', 'start_time')
    list_per_page = 50
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('schedule/', self.admin_site.admin_view(weekly_schedule_view), name='pfa_weekly_schedule'),
        ]
        return custom_urls + urls
    
    # Custom display methods
    def class_name_colored(self, obj):
        """Display class name with color coding by category"""
        categories = obj.training_class.class_categories.all()
        if categories:
            category = categories.first().category
            colors = {
                'Striking': '#e74c3c',    # Red
                'Grappling': '#3498db',   # Blue  
                'Fitness': '#27ae60',     # Green
                'Lifestyle': '#f39c12'    # Orange
            }
            color = colors.get(category, '#34495e')
            return format_html(
                '<span style="color: {}; font-weight: bold;">{}</span>',
                color, obj.training_class.name
            )
        return obj.training_class.name
    class_name_colored.short_description = 'Class'
    class_name_colored.admin_order_field = 'training_class__name'
    
    def weekday_display(self, obj):
        """Display weekday with better formatting"""
        day_colors = {
            '1': '#e74c3c',  # Monday - Red
            '2': '#e67e22',  # Tuesday - Orange  
            '3': '#f1c40f',  # Wednesday - Yellow
            '4': '#27ae60',  # Thursday - Green
            '5': '#3498db',  # Friday - Blue
            '6': '#9b59b6',  # Saturday - Purple
            '7': '#95a5a6'   # Sunday - Grey
        }
        color = day_colors.get(obj.weekday, '#34495e')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color, obj.get_weekday_display()
        )
    weekday_display.short_description = 'Day'
    weekday_display.admin_order_field = 'weekday'
    
    def time_display(self, obj):
        """Display time with better formatting"""
        return format_html(
            '<span style="font-family: monospace; font-weight: bold;">{} - {}</span>',
            obj.start_time.strftime('%H:%M'),
            obj.end_time.strftime('%H:%M')
        )
    time_display.short_description = 'Time'
    time_display.admin_order_field = 'start_time'
    
    def duration_display(self, obj):
        """Display duration with minutes"""
        return f"{obj.time_span} min"
    duration_display.short_description = 'Duration'
    duration_display.admin_order_field = 'time_span'
    
    def categories_display(self, obj):
        """Display all categories for the class"""
        categories = obj.training_class.class_categories.all()
        if categories:
            return " + ".join([cat.category for cat in categories])
        return "-"
    categories_display.short_description = 'Categories'
    
    def last_updated(self, obj):
        """Display last updated time"""
        return obj.updated.strftime('%Y-%m-%d %H:%M')
    last_updated.short_description = 'Last Updated'
    last_updated.admin_order_field = 'updated'

class ClassAdmin(LoggingAdmin):
    list_display = ('name', 'categories_display', 'instance_count', 'last_updated')
    list_filter = ('class_categories', 'created')
    search_fields = ('name',)
    filter_horizontal = ('class_categories',)
    inlines = [ClassInstanceInline]
    
    def categories_display(self, obj):
        """Display categories with color coding"""
        categories = obj.class_categories.all()
        if not categories:
            return "-"
        
        colored_cats = []
        colors = {
            'Striking': '#e74c3c',
            'Grappling': '#3498db', 
            'Fitness': '#27ae60',
            'Lifestyle': '#f39c12'
        }
        
        for cat in categories:
            color = colors.get(cat.category, '#34495e')
            colored_cats.append(
                format_html('<span style="color: {};">{}</span>', color, cat.category)
            )
        return format_html(' + '.join(colored_cats))
    categories_display.short_description = 'Categories'
    
    def instance_count(self, obj):
        """Show how many instances (schedule slots) this class has"""
        count = obj.classinstance_set.count()
        return format_html('<strong>{}</strong> slots', count)
    instance_count.short_description = 'Schedule Slots'
    
    def last_updated(self, obj):
        return obj.updated.strftime('%Y-%m-%d %H:%M')
    last_updated.short_description = 'Last Updated'
    last_updated.admin_order_field = 'updated'

class ClassCategoryAdmin(LoggingAdmin):
    list_display = ('category', 'class_count', 'total_instances')
    
    def class_count(self, obj):
        """Show how many classes use this category"""
        count = obj.class_set.count()
        return f"{count} classes"
    class_count.short_description = 'Classes Using'
    
    def total_instances(self, obj):
        """Show total schedule instances for this category"""
        count = ClassInstance.objects.filter(
            training_class__class_categories=obj
        ).count()
        return f"{count} schedule slots"
    total_instances.short_description = 'Total Schedule Slots'

# Register custom admin log entry view
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ('action_time', 'user', 'content_type', 'object_repr', 'action_flag')
    list_filter = ('action_time', 'user', 'content_type')
    search_fields = ('object_repr', 'change_message')
    readonly_fields = ('action_time', 'user', 'content_type', 'object_id', 'object_repr', 'action_flag', 'change_message')
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False

# Weekly schedule view function with admin authentication
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def weekly_schedule_view(request):
    """Custom weekly schedule grid view"""
    # Get all class instances grouped by weekday
    schedule_data = {}
    weekdays = [
        ('1', 'Monday'),
        ('2', 'Tuesday'), 
        ('3', 'Wednesday'),
        ('4', 'Thursday'),
        ('5', 'Friday'),
        ('6', 'Saturday'),
        ('7', 'Sunday')
    ]
    
    for day_num, day_name in weekdays:
        instances = ClassInstance.objects.filter(
            weekday=day_num, deleted=0
        ).select_related('training_class').prefetch_related(
            'training_class__class_categories'
        ).order_by('start_time')
        
        schedule_data[day_name] = {
            'day_num': day_num,
            'classes': instances
        }
    
    context = {
        'title': 'Weekly Schedule Overview',
        'schedule_data': schedule_data,
        'site_title': admin.site.site_title,
        'site_header': admin.site.site_header,
        'has_permission': True,
    }
    
    return render(request, 'admin/pfa/weekly_schedule.html', context)

# Override the main admin site to customize PFA app index
class CustomAdminSite(admin.AdminSite):
    def app_index(self, request, app_label, extra_context=None):
        if app_label == 'pfa':
            # Get schedule data for PFA app index
            schedule_data = {}
            weekdays = [
                ('1', 'Monday'), ('2', 'Tuesday'), ('3', 'Wednesday'),
                ('4', 'Thursday'), ('5', 'Friday'), ('6', 'Saturday'), ('7', 'Sunday')
            ]
            
            for day_num, day_name in weekdays:
                instances = ClassInstance.objects.filter(
                    weekday=day_num, deleted=0
                ).select_related('training_class').prefetch_related(
                    'training_class__class_categories'
                ).order_by('start_time')
                
                schedule_data[day_name] = {
                    'day_num': day_num,
                    'classes': instances
                }
            
            if extra_context is None:
                extra_context = {}
            extra_context['schedule_data'] = schedule_data
            
        return super().app_index(request, app_label, extra_context)

# Replace the default admin site
admin.site.__class__ = CustomAdminSite

admin.site.register(LogEntry, LogEntryAdmin)
admin.site.register(ClassInstance, ClassInstanceAdmin)
admin.site.register(Class, ClassAdmin)
admin.site.register(ClassCategory, ClassCategoryAdmin)
