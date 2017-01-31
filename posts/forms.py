from django import forms
from .models import Post

class PostForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = [
			"title",
			"content",
			"image",
			"draft",
			"publish",  #Lo que hay que rellenar para crear un post
		]