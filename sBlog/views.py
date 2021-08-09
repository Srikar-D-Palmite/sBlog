from django.shortcuts import redirect, render
from django.http import HttpResponse
from sBlog.models import Users, Posts, Comments
from django.http import HttpResponseRedirect
# from django.contrib import messages, auth
# from django.contrib.auth.decorators import login_required
from django.db.models import Q

# create a row:
# user = Users(username=request.POST['username'], password=request.POST['password'])
# user.save()

# access a row:
# Users.objects.all()
# Users.objects.filter()
# Users.objects.exclude()
# Users.objects.get() [for a single row]


# Views:
def index(request):
    # get last 20 posts
    latest_posts = Posts.objects.all().order_by('-id')[:20]
    return render(request, 'index.html', {
        'latest_posts': latest_posts
        })

def logged_in(request):
    # User must be logged in to access this view
    if 'user_id' not in request.session:
        return HttpResponseRedirect("/")
    # Return homepage but with a alert that they are logged in
    latest_posts = Posts.objects.all().order_by('-id')[:20]
    return render(request, 'index.html', {
        'latest_posts': latest_posts,
        'logged_in': True
        })

def register(request):
    # Take to register page
    if request.method == 'GET':
        return render(request, 'register.html')
    # Register user in Users table
    elif request.method == 'POST':
        # Passwords do not match
        if request.POST["password"] != request.POST["confirm password"]:
            return render(request, 'register.html', {
                'error': 'Passwords do not match'
            })
        # Username must be unique
        if request.POST['username'] in Users.objects.all():
            return render(request, '/register', {
                'error': 'username is taken'
                })
        # Add row to db
        new_user = Users(username=request.POST['username'], password=request.POST['password'])
        new_user.save()
        return HttpResponseRedirect("/login")
    else:
        return HttpResponse("Error")

def login(request):
    # Take user to login page
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        # try to find username in table
        try:
            logging_user = Users.objects.get(username=request.POST['username'])
        except:
        # login fail cases
            return render(request, 'login.html', {
                'error': 'Username does not exist'
            })
        if logging_user.password != request.POST['password']:
            return render(request, 'login.html', {
                'error': 'Passwords do not match'
            })
        # Add user to session (log in)
        request.session['user_id'] = logging_user.id
        return HttpResponseRedirect("/login_success", {'success': True})

def logout(request):
    if not 'user_id' in request.session:
        return HttpResponseRedirect("/")
    # remove user from session 
    # ~= auth.logout(request)
    del request.session['user_id']
    latest_posts = Posts.objects.all().order_by('-id')[:10]
    return render(request, 'index.html', {
        'logout': True,
        'latest_posts': latest_posts
    })

def post(request):
    # check if user is logged in
    if "user_id" not in request.session:
        return HttpResponseRedirect("/login")
    if request.method == 'POST':
        # Save post in Posts table in db
        user_new_post = Posts(title=request.POST['title'], content=request.POST['content'], 
                              poster=Users.objects.get(id = request.session['user_id']))
        user_new_post.save()
        # Take User to their history page
        user_posts = Posts.objects.filter(poster=Users.objects.get(id=request.session['user_id'])).order_by('-id')
        return render(request, 'history.html', {
            'posted': True, 'user_posts': user_posts
            })
    # send user to new post page
    else:
        return render(request, 'new_post.html')

def view_post(request, post_id):
    try:
        post = Posts.objects.get(id=post_id)
        comments = Comments.objects.filter(post=post)
        owner = False
        # if logged in
        if "user_id" in request.session:
            # Page if user is creator of the post
            if post.poster == Users.objects.get(id=request.session["user_id"]):
                owner = True
        return render(request, 'view_post.html', {
            'post': post,
            'comments': comments,
            "owner": owner
            })
    except:
        return render(request, 'pagenotfound.html', {'error_message': 'Post not found'})

def post_history(request):
    # Check if user is logged in
    if "user_id" not in request.session:
        return HttpResponseRedirect("/login")
    # Take User to their history page
    user_posts = Posts.objects.filter(poster=Users.objects.get(id=request.session['user_id'])).order_by('-id')
    return render(request, 'history.html', {'user_posts': user_posts})

def comment(request, post_id):
    # ensure user is logged in
    if "user_id" not in request.session:
        return HttpResponseRedirect("/login")
    if request.method == 'POST':
        # Save comment
        comment = Comments(comment_title=request.POST['title'], comment_text=request.POST['content'], 
                           post=Posts.objects.get(id=post_id), 
                           commenter=Users.objects.get(id=request.session['user_id']))
        comment.save()
        return HttpResponseRedirect(f"/comment_success/{post_id}")
    # take user to comments page
    else:
        post = Posts.objects.get(id=post_id)
        return render(request, 'comment.html', {
            'post': post
            })

def comment_success(request, post_id):
    # ensure user is logged in
    if "user_id" not in request.session:
        return HttpResponseRedirect("/login")
    try:
        # Show the view page of the post they commented on with success alert
        post = Posts.objects.get(id=post_id)
        comments = Comments.objects.filter(post=post)
        return render(request, 'view_post.html', {
            'post': post,
            'commented': True,
            'comments': comments
            })
    except:
        return render(request, 'pagenotfound.html', {'error_message': 'Post not found'})

def edit_post(request, post_id):
    # ensure user is logged in
    if "user_id" not in request.session:
        return HttpResponseRedirect("/login")
    # Validate poster is editing
    post = Posts.objects.get(id=post_id)
    if post.poster != Users.objects.get(id=request.session["user_id"]):
        return HttpResponseRedirect(f'/view/{post_id}')
    if request.method == 'POST':
        # Save post after edit
        edited_post = Posts.objects.get(id=post_id)
        edited_post.content=request.POST['content']
        edited_post.save()
        return HttpResponseRedirect(f'/view/{post_id}')
    else:
        return render(request, 'edit_post.html', {
            'post': post
            })

def about(request):
    return render(request, 'about.html')

def delete_post(request, post_id):
    # ensure user is logged in
    if "user_id" not in request.session:
        return HttpResponseRedirect("/login")

    post = Posts.objects.get(id=post_id)
    # ensure post is being deleted by poster
    if post.poster != Users.objects.get(id=request.session["user_id"]):
        return HttpResponseRedirect(f'/view/{post_id}')
    if request.method == "GET":
        return render(request, 'confirm_delete.html', {
            'post': post
            })
    else:
        # delete the post from Posts table
        post = Posts.objects.get(id=post_id)
        post.delete()
        return HttpResponseRedirect("/history", {"deleted": True})

def search(request):
    if request.method == "GET":
        return render(request, 'search_page.html')
    query = request.POST['query']
    search_in = request.POST['search_in']
    # find search matches in title and content, or usernames
    if search_in == 'title_content':
        matches = Posts.objects.filter(Q(content__icontains=query) | Q(title__icontains=query))
    else:
        user_matches = Users.objects.filter(Q(username__icontains=query)) # poster.username
        matches = []
        for user in user_matches:
            matches += Posts.objects.filter(poster=user)
    
    return render(request, 'search_res.html', {'matches': matches})
