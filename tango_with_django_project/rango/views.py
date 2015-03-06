from django.shortcuts import render, redirect
from rango.models import Category
from rango.models import Page
from rango.forms import CategoryForm
from rango.forms import PageForm
from rango.forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from datetime import datetime
from rango.bing_search import run_query

from django.http import HttpResponse, HttpResponseRedirect         #Each function is linked to a different url pattern
                                                                   #based on its function name.
def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]

    context_dict = {'categories': category_list, 'pages': page_list}

    visits = request.session.get('visits')
    if not visits:
        visits = 1
    reset_last_visit_time = False

    last_visit = request.session.get('last_visit')
    if last_visit:
        last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")

        if (datetime.now() - last_visit_time).seconds > 0:
            # ...reassign the value of the cookie to +1 of what it was before...
            visits = visits + 1
            # ...and update the last visit cookie, too.
            reset_last_visit_time = True
    else:
        # Cookie last_visit doesn't exist, so create it to the current date/time.
        reset_last_visit_time = True

    if reset_last_visit_time:
        request.session['last_visit'] = str(datetime.now())
        request.session['visits'] = visits
    context_dict['visits'] = visits


    response = render(request,'rango/index.html', context_dict)

    return response
    return render(request, 'rango/index.html', context_dict)
    return HttpResponse("Rango says hey there world")
def about(request):
     # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage is the same as {{ boldmessage }} in the template!
    context_dict = {'boldmessage': "It's me"}
    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.

	# If the visits session varible exists, take it and use it.
    # If it doesn't, we haven't visited the site so set the count to zero.
    if request.session.get('visits'):
       count = request.session.get('visits')
    else:
       count = 0
    return render(request, 'rango/about.html',{'visits': count})
    return HttpResponse("This tutorial has been put together by Rajeevan Vijayakumar, 2080123")

def category(request, category_name_slug):

    # Create a context dictionary which we can pass to the template rendering engine.
	context_dict = {'result_list': None, 'query': None}
	if request.method == 'POST':
            query = request.POST['query'].strip()
	    if query:
		context_dict['result_list'] = run_query(query)
                context_dict['query'] = query
        try:
            category = Category.objects.get(slug=category_name_slug)
            context_dict['category_name'] = category.name
	    context_dict['category'] = category


        # Retrieve all of the associated pages.
        # Note that filter returns >= 1 model instance.
            pages = Page.objects.filter(category=category).order_by('-views')

        # Adds our results list to the template context under name pages.
            context_dict['pages'] = pages
        # We also add the category object from the database to the context dictionary.
        # We'll use this in the template to verify that the category exists.
            context_dict['category'] = category
        except Category.DoesNotExist:
        # We get here if we didn't find the specified category.
        # Don't do anything - the template displays the "no category" message for us.
               pass
	if not context_dict['query']:
         context_dict['query'] = category.name
    # Go render the response and return it to the client.
        return render(request, 'rango/category.html', context_dict)

def add_category(request):
    # A HTTP POST?
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            form.save(commit=True)

            # Now call the index() view.
            # The user will be shown the homepage.
            return index(request)
        else:
            # The supplied form contained errors - just print them to the terminal.
            print form.errors
    else:
        # If the request was not a POST, display the form to enter details.
        form = CategoryForm()

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render(request, 'rango/add_category.html', {'form': form})

def add_page(request, category_name_slug):

    try:
        cat = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
                cat = None

    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if cat:
                page = form.save(commit=False)
                page.category = cat
                page.views = 0
                page.save()
                return category(request, category_name_slug)
        else:
            print form.errors
    else:
        form = PageForm()

    context_dict = {'form':form, 'category': cat}

    return render(request, 'rango/add_page.html', context_dict)


@login_required
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text!")

# Use the login_required() decorator to ensure only those logged in can access the view.
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/rango/')
	
def search(request):

    result_list = []

    if request.method == 'POST':
        query = request.POST['query'].strip()

        if query:
            # Run our Bing function to get the results list!
            result_list = run_query(query)

    return render(request, 'rango/search.html', {'result_list': result_list})
	
def track_url(request):

    if request.method == 'GET':
       if 'page_id' in request.GET:
          page_id = request.GET['page_id']
          try:
              page = Page.objects.get(id=page_id)
          except:
              return redirect('index')
          page.views = page.views + 1
          page.save()
          return redirect(page.url)
    return redirect('index')

def register_profile(request):

    if request.method == "POST":
        profile_form = UserProfileForm(data=request.POST)
	if profile_form.is_valid():
            profile = profile_form.save(commit=False)
            profile.user = get_user_model()
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            profile.save()
            return redirect('index')
        else:
            profile_form = UserProfileForm()
        return render(request, 'registration/profile_registration.html',{'profile_form': profile_form})
