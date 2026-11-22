from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Profile, Skill, Message
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import CustomUserCreationForm, ProfileForm, SkillForm, MessageForm
from django.contrib import messages
from django.db.models import Q
from .utils import searchProfiles, paginateProfiles
# Create your views here.


def loginUser(request):

    page = 'login'
    context = {'page':page}
    #if the user is authenticated redirect to profiles so that dont access login page
    if request.user.is_authenticated:
        return redirect('profiles')
    
    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']

        #check whether user exists in the database
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "Username does not exist")

        #here we already know the user exists. Because of the try and except above
        #authenticate verifies a user's credentials to determine if valid
        #the authenticate either return the user if creds are valid or None if the creds are invalid
        user = authenticate(request, username=username, password=password)
        #here if the user creds are valid and the user exists, then create a session cookie for them.
        if user is not None:
            #the login function creates a session for the user and adds that to the browser's cookies
            login(request, user)
            return redirect(request.GET['next'] if 'next' in request.GET else 'account')
        else:
            messages.error(request, "Username  or Password is incorrect")
        
    return render(request, 'users/login_register.html', context)

def logoutUser(request):
    logout(request)
    messages.success(request, "Successfully logged out!")
    return redirect('login')


def registerUser(request):
    form = CustomUserCreationForm()
    page = 'register'

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            #here we hold the user before processing it.
            user = form.save(commit=False)
            #say maybe make things lowercase
            user.username = user.username.lower()
            user.save()
            messages.success(request, f"{user.username.capitalize()}'s account created successfully")

            #login the user. Create a session for them in the cookies
            login(request, user)
            return redirect('edit-account')
        else:
            messages.error(request, "Error occured during registration")

    context = {'page': page, 'form': form}
    return render(request, 'users/login_register.html', context)

def profiles(request):
    profiles, search_query = searchProfiles(request)
    custom_range, profiles = paginateProfiles(request, profiles)
    context = {'profiles':profiles,
               'search_query': search_query,
               'custom_range': custom_range}
    
    return render(request, 'users/profiles.html', context)

def userProfile(request, pk):
    profile = Profile.objects.get(id=pk)
    topSkills = profile.skill_set.exclude(description__exact="")
    otherskills = profile.skill_set.filter(description="")
    context = {
        'profile':profile,
        'topSkills': topSkills,
        'otherSkills':otherskills,
    }
    return render(request, 'users/user-profile.html', context)

@login_required(login_url='login')
def userAccount(request):
    profile = request.user.profile
    topSkills = profile.skill_set.exclude(description__exact="")
    otherskills = profile.skill_set.filter(description="")
    context = {
        'profile':profile,
        'topSkills': topSkills,
        'otherSkills':otherskills,
    }
    return render(request, 'users/account.html', context)

@login_required(login_url='login')
def editAccount(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, f"profile updated successfully")
            return redirect('account')
    context = {
        'form': form,
    }
    return render(request, 'users/profile_form.html', context)

@login_required(login_url='login')
def createSkill(request):
    form = SkillForm()
    profile = request.user.profile

    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request, f"{skill.name} skill added successfully")
            return redirect('account')
    context = {
        'form': form,
    }
    return render(request, 'users/skill_form.html', context)

@login_required(login_url='login')
def editSkill(request, pk):
    skillObj = request.user.profile.skill_set.get(id=pk)
    form = SkillForm(instance=skillObj)
    
    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skillObj)
        if form.is_valid():
            form.save()
            messages.success(request, f"{skillObj} updated successfully")
            return redirect('account')
    context = {
        'form':form,
    }
    return render(request, 'users/skill_form.html', context)

@login_required(login_url='login')
def deleteSkill(request, pk):
    skillDel = request.user.profile.skill_set.get(id=pk)
    context = {
        'skill':skillDel
    }
    if request.method == 'POST':
        skillDel.delete()
        messages.success(request, f"{skillDel} deleted successfully")
        return redirect('account')
    return render(request, 'users/delete_skill.html', context)

@login_required(login_url='login')
def inbox(request):
    profile =request.user.profile
    messageRequests = profile.messages.all() #here we are getting the recipients name
    unreadCount = messageRequests.filter(is_read=False).count()
    context = {
        'messageRequests': messageRequests,
        'unreadCount': unreadCount,
    }
    return render(request, 'users/inbox.html', context)

@login_required(login_url='login')
def viewMessage(request, pk):
    #ensures we are getting data only the individual signed in.
    #one cannot get the data unless they are the ones signed in
    profile = request.user.profile
    message = profile.messages.get(id=pk)
    if message.is_read == False:
        message.is_read=True
        message.save()
    context = {
        'message': message,
    }
    return render(request, 'users/message.html', context)

def createMessage(request, pk):
    form = MessageForm()
    recipient = Profile.objects.get(id=pk)

    try:
        sender = request.user.profile

    except:
        sender = None

    if request.method == 'POST':
        form  = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient

            if sender:
                message.name = sender.name
                message.email = sender.email

            message.save()
            messages.success(request, 'Your message was successfully sent')
            return redirect('user-profile', pk=recipient.id)
    context = {
        'form': form,
        'recipient': recipient
    }
    return render(request, 'users/message_form.html', context)