from django.forms import ModelForm
from .models import Project, Tag, Review
from django import forms

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = '__all__'
        exclude = ['vote_total', 'vote_ratio', 'owner']
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class':'input'})
            
        # self.fields['title'].widget.attrs.update({
        #     'class': 'input', 'placeholder':'Add title',
        # })

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['value', 'body']
        labels = {
            'value': 'Place Your Vote',
            'body': 'Add a comment for your vote'
        }

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)
        
        for name, field in self.fields.items():
            field.widget.attrs.update({'class':'input'})
                    
            # self.fields['title'].widget.attrs.update({
            #     'class': 'input', 'placeholder':'Add title',
            # })