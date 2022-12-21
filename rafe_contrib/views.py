from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.template.loader import get_template
from django.core.mail import EmailMessage
from time import strftime
from .models import (
    rafe_contrib_Profile, rafe_contrib_Work, rafe_contrib_Skill, rafe_contrib_Education, rafe_contrib_Achievements, RafeUser
)

"""
time spent debugging: 20hrs
hahaha, i tried my best to make this code extremely optimized and readable
if any errors are found increment the time spent debugging by the amont you spent on it, and if you do fix the error eventually make it zero
refer to docs.md for more documentation on code if i do decide to write it...
if you're using VSCodes download `better comments` extension too
"""

# ****** unauthenticated view start ****** #


def index(request):
    context = {
        'title': 'Progenx'
    }
    return render(request, 'rafe_contrib/index.html', context)


def register(request):
    if request.user.is_authenticated:
        return redirect('rafe_contrib-home')

    if request.method == 'POST':
        # ***** getting post data ****** #
        first_name = request.POST['first_name'].title()
        last_name = request.POST['last_name'].title()
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        password_confirmation = request.POST['password_confirm']
        # ***** end getting post data ****** #
        if (password == password_confirmation):
            if (len(password) < 8):
                context = {
                    'password_length_error': True,
                    'first_name': first_name,
                    'last_name': last_name,
                    'email': email,
                    'username': username,
                    'password': password,
                    'password_confirm': password_confirmation,
                }  # *Creating an instance ofthe pervious data i guess..
                return render(request, 'rafe_contrib/register.html', context)
            elif User.objects.filter(email=email).exists():
                context = {
                    'email_taken_error': True,
                    'title': 'Progenx | Register',
                    'first_name': first_name,
                    'last_name': last_name,
                    'email': email,
                    'username': username,
                    'password': password,
                    'password_confirm': password_confirmation,
                }  # *Creating an instance ofthe pervious data i guess..
                return render(request, 'rafe_contrib/register.html', context)
            elif User.objects.filter(username=username):
                context = {
                    'username_taken_error': True,
                    'first_name': first_name,
                    'title': 'Progenx | Register',
                    'last_name': last_name,
                    'email': email,
                    'username': username,
                    'password': password,
                    'password_confirm': password_confirmation,
                }  # *Creating an instance ofthe pervious data i guess..
                return render(request, 'rafe_contrib/register.html', context)
            else:
                # ctx = {
                #     'user' : username
                # }
                # message = get_template('mail.html').render(ctx)
                # msg = EmailMessage(
                #     'Welcome to Progenex',
                #     message,
                #     'Tobi from Progenex by Genxsis',
                #     [email],
                # )
                # msg.content_subtype ="html"# Main content is now text/html
                # msg.send()
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name,
                )
                user_login = authenticate(username=username, password=password)
                login(request, user_login)  # *Logs in USER
            # *Create user model and redirect to edit-profile
            try:
                user.save()
                user_model = User.objects.get(username=username)
                new_profile = rafe_contrib_Profile.objects.create(
                    owner=user_model, user_id=user_model.id
                )
                new_profile.save()
                # *Rediects to specified page once condition is met
                return redirect('rafe_contrib-personal_contact')
            except Exception as e:
                pass

        else:
            context = {
                'password_do_not_match': True,
                'first_name': first_name,
                'last_name': last_name,
                'title': 'Progenx | Register',
                'email': email,
                'username': username,
                'password': password,
                'password_confirm': password_confirmation,
            }  # *Creating an instance ofthe pervious data i guess..
            return render(request, 'rafe_contrib/register.html', context)

    context = {
        'title': 'Progenx | Register'
    }
    return render(request, 'rafe_contrib/register.html', context)


def _login(request):
    context = {
        'title': 'Progenx | Login'
    }
    if request.user.is_authenticated:
        return redirect('rafe_contrib-home')

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = authenticate(username=username, password=password)
        except Exception as e:
            print(e)

        if user is not None:
            login(request, user)
            return redirect('rafe_contrib-home')
        else:
            context = {
                'username': username,
                'password': password,
                'invalid_username_or_password': True,
                'title': 'Progenx | Login'
            }

    return render(request, 'rafe_contrib/login.html', context)


def _logout(request):
    logout(request)
    return redirect('rafe_contrib-login')
# ****** unauthenticated view end ****** #


@login_required(login_url='/rafe/login')
def home(request):
    context = {
        'title': 'Progenx | Home'
    }
    return render(request, 'rafe_contrib/home.html', context)


@login_required(login_url='/rafe/login')
def achievements(request):
    achievements = rafe_contrib_Achievements.objects.filter(owner=request.user)
    if request.method == "POST":
        title = request.POST['title']
        description = request.POST['description']
        if title != '':
            rafe_contrib_Achievements.objects.create(
                owner=request.user,
                title=title,
                description=description
            )
            context = {
                'success_msg':True,
                'msg':'to add education',
                'title': 'Progenx | Achievements',
                'achievements': achievements,
            }
            return render(request, 'rafe_contrib/achievements.html', context)
        else:
            context = {
                'title_error':True,
                'ach_title':title,
                'description':description,
                'title': 'Progenx | Achievements',
                'achievements': achievements,
            }
            return render(request, 'rafe_contrib/achievements.html', context)
  
    context = {
        'title': 'Progenx | Achievements',
        'achievements': achievements,
    }
    return render(request, 'rafe_contrib/achievements.html', context)


@login_required(login_url='/rafe/login')
def del_ach(reqeust, pk=None):
    rafe_contrib_Achievements.objects.get(id=pk).delete()
    return redirect('rafe_contrib-achievements', permanent=True)

@login_required(login_url='/rafe/login')
def education(request):
    work = rafe_contrib_Education.objects.filter(owner=request.user)
    if request.method == "POST":
        degree = request.POST['deg']
        institution = request.POST['org_name']
        course_of_study = request.POST['role']
        start_date = request.POST['org_start_date']
        end_date = request.POST['org_end_date']
        description = request.POST['role_description']
        if end_date != '':
            try:
                end_date = int(end_date)
                if end_date > int(strftime('%Y')):
                    end_date = 'present'
            except:
                end_date = 'present'
                context = {
                    'end_date_not_int_err': True,
                    'title': 'Progenx | Work',
                    'works': work,
                    'orgname': institution,
                    'role': course_of_study,
                    'startdate': start_date,
                    'enddate': end_date,
                    'description': description,
                }
                return render(request, 'rafe_contrib/education.html', context)
        else:
            end_date = 'present'
        try:
            start_date = int(start_date)
            if start_date > int(strftime('%Y')):
                start_date = int(strftime('%Y'))
        except:
            context = {
                'start_date_not_int_err': True,
                'title': 'Progenx | Work',
                'works': work,
                'orgname': institution,
                'role': course_of_study,
                'startdate': start_date,
                'enddate': end_date,
                'description': description,
            }
            return render(request, 'rafe_contrib/education.html', context)

        if institution != '':
            if start_date != '':
                if type(start_date) == int:
                    # *using 1941 since someone born 1941 would be like 80 years at the time of writing this code (2022)
                    if start_date > 1941:
                        rafe_contrib_Education.objects.create(
                            owner=request.user,
                            institution=institution,
                            degree=degree,
                            course_of_study=course_of_study,
                            start=start_date,
                            stop=end_date,
                            description=description,
                        )
                        context = {
                            'success_msg': True,
                            'msg': 'to add skills',
                            'title': 'Progenx | Work',
                            'works': work,
                        }
                        return render(request, 'rafe_contrib/education.html', context)
                    else:
                        context = {
                            'start_date_err': True,
                            'title': 'Progenx | Work',
                            'works': work,
                            'orgname': institution,
                            'role': course_of_study,
                            'startdate': start_date,
                            'enddate': end_date,
                            'description': description,
                        }
                        return render(request, 'rafe_contrib/education.html', context)

            elif start_date == '':
                context = {
                    'start_date_err': True,
                    'title': 'Progenx | Work',
                    'works': work,
                    'orgname': institution,
                    'role': course_of_study,
                    'startdate': start_date,
                    'enddate': end_date,
                    'description': description,
                }
                return render(request, 'rafe_contrib/education.html', context)
            else:
                context = {
                    'end_date_err': True,
                    'title': 'Progenx | Work',
                    'works': work,
                    'orgname': institution,
                    'role': course_of_study,
                    'startdate': start_date,
                    'enddate': end_date,
                    'description': description,
                }
                return render(request, 'rafe_contrib/education.html', context)

        else:
            context = {
                'orgname_error': True,
                'title': 'Progenx | Work',
                'works': work,
                'orgname': institution,
                'role': course_of_study,
                'startdate': start_date,
                'enddate': end_date,
                'description': description,
            }
            return render(request, 'rafe_contrib/education.html', context)

    context = {
        'title': 'Progenx | Work',
        'works': work,
    }
    return render(request, 'rafe_contrib/education.html', context)

@login_required(login_url='/rafe/login')
def skill(request):
    skill = rafe_contrib_Skill.objects.filter(owner=request.user)
    if request.method == "POST":
        skill_name = request.POST['skill_title']
        proficiency = request.POST['proficiency']
        try:
            proficiency = int(proficiency)
            if proficiency > 100:
                proficiency = 100
        except:
            context = {
                'proficiency_error':True,
                'skill_title':skill_name,
                'proficiency_':proficiency,
                'title': 'Progenx | Skills',
                'skills': skill,
            }
            return render(request, 'rafe_contrib/skill.html', context)

        if skill_name != '':
            rafe_contrib_Skill.objects.create(
                owner=request.user,
                name=skill_name,
                proficiency=proficiency
            )
            context = {
                'success_msg':True,
                'msg':'click here to add work',
                'title': 'Progenx | Skills',
                'skills': skill,
            }
            return render(request, 'rafe_contrib/skill.html', context)
        else:
            context = {
                'name_error':True,
                'skill_title':skill_name,
                'proficiency_':proficiency,
                'title': 'Progenx | Skills',
                'skills': skill,
            }
            return render(request, 'rafe_contrib/skill.html', context)
    context = {
        'title': 'Progenx | Skills',
        'skills': skill,
    }
    return render(request, 'rafe_contrib/skill.html', context)


@login_required(login_url='/rafe/login')
def work(request):
    work = rafe_contrib_Work.objects.filter(owner=request.user)
    if request.method == "POST":
        org_name = request.POST['org_name']
        role = request.POST['role']
        start_date = request.POST['org_start_date']
        end_date = request.POST['org_end_date']
        description = request.POST['role_description']
        if end_date != '':
            try:
                end_date = int(end_date)
                if end_date > int(strftime('%Y')):
                    end_date = 'present'
            except:
                context = {
                    'end_date_not_int_err': True,
                    'title': 'Progenx | Work',
                    'works': work,
                    'orgname': org_name,
                    'role': role,
                    'startdate': start_date,
                    'enddate': end_date,
                    'description': description,
                }
                return render(request, 'rafe_contrib/work.html', context)
        else:
            end_date = 'present'
        try:
            start_date = int(start_date)
            if start_date > int(strftime('%Y')):
                start_date = int(strftime('%Y'))
        except:
            context = {
                'start_date_not_int_err': True,
                'title': 'Progenx | Work',
                'works': work,
                'orgname': org_name,
                'role': role,
                'startdate': start_date,
                'enddate': end_date,
                'description': description,
            }
            return render(request, 'rafe_contrib/work.html', context)

        if org_name != '':
            if start_date != '':
                if type(start_date) == int:
                    # *using 1941 since someone born 1941 would be like 80 years at the time of writing this code (2022)
                    if start_date > 1941:
                        rafe_contrib_Work.objects.create(
                            owner=request.user,
                            org_name=org_name,
                            title=role,
                            start=start_date,
                            stop=end_date,
                            description=description,
                        )
                        context = {
                            'success_msg': True,
                            'msg': 'to add educational background',
                            'title': 'Progenx | Work',
                            'works': work,
                        }
                        return render(request, 'rafe_contrib/work.html', context)
                    else:
                        context = {
                            'start_date_err': True,
                            'title': 'Progenx | Work',
                            'works': work,
                            'orgname': org_name,
                            'role': role,
                            'startdate': start_date,
                            'enddate': end_date,
                            'description': description,
                        }
                        return render(request, 'rafe_contrib/work.html', context)

            elif start_date == '':
                context = {
                    'start_date_err': True,
                    'title': 'Progenx | Work',
                    'works': work,
                    'orgname': org_name,
                    'role': role,
                    'startdate': start_date,
                    'enddate': end_date,
                    'description': description,
                }
                return render(request, 'rafe_contrib/work.html', context)
            else:
                context = {
                    'end_date_err': True,
                    'title': 'Progenx | Work',
                    'works': work,
                    'orgname': org_name,
                    'role': role,
                    'startdate': start_date,
                    'enddate': end_date,
                    'description': description,
                }
                return render(request, 'rafe_contrib/work.html', context)

        else:
            context = {
                'orgname_error': True,
                'title': 'Progenx | Work',
                'works': work,
                'orgname': org_name,
                'role': role,
                'startdate': start_date,
                'enddate': end_date,
                'description': description,
            }
            return render(request, 'rafe_contrib/work.html', context)

    context = {
        'title': 'Progenx | Work',
        'works': work,
    }
    return render(request, 'rafe_contrib/work.html', context)


def delete_work(request, pk):
    rafe_contrib_Work.objects.get(id=pk).delete()
    return redirect('rafe_contrib-work', permanent=True)


@login_required(login_url='/rafe/login')
def personal_c(request):
    user_details = User.objects.get(username=request.user)
    user_profile = rafe_contrib_Profile.objects.get(owner=request.user)
    if request.method == "POST":
        #TODO: LEARN HOW TO ADD SUFFIX TO DATABASE ITEMS
        if request.FILES.get('image') == None:
            image = user_profile.profile_img
            occupation = request.POST['occupation']
            address = request.POST['address']
            phone_number = request.POST['phone_number']
            twitter = request.POST['twitter_username']
            linkedin = request.POST['linkedin']
            about_me = request.POST['about_me']

            user_profile.profile_img = image
            user_profile.occupation = occupation
            user_profile.address = address
            user_profile.phone_number = phone_number
            if twitter != None:
                user_profile.twitter_link = twitter
            if linkedin != None:
                user_profile.linkedin_link = linkedin
            user_profile.about_me = about_me
            user_profile.save()
            return redirect('rafe_contrib-work')

        elif request.FILES.get('image') != None:
            image = request.FILES.get('image')
            occupation = request.POST['occupation']
            address = request.POST['address']
            phone_number = request.POST['phone_number']
            twitter = request.POST['twitter_username'].strip()
            linkedin = request.POST['linkedin'].strip()
            about_me = request.POST['about_me']

            user_profile.profile_img = image
            user_profile.occupation = occupation
            user_profile.address = address
            user_profile.phone_number = phone_number
            if twitter != None:
                user_profile.twitter_link = twitter
            if linkedin != None:
                user_profile.linkedin_link = linkedin
            user_profile.about_me = about_me
            user_profile.save()
            return redirect('rafe_contrib-work')

    context = {
        'user': user_details,
        'user_profile':user_profile,
        'title': 'Progenx | Personal & Contact',
    }
    return render(request, 'rafe_contrib/personal&c.html', context)
    


def delete_education(request, pk):
    rafe_contrib_Education.objects.get(id=pk).delete()
    return redirect('rafe_contrib-education', permanent=True)


def delete_skill(request, pk):
    rafe_contrib_Skill.objects.get(id=pk).delete()
    return redirect('rafe_contrib-skills', permanent=True)
