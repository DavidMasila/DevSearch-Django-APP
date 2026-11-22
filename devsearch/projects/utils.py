from django.db.models import Q
from .models import Project, Tag, Review
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def searchProjects(request):
    search_query = ''

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    tags = Tag.objects.filter(name__icontains=search_query)

    projects = Project.objects.distinct().filter(
        Q(title__icontains=search_query)|
        Q(description__icontains=search_query)|
        Q(owner__name__icontains=search_query)|
        Q(tags__in=tags)
    )
    return projects, search_query

def paginateProjects(request, projects):
        #get the page number
        page =  request.GET.get('page')
        paginator = Paginator(projects, 3)

        try:
            #Projects visible should be the ones on the page paginated
            projects = paginator.page(page)
        except PageNotAnInteger:
            page = 1
            projects = paginator.page(page)
        except EmptyPage:
            #let page be the last page.
            page = paginator.num_pages
            projects = paginator.page(page)

        #custom range to prevent showing all the pagination page links
        left_index = (int(page)-4)
        if left_index < 1:
            left_index = 1

        right_index = (int(page)+5)
        if right_index > paginator.num_pages:
            right_index = paginator.num_pages + 1
    
        custom_range = range(left_index, right_index)

        return custom_range, projects