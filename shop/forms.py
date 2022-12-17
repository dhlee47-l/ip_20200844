from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)
        widgets = {
            "content": forms.Textarea(attrs={
                'placeholder': '댓글을 작성해주세요',
                'class': 'form-control', 'rows': '3'
            })
        }


