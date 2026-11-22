from django.shortcuts import render,redirect
from .models import Project, Tag, Review
from .forms import ProjectForm, ReviewForm
from django.contrib.auth.decorators import login_required
from users.models import Profile
from .utils import searchProjects, paginateProjects
from django.contrib import messages
# Create your views here.


@login_required(login_url='login')
def create_project(request):
    form = ProjectForm()

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            profile = Profile.objects.get(user=request.user)
            project.owner = profile
            project.save()
            return redirect('projects')
    context = {'form': form}
    return render(request, 'projects/project_form.html', context)

def projects(request):
    projects, search_query = searchProjects(request)
    custom_range, projects = paginateProjects(request, projects)
    context = {'projects': projects,
               'search_query': search_query,
               'custom_range': custom_range}
    
    return render(request, 'projects/projects.html', context)

def project(request, pk):
    projectObj = Project.objects.get(id=pk)
    form = ReviewForm()
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.project = projectObj
            review.owner = request.user.profile
            review.save()
            projectObj.getVoteCount
            messages.success(request, 'Your review was successfully submitted')

            return redirect('project', pk=projectObj.id)
    # tags = projectObj.tags.all()
    context = {'projects':projectObj,
               'form':form}
    return render(request, 'projects/single-project.html', context)

@login_required(login_url='login')
def update_project(request, pk):
    #making sure the only way to edit a project is if you are signed in
    profile = request.user.profile
    projectObj = profile.project_set.get(id=pk)
    form = ProjectForm(instance=projectObj)

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=projectObj)
        if form.is_valid():
            form.save()
            return redirect('projects')
    context = {'form': form}
    return render(request, 'projects/project_form.html', context)

@login_required(login_url='login')
def delete_project(request, pk):
    #also ensuring only the owner of a project can delete it.
    profile =  request.user.profile
    projectObj = profile.project_set.get(id=pk)
    if request.method == 'POST':
        projectObj.delete()
        return redirect("account")
    context = {
        'project': projectObj
    }
    return render(request, 'projects/delete_objects.html', context)
