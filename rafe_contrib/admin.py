from django.contrib import admin
from .models import (
    rafe_contrib_Profile, rafe_contrib_Work, rafe_contrib_Skill, rafe_contrib_Education, rafe_contrib_Achievements
)
    

admin.site.register(rafe_contrib_Work)
admin.site.register(rafe_contrib_Profile)
admin.site.register(rafe_contrib_Skill)
admin.site.register(rafe_contrib_Education)
admin.site.register(rafe_contrib_Achievements)

admin.site.site_header = "Progenex Administration"