from django.contrib import admin
from django.contrib.admin import AdminSite
from .models import Position, EmployeePosition, EmployeeProfile, Notification
from django.conf import settings
from django.contrib.auth.models import Group
from main.models import MyUser
from chat.models import Message
from forum.models import Post, Topic

class MultiDBModelAdmin(admin.ModelAdmin):
    # A handy constant for the name of the alternate database.
    using = settings.ADMIN_DB

    def save_model(self, request, obj, form, change):
        # Tell Django to save objects to the 'other' database.
        obj.save(using=self.using)

    def delete_model(self, request, obj):
        # Tell Django to delete objects from the 'other' database
        obj.delete(using=self.using)

    def get_queryset(self, request):
        # Tell Django to look for objects on the 'other' database.
        return super().get_queryset(request).using(self.using)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Tell Django to populate ForeignKey widgets using a query
        # on the 'other' database.
        return super().formfield_for_foreignkey(db_field, request, using=self.using, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        # Tell Django to populate ManyToMany widgets using a query
        # on the 'other' database.
        return super().formfield_for_manytomany(db_field, request, using=self.using, **kwargs)


employee_admin_site = AdminSite(name='employees')

employee_admin_site.register(MyUser, MultiDBModelAdmin)
employee_admin_site.register(Group, MultiDBModelAdmin)

employee_admin_site.register(Position, MultiDBModelAdmin)
employee_admin_site.register(EmployeePosition, MultiDBModelAdmin)
employee_admin_site.register(EmployeeProfile, MultiDBModelAdmin)
employee_admin_site.register(Notification, MultiDBModelAdmin)

employee_admin_site.register(Post, MultiDBModelAdmin)
employee_admin_site.register(Topic, MultiDBModelAdmin)
employee_admin_site.register(Message, MultiDBModelAdmin)
