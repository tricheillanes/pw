from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from .forms import PostForm
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone


# Create your views here.

def post_create(request):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404

	form = PostForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.user = request.user
		instance.save() 
		messages.success(request, "Creado Bien")
		return redirect("posts:list")
	#if request.method == "POST":
	#	print request.POST.get("content") #Esto es cuando creas un post que salga en el terminal la informacion
	#	print request.POST.get("title")
		#Post.objects.create("title"=title)
	context = {
		"form": form,
	}
	return render(request, "post_form.html", context)

def post_detail(request, id=None):
	instance = get_object_or_404(Post, id=id)
	if instance.publish > timezone.now().date() or instance.draft:
		if not request.user.is_staff or not request.user.is_superuser:
			raise Http404

	context = {
		"title": instance.title,
		"instance": instance,
	}
	return render(request, "post_detail.html", context)
	#return HttpResponse("<h1>DEETAIL</h1>")
  
def post_list(request):
	today = timezone.now().date()
	queryset_list = Post.objects.active()
	if request.user.is_staff or request.user.is_superuser:
		queryset_list = Post.objects.all()

	query = request.GET.get("q")
	if query:
		queryset_list = queryset_list.filter(
				Q(title__icontains=query)|
				Q(content__icontains=query)|
				Q(user__first_name__icontains=query) | 
				Q(user__last_name__icontains=query)
				).distinct()


	paginator = Paginator(queryset_list, 20) # Show 25 contacts per page
	page_request_var = "page"
	page = request.GET.get(page_request_var)
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		queryset = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		queryset = paginator.page(paginator.num_pages)

	#if request.user.is_authenticated():
	context = {
		"objects_list": queryset,
		"title": "El mundo de las plantas",
		"page_request_var": page_request_var,
		"today": today,
	}

	return render(request, "post_list.html", context)
	#return HttpResponse("<h1>LISST ITEM</h1>")


def post_update(request, id=None):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	instance = get_object_or_404(Post, id=id)
	form = PostForm(request.POST or None, request.FILES or None, instance=instance)
	# or None sirve para que no nos salga todo el rato lo de NECESITA INTRODUCIR EL CAMPO
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		messages.success(request, "Modificado Bien")
		return redirect('/' + 'posts' + '/' + id + '/')

	context = {
		"title": instance.title,
		"instance": instance,
		"form": form,
	}
	return render(request, "post_form.html", context)

def post_delete(request, id=None):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	instance = get_object_or_404(Post, id=id)
	instance.delete()
	messages.success(request, "Bien Eliminado")
	return redirect("posts:list")

