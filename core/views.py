from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import *
from django.template.loader import render_to_string, get_template
from django.core.mail import EmailMessage


"""
Hello there, I'm leaving this message here for anyone who'll be working on this in the future.
If happen to face any bugs while working, then do the following:
1. If it works, don't touch it
2. Check for missing commas and colons
3. Save the updated code and run it again
4. Use dashes ("-") to separate multiple words in urls.py file.
5. Go get some boob milk too(this one helps me alot).
"""

#----------------------- Unauthenticated Views Start ------------------#
def index(request):
    context = {
        'title' : 'Progenex | Index',
    }
    return render(request, 'index.html', context)

def login(request):
    context = {
        'title' : 'Progenex | Login',
    }
    if request.method == 'POST':
        username = request.POST['username'] #Requesting Username
        password = request.POST['password'] #Requesting Password
    
        user = auth.authenticate(username=username, password=password)

        if user is not None: #Cheking If User Exists in the database
            auth.login(request, user) # Logs in User
            return redirect('home') # Redirects to home view
            print(request.user)
        else:
            messages.info(request, 'Invalid Username or Password') #Conditional Checking if credentials are correct
            return redirect('login')#Redirects to login if invalid

    else:
        return render(request, 'login.html', context)

def register(request):
    context = {
        'title' : 'Progenex | Register',
    }
    if request.method == 'POST':
        #Requesting POST data
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        #End of POST data request

        #Condition is executed if both passwords are the same
        if password == password2:
            if User.objects.filter(email=email).exists(): #Checking databse for existing data
                messages.info(request, "This email is already in use")#Returns Error Message
                return redirect(register)
            elif User.objects.filter(username=username).exists():
                messages.info(request, "Username Taken")
                return redirect('register')
            #Else condition executed if the above conditions are not fulfilled    
            else:
                ctx = {
                    'user' : username
                }
                message = get_template('mail.html').render(ctx)
                msg = EmailMessage(
                    'Welcome to Progenex',
                    message,
                    'Tobi from Progenex by Genxsis',
                    [email],
                )
                msg.content_subtype ="html"# Main content is now text/html
                msg.send()
                user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name )
                user.save()
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)#Logs in USER



            #Create user model and redirect to edit-profile
            user_model = User.objects.get(username=username)
            new_profile = Profile.objects.create(owner=user_model, user_id=user_model.id)
            new_profile.save()
            return redirect('p-and-c')#Rediects to specified page once condition is met
        else:
            messages.info(request, "Passwords do not match")
            return redirect(register)

    else:
        return render(request, 'register.html', context)

#----------------------- Unauthenticated Views End ------------------#

#---------------------------------------------

#------------------------ Authenticated Views Start --------------------#
@login_required
def home(request):
    context = {
        'title' : 'Progenex | Home',
    }
    return render(request, 'home.html', context)

@login_required
def delete_work(request, pk=None):
    Work.objects.get(id=pk).delete()
    return redirect("work")

@login_required
def delete_skill(request, pk=None):
    Skill.objects.get(id=pk).delete()
    return redirect("skills")


@login_required
def achievements(request):
    achievements = Achievements.objects.filter(owner=request.user)
    if request.method == "POST":
        title = request.POST['title']
        description = request.POST['description']
        Achievements.objects.create(owner=request.user, title=title, description=description)
        messages.success(request,'Achievement added successfully')
    context ={
        'achievements' : achievements
    }
    return render(request, 'achievements.html', context)

@login_required
def del_ach(reqeust, pk=None):
    Achievements.objects.get(id=pk).delete()
    return redirect('achievements')

@login_required
def work(request):
    work = Work.objects.all()
    if request.method == "POST":
        org_name = request.POST['org_name']
        title = request.POST['role']
        start = request.POST['from']
        stop = request.POST['to']
        description = request.POST['desc']

        Work.objects.create(owner=request.user, title=title, org_name=org_name, start=start, stop=stop, description=description)
        messages.success(request, "Work History has been added")
        

    context = {
        'title' : 'Progenex | Work',
        'work' : work
    }
    return render(request, 'work.html', context)



@login_required
def delete_education(request, pk=None):
    Education.objects.get(id=pk).delete()
    return redirect("education")


@login_required
def education(request):
    education = Education.objects.filter(owner=request.user)
    if request.method == "POST":
        institution = request.POST['int_name']
        course = request.POST['course']
        degree = request.POST['degree']
        start = request.POST['start']
        stop = request.POST['stop']
        description = request.POST['description']
        Education.objects.create(owner=request.user, institution=institution, degree=degree, start=start, stop=stop, description=description, course_of_study=course)
        messages.success(request, 'Education background added successfully')
    context = {
        'title' : 'Progenex | Education',
        'education' : education
    }
    return render(request, 'education.html', context)

@login_required
def skills(request):
    skills = Skill.objects.filter(owner=request.user)
    if request.method == "POST":
        name = request.POST['skill']
        proficiency = request.POST['proficiency']

        Skill.objects.create(owner=request.user, name=name, proficiency=proficiency)
        messages.success(request, 'Skill added successfully')
    
    context = {
        'title' : 'Progenex | Skills',
        'skills' : skills
    }
    return render(request, 'skills.html', context)

@login_required
def p_and_c(request):
    user_profile = Profile.objects.get(owner=request.user)
    if request.method == "POST":
        if request.FILES.get('image') == None:
            image = user_profile.profile_img
            address = request.POST['address']
            phone_number = request.POST['phone']
            twitter_username = request.POST['twitter']
            linkedin_link = request.POST['linkedin']
            about_me = request.POST['desc']
            occupation = request.POST['occupation']

            user_profile.profile_img = image
            user_profile.address = address
            user_profile.occupation = occupation
            user_profile.phone_number = phone_number
            user_profile.twitter_username = twitter_username
            user_profile.linkedin_link = linkedin_link
            user_profile.about_me = about_me
            user_profile.save()
            return redirect("work")


        elif request.FILES.get('image') != None:
            image = request.FILES.get('image')
            address = request.POST['address']
            phone_number = request.POST['phone']
            twitter_username = request.POST['twitter']
            linkedin_link = request.POST['linkedin']
            about_me = request.POST['desc']
            occupation = request.POST['occupation']

            user_profile.profile_img = image
            user_profile.address = address
            user_profile.occupation = occupation
            user_profile.phone_number = phone_number
            user_profile.twitter_username = twitter_username
            user_profile.linkedin_link = linkedin_link
            user_profile.about_me = about_me
            user_profile.save()
            return redirect("work")
    context = {
        'title' : 'Progenex | Personal and Contact information',
        'user_profile' : user_profile,
    }
    return render(request, 'p&c.html', context)

@login_required
def logout(request):
    auth.logout(request)
    return redirect('login')


def resume(request, pk):
    user_object= User.objects.get(username=pk)
    user_profile = Profile.objects.get(owner=user_object)
    work = Work.objects.filter(owner=user_object).order_by("-id")
    skills = Skill.objects.filter(owner=user_object).order_by("-id")
    education = Education.objects.filter(owner=user_object).order_by("-id")
    achievements = Achievements.objects.filter(owner=user_object).order_by("-id")

    context = {
        'user_profile' : user_profile,
        'work' : work,
        'skills' : skills,
        'education' : education,
        'achievements' : achievements

    }
    return render(request, 'resume.html', context)
#------------------------ Authenticated Views End --------------------#


# Create your views here.
