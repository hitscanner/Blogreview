from django.shortcuts import render, redirect
from .models import Blog, Comment
from django.db.models import Q

# Create your views here.

def index(request):
    posts = Blog.objects.all()
    context={ 
        "posts":posts,  
        }
    return render(request,"index.html",context)




def read(request,post_id):
    post = Blog.objects.get(id=post_id)
    comment = Comment.objects.filter(post=post.id) 
    context = {
        "post":post,
        "comment":comment,
    }
    return render(request,'read.html',context)

def create(request): 
    if request.method == "GET":
        return render(request,'create.html')
    elif request.method == "POST":
        post = Blog()
        post.user = request.user
        post.title = request.POST['title']
        post.content = request.POST['content']        
        post.save()
        return redirect(index)

def update(request,post_id):
    if request.method == "GET": #GET은 하나만 골라서 가져옴
        post = Blog.objects.get(id = post_id)
        context = {
            "post":post,
        }
        return render(request,'update.html',context)
    elif request.method == "POST":
        post = Blog.objects.get(id = post_id)
        post.title = request.POST['title']
        post.content = request.POST['content'] 
        post.save()
        return redirect(index)

def delete(request,post_id):
    post = Blog.objects.get(id = post_id)
    post.delete()
    return redirect(index)

def c_create(request,post_id):
    if request.method == "POST":
        comment = Comment() 
        comment.user = request.user 
        comment.post = Blog.objects.get(id=post_id) 
        comment.content = request.POST['comment']
        anonymous = request.POST.get('anonymous',False)  
        if anonymous == "1":
            comment.anonymous = True
        comment.save() 
        return redirect(read,comment.post.id)