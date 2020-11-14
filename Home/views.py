from .forms import CommentForm, InterestsForm, PostCodeForm, PostsForm, RegisterForm, TownForm, YearGroupForm
# this imports all of the relevant forms i need for the project
from .models import Comment, Interests, PostCode, Town, UserInformation, YearGroup, Friend
# this imports all of the models i am using for the project
from .models import Posts as Post_model
# this imports the Posts model as Post_model as i have made a funciton called post with the same identifier
from django.contrib.auth.models import User
# this imports the user model which is a predefined model created by django to handle logins to the system
from django.http import HttpResponseRedirect, HttpResponse
# this imports HttpResponseRedirect to redirect the user to a specific url
from django.shortcuts import get_object_or_404, render, redirect
'''
this imports get_object_or_404, render and redirect. get_object_or_404 will get an object from the database
or display an error page. render will render a specific page with any contextual values like a form
'''
from django.db.models import Q
'''
this imports q from a predefined django model to query the database from a form filled on a html page.
this will  allow me to filter queries with keyword arguements specified by the user.
'''
import git
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def update(request):
    if request.method == "POST":
        repo = git.Repo("/home/k5924/Galaxy-Online")
        origin = repo.remotes.origin
        origin.pull()
        return HttpResponse("Updated code on PythonAnywhere")
    else:
        return HttpResponse("Couldn't update code on PythonAnywhere")


def Index(request):
    # function labeled index which takes parameter request
    return render(request, 'Home/index.html')
    # returns by rendering the request as the index.html


def SignUp(request):
    # function labeled SignUp which takes parameter request
    if request.method == 'POST':
        # if the request method is post
        form = RegisterForm(request.POST)
        # the registration form is called with parameter of request.post
        # this will load the registration form with the data filled in the form
        if form.is_valid():
            # if the form is valid
            form.save()
            # save the form
            return HttpResponseRedirect('Login')
            # return to the login page
    else:
        # if the form isnt valid
        form = RegisterForm()
        # display another blank registration form
    context = {
        'form': form,
    }
    # the context that will be displayed on the page is form
    return render(request, 'Home/SignUp.html', context)
    # returns by rendering the request as the SignUp.html with the relevant form


def Profile(request, pk=None):
    # function labeled Profile which takes parameters request and pk which is None
    if pk:
        # if a pk is supplied
        user = User.objects.get(pk=pk)
        # get the users data for their profile
    else:
        user = request.user
        # display the logged users profile
    context = {'user': user}
    # take user as a parameter in context
    return render(request, 'Home/Profile.html', context)
    # returns by rendering the request as the Profile.html with the relevant user data


def EditProfile(request):
    # function labeled EditProfile which takes parameter request
    if request.method == 'POST':
        # if form is displayed
        form1 = YearGroupForm(request.POST, instance=request.user.userinformation.year)
        form2 = InterestsForm(request.POST, instance=request.user.userinformation.interest)
        form3 = PostCodeForm(request.POST, instance=request.user.userinformation.postcode)
        form4 = TownForm(request.POST, instance=request.user.userinformation.town)
        # initialise values for each form as an instance in relation to the user
        if form1.is_valid() and form2.is_valid() and form3.is_valid() and form4.is_valid():
            # if all the forms are valid
            data1 = request.user  # get the current users data
            data2 = form1.cleaned_data['year']
            data3 = form2.cleaned_data['interest']
            data4 = form3.cleaned_data['postcode']
            data5 = form4.cleaned_data['town']
            # store the cleaned data returned from the forms
            year = YearGroup.objects.get(year=data2)
            interest = Interests.objects.get(interest=data3)
            postcode = PostCode.objects.get(postcode=data4.upper())
            town = Town.objects.get(town=data5.lower())
            # get the primary key of the object in their database tables
            user = UserInformation.objects.get(user=data1)
            # get the users object from the database table for UserInformation
            user.year = year
            user.interest = interest
            user.postcode = postcode
            user.town = town
            user.save()
            # save the primary keys of objects returned as the foreign keys in the UserInformation table
            # for that user
            return HttpResponseRedirect('../Profile')
            # redirect the user back to the profile page
    else:
        form1 = YearGroupForm(instance=request.user.userinformation.year)
        form2 = InterestsForm(instance=request.user.userinformation.interest)
        form3 = PostCodeForm(instance=request.user.userinformation.postcode)
        form4 = TownForm(instance=request.user.userinformation.town)
        # if there was an error in the form display errors and a blank form
    context = {
        'form1': form1,
        'form2': form2,
        'form3': form3,
        'form4': form4
    }  # store data to be used in the html template
    return render(request, 'Home/Edit Profile.html', context)
    # returns by rendering the request as the Edit Profile.html with the relevant forms


def Friends(request):
    # create function labeled Friends with parameter request
    try:
        friend = Friend.objects.get(current_user=request.user)
        friends = friend.users.all()
        # try to get the current users friends list
    except Friend.DoesNotExist:
        friends = None
        # unless the current user has no friends
    context = {
        'friends': friends
    }  # store the friends in a context variable to use on the template
    return render(request, 'Home/Friends.html', context)
    # render the template Friends.html with the friends list of the user


def AddFriend(request):
    # create function labeled AddFriend with parameter request
    user = request.user
    # store current user as user
    try:
        friend = Friend.objects.get(current_user=request.user)
        friends = friend.users.all()
        # try to get the current users friends list
    except Friend.DoesNotExist:
        friends = None
        # unless the current user has no friends
    superuser = User.objects.get(username="admin")  # store superuser as admin
    yearlist = UserInformation.objects.filter(year=user.userinformation.year).exclude(user=user)
    yearlist = yearlist.exclude(user=superuser)
    interestlist = UserInformation.objects.filter(interest=user.userinformation.interest).exclude(user=user)
    interestlist = interestlist.exclude(user=superuser)
    postcodelist = UserInformation.objects.filter(postcode=user.userinformation.postcode).exclude(user=user)
    postcodelist = postcodelist.exclude(user=superuser)
    townlist = UserInformation.objects.filter(town=user.userinformation.town).exclude(user=user)
    townlist = townlist.exclude(user=superuser)
    # exclude admin and current user from all friends lists that will be displayed
    context = {
        'yearlist': yearlist,
        'interestlist': interestlist,
        'postcodelist': postcodelist,
        'townlist': townlist,
        'friends': friends
    }  # pass friends lists as context variables in template
    return render(request, 'Home/AddFriends.html', context)
    # render template AddFriends.html with each friends list


def ChangeFriendStatus(request, operation, pk):
    # create function labeled ChangeFriendStatus with parameters request, operation and pk
    new_friend = User.objects.get(pk=pk)
    # store the passed primary key as new_friend variable
    if operation == "add":
        # if the operaiton is add
        Friend.make_friend(request.user, new_friend)
        # make a friend relationsihp between the logged in user and new_friend
    elif operation == "remove":
        # if the operation is remove
        Friend.lose_friend(request.user, new_friend)
        # remove the friend relationship between the logged in user and new_friend
    return redirect('Friends')
    # redirect to the Friends url


def Posts(request):
    # creates function labeled Posts with parameter request
    post = Post_model.objects.filter(user=request.user).order_by('-publish')
    # orders the users posts by most recently created
    others = Post_model.objects.all().exclude(user=request.user).order_by('-publish')
    # orders other users posts by most recently created
    content = {
        'post': post,
        'others': others
    }  # store users posts as variables to be used in the template
    return render(request, 'Home/Posts.html', content)
    # render Posts.html with the associated users posts


def CreatePost(request):
    # function labeled CreatePost taking parameter request
    if request.method == 'POST':
        # if the request has been made
        form = PostsForm(request.POST or None, request.FILES or None)
        # create an instance of the posts form to be viewed
        if form.is_valid():
            # if the form is valid
            post = form.save(commit=False)
            # get the post to edit a field in the Post table before its saved
            post.user = request.user
            # assign the user to the post
            post.save()
            # save the post
            return HttpResponseRedirect('../Posts')
            # redirect to the Posts page
    else:
        form = PostsForm()
        # if the post isnt valid show field errors and a blank form
    context = {
        'form': form
    }  # store form in context to be used in template
    return render(request, 'Home/Create Post.html', context)
    # render Create Post.html with the associated form


def PostDetail(request, pk):
    # create function labeled PostDetail with parameters request and pk
    post = get_object_or_404(Post_model, pk=pk)
    # get the object from the Post_model with that primary key and stpre it as post
    comments = Comment.objects.filter(post=post).order_by('-id')
    # get comments for post and order comments by id of user
    is_liked = False
    # store boolean
    comment_form = CommentForm()
    # get CommentForm
    if post.likes.filter(id=request.user.id).exists():
        # filter the posts likes field to see if user has liked post
        is_liked = True
        # update boolean
    elif request.method == 'POST':
        # if the request is post
        comment_form = CommentForm(request.POST or None)
        # get CommentForm to be displayed
        if comment_form.is_valid():
            # if the form is valid
            content = request.POST.get('content')
            # get the content in the form
            comment = Comment.objects.create(post=post, user=request.user, content=content)
            # create a object in the comments table assigniing the post, user and content in the object
            comment.save()
            # save the comment in the table
            return HttpResponseRedirect(post.get_absolute_url())
            # refresh the page with the new comment
    context = {
        'post': post,
        'is_liked': is_liked,
        'total_likes': post.total_likes(),
        'comments': comments,
        'form': comment_form,
    }  # stores post, is_likes, post.total_likes, comments and comment_form to be used in the template
    return render(request, 'Home/post_detail.html', context)
    # render the post_detail page with the contextual variables


def LikePost(request):
    # creates function labeled LikePost with parameter request
    post = get_object_or_404(Post_model, id=request.POST.get('post_id'))
    # get post that is being liked by the user
    is_liked = False
    # is_liked is initially false
    if post.likes.filter(id=request.user.id).exists():
        # if the user already likes the post
        post.likes.remove(request.user)
        # remove the user from the posts likes
        is_liked = False
    else:
        post.likes.add(request.user)
        # add user to the posts likes
        is_liked = True
        # update boolean value
    return HttpResponseRedirect(post.get_absolute_url())
    # refresh the page with the post that the user is on


def DeletePost(request):
    # create function DeletePost with parameter request
    post = get_object_or_404(Post_model, id=request.POST.get('post_id'))
    # get post to delete
    post.delete(False)
    # delete post from posts table
    return HttpResponseRedirect('../Posts')
    # redirect the user to the Posts view


def Search(request):
    # create search function with parameter request
    query = request.GET.get('query')
    # store search parameters as a query
    if query:
        # if a query has been made when searching
        results = Post_model.objects.filter(Q(title__icontains=query) | Q(content__icontains=query))
        # search for posts with the query in the title or contents of the posts
        # store the collected data as results
    else:
        results = Post_model.objects.all()
        # get all the posts in the database if no query has been made
    context = {
        "results": results,
    }  # store results as a parameter to be used in the template
    return render(request, "Home/search.html", context)
    # render the search template with all the collected results


def SearchFriends(request):
    # create search friends function with parameter request
    query = request.GET.get('query')
    # store search parameters as a query
    if query:
        # if a query has been made when searching
        superuser = User.objects.get(username="admin")
        # define super user as the admin
        results = User.objects.filter(Q(username__icontains=query) | Q(first_name__icontains=query) | Q(last_name__icontains=query))
        # search for users with the query in the username, firstname, lastname
        results = results.exclude(id=request.user.pk)
        results = results.exclude(id=superuser.pk)
        # exclude the current user and super user from the results
    else:
        results = False
        # return false if no query was made
    context = {
        "results": results,
    }  # pass results as context variable in template
    return render(request, "Home/friend search.html", context)
    # render remplate friend search.html with results of search
