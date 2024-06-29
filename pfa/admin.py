from django.contrib import admin
from .models import Class, ClassCategory, ClassInstance

class ClassInstanceAdmin(admin.ModelAdmin):
	list_display = ('training_class', 'weekday', 'start_time', 'end_time')
	
admin.site.register(ClassInstance, ClassInstanceAdmin)
admin.site.register(Class)
