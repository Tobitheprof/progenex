from django.contrib import admin
from .models import *


class WorkAdmin(admin.ModelAdmin):
    list_display = ['owner', 'title', 'org_name', 'start', 'stop' ]
    
    
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['owner', 'user_id', 'address', 'occupation', 'profile_img', 'twitter_link', 'linkedin_link', 'phone_number']

    def user(self, profile):
        return f'{profile.owner}'

class SkillAdmin(admin.ModelAdmin):
    list_display = ['owner', 'name', 'proficiency']


class EdAdmin(admin.ModelAdmin):
    list_display = ['owner', 'institution', 'degree', 'course_of_study', 'start', 'stop', 'description']

class AchievementAdmin(admin.ModelAdmin):
    list_display = ['owner', 'title', 'description']


admin.site.register(Work, WorkAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Skill, SkillAdmin)
admin.site.register(Education, EdAdmin)
admin.site.register(Achievements, AchievementAdmin)

admin.site.site_header = "Progenex Administration"

# Register your models here.
