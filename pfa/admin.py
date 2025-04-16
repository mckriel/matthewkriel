from django.contrib import admin
from django.contrib.admin.models import LogEntry
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

class ClassInstanceAdmin(LoggingAdmin):
    list_display = ('training_class', 'weekday', 'start_time', 'end_time')
    
class ClassAdmin(LoggingAdmin):
    list_display = ('name',)

class ClassCategoryAdmin(LoggingAdmin):
    list_display = ('category',)

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

admin.site.register(LogEntry, LogEntryAdmin)
admin.site.register(ClassInstance, ClassInstanceAdmin)
admin.site.register(Class, ClassAdmin)
admin.site.register(ClassCategory, ClassCategoryAdmin)
