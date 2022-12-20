from django.urls import path
from . import views

urlpatterns = [
            # ****** unauthenticated views start ****** #       
    path(
        '',
        views.index,
        name='rafe_contrib-index'
    ),
    
    path(
        'register/',
        views.register,
        name='rafe_contrib-register'
    ),
    
    path(
        'login/',
        views._login,
        name='rafe_contrib-login'
    ),
    
    path(
        'logout/',
        views._logout,
        name='rafe_contrib-logout'
    ),
    
            # ****** unauthenticated views end ****** #     

            # ****** authenticated views start ****** #
    path(
        'home/',
        views.home,
        name='rafe_contrib-home'
    ),
    
    path(
        'achievements/',
        views.achievements,
        name='rafe_contrib-achievements'
    ),
    
    path(
        'education/',
        views.education,
        name='rafe_contrib-education'
    ),
    
    path(
        'personal&contact/',
        views.personal_c,
        name='rafe_contrib-personal_contact'
    ),
    
    path(
        'skill/',
        views.skill,
        name='rafe_contrib-skills'
    ),
    
    path(
        'work/',
        views.work,
        name='rafe_contrib-work'
    ),
    
            # ****** authenticated views end ****** #

            # ****** Delete items ****** #      
    path(
        'delete_achievement/<int:pk>',
        views.del_ach,
        name="rafe_contrib-delete-achievement"
    ),
    
    path(
        'delete_work/<int:pk>',
        views.delete_work,
        name="rafe_contrib-delete-work"
    ),
    
    path(
        'delete_education/<int:pk>',
        views.delete_education,
        name="rafe_contrib-delete-education"
    ),
    
    path(
        'delete_education/<int:pk>',
        views.delete_skill,
        name="rafe_contrib-delete-skill"
    ),
    
            # ****** Delete items end ****** #      
]
