from django.db import models
import uuid
from django.contrib.auth.models import User
from users.models import Profile
# Create your models here.


class Project(models.Model):
    title = models.CharField(max_length=200)
    owner = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    featured_image = models.ImageField(null=True, blank=True, default="default.png")
    demo_link = models.CharField(null=True, blank=True, max_length=2000)
    source_link = models.CharField(null=True, blank=True, max_length=2000)
    tags = models.ManyToManyField("Tag", blank=True)
    vote_total = models.IntegerField(default=0, null=True, blank=True)
    vote_ratio = models.IntegerField(default=0, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    # editable is for when submitting forms
    id = models.UUIDField(
        default=uuid.uuid4, primary_key=True, unique=True, editable=False
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering=['-vote_ratio', '-vote_total', 'title']

    #making sure you can't vote on your own project. 
    @property
    def reviewers(self):
        #get a list of everyone that's voted
        queryset = self.review_set.all().values_list('owner__id', flat=True)
        return queryset

    @property
    def getVoteCount(self):
        reviews = self.review_set.all()
        upVotes = reviews.filter(value='up').count()
        totalVotes = reviews.count()
        ratio = (upVotes/totalVotes) * 100

        self.vote_total = totalVotes
        self.vote_ratio = ratio
        self.save()


class Review(models.Model):
    # creates a dropdown in our form for the user to pick.
    # Up is what's stored in the database and Up Vote is what's shown to the user in the form
    VOTE_TYPE = (("up", "Up Vote"), ("down", "Down Vote"))
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    body = models.TextField(null=True, blank=True)
    value = models.CharField(max_length=200, choices=VOTE_TYPE)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(
        primary_key=True, unique=True, editable=False, default=uuid.uuid4
    )

    class Meta:
        unique_together = [
        ['owner','project']
        ]
    def __str__(self):
        return self.value


class Tag(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )

    def __str__(self):
        return self.name
