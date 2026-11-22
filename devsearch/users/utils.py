from django.db.models import Q
from .models import Skill, Profile
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def searchProfiles(request):
    search_query = ''
    
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
    
    skills = Skill.objects.filter(name__icontains=search_query)
    
    profiles = Profile.objects.distinct().filter(
        Q(name__icontains=search_query)|
        Q(short_intro__icontains=search_query)|
        Q(skill__in=skills)
        )
    return profiles, search_query


def paginateProfiles(request, profiles):
        #get the page number
        page =  request.GET.get('page')
        paginator = Paginator(profiles, 1)

        try:
            #Projects visible should be the ones on the page paginated
            profiles = paginator.page(page)
        except PageNotAnInteger:
            page = 1
            profiles = paginator.page(page)
        except EmptyPage:
            #let page be the last page.
            page = paginator.num_pages
            profiles = paginator.page(page)

        #custom range to prevent showing all the pagination page links
        left_index = (int(page)-4)
        if left_index < 1:
            left_index = 1

        right_index = (int(page)+5)
        if right_index > paginator.num_pages:
            right_index = paginator.num_pages + 1
    
        custom_range = range(left_index, right_index)

        return custom_range, profiles