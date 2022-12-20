from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [

    #Uauthenticated Views Start
    path('', views.index, name="index"),
    path('login', views.login, name="login"),
    path('register', views.register, name="register"),
    #Uauthenticated Views End
    
    #-------------Authenticated URLs Start------------#
    path('home/', views.home, name="home"),
    path('education', views.education, name="education"),
    path('skills', views.skills, name="skills"),
    path('delete_work/<int:pk>/', views.delete_work, name='del-work'),
    path('delete_skill/<int:pk>', views.delete_skill, name="del-skill"),
    path('delete_education/<int:pk>', views.delete_education, name="del-edu"),
    path('delete_achievement/<int:pk>', views.del_ach, name="del-ach"),
    path('personal-and-contact-information', views.p_and_c, name="p-and-c"),
    path('work', views.work, name="work"),
    path('achievements/', views.achievements, name="achievements"),
    path('logout', views.logout, name="logout"),
    path('progenex/resume/<str:pk>', views.resume, name="resume"),
    #-------------Authenticated URLs End--------------#


    #------------------- PAssowrd Reset Views Start ------------------#
    path(
        'reset_password/',
        auth_views.PasswordResetView.as_view(
            template_name="password_reset.html"),
        name="reset_password"),
    path(
        'reset_password_sent/',
        auth_views.PasswordResetDoneView.as_view(
            template_name="password_reset_sent.html"),
        name="password_reset_done"),
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name="password_reset_form.html"),
        name="password_reset_confirm"),
    path(
        'reset_password_success/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name="password_reset_done.html"),
        name="password_reset_complete"),
    #------------------- PAssowrd Reset Views End ------------------#

]