from django import forms
from django.core import paginator
from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone
from django.http import HttpResponse
from .models import Post
from django.core.mail import mail_admins

from mysite.settings import EMAIL_HOST_USER

from django.core.mail import send_mail

from django.contrib import messages
from .forms import PostForm, DocumentForm, ContactForm, Subscribe, CommentForm
from django.core.paginator import Paginator, PageNotAnInteger

# def post_list(request):
#     posts = Post.objects.all()
#     return render(request, 'post_list.html', {'posts': posts})

def post_list(request):
    posts = Post.objects.all()
    paginator = Paginator(posts, 3)
    # print(paginator.num_pages)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
        # print(posts)
    except PageNotAnInteger:
        posts = paginator.page(1)
    return render(request, 'post_list.html', {'page':page, 'posts':posts})
# def post_list(request):
#     posts = Post.objects.all()
#     return render(request, 'post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.filter(active=True)
    new_comment = None
    
    # Comment posted
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            # Assign current post to the comment
            new_comment.post = post
            new_comment.save()
    
    else:
        comment_form = CommentForm()
    
    return render(request, 'post_detail.html', {'post':post, 'comments': comments, 'new_comment':new_comment, 'comment_form':comment_form })

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()    
            return redirect('post_list')
            
    else:
         form = PostForm()
    return render(request, 'post_new.html', {'form':form})
    

def home(request):
    return HttpResponse("Hey!!")

def index(request):
    return render(request, 'index.html', {})

def upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('post_list')
    else:
        form = DocumentForm()
    return render(request, 'form_upload.html', {'form': form})


def contact_us(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # send email code goes here
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = "New message"
            message = "{0} has sent you a new message:\n\n{1}" .format(name,form.cleaned_data['message'])
            mail_admins(subject,message)
            form.save()
            messages.add_message(request,messages.INFO,'Thank you for contacting us. We will be back to you in a moment!')
            return redirect('contact')
            #send_mail('New Enquiry', message, from_email, ['enquiry@exampleco.com'])
            #return HttpResponse('Thanks for contacting us!')
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})

def subscribe(request):
    sub = Subscribe()
    if request.method == 'POST':
        sub = Subscribe(request.POST)
        print("First", sub['Email'])
        subject = 'Welcome to Achiever\'s'
        message = 'Hope you are enjoying your Django Tutorials'
        recepient = str(sub['Email'].value())
        print("Second", recepient)
        send_mail(subject, message, EMAIL_HOST_USER, [recepient], fail_silently = False)
        return render(request, 'success.html', {'recepient': recepient})
    return render(request, 'email.html', {'form':sub})



# from mysite.settings import EMAIL_HOST_USER
# from django.core.mail import send_mail

# def subscribe(request):
#     sub = Subscribe()
#     if request.method == 'POST':
#         sub = Subscribe(request.POST)
#         print("First", sub['Email'])
#         subject = 'Welcome to Achiever\'s group'
#         message = 'You are viewing demo of gmail functionality'
#         recepient = str(sub['Email'].value())
#         print("Second", recepient)
#         send_mail(message, EMAIL_HOST_USER, [recepient], fail_silently=False)
#         return render(request, 'success.html', {'receipent': recepient})
#     return render(request, 'email.html', {'form':sub})
