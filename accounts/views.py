from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from .forms import UserAdminCreationForm, CustomUserChangeForm, PostForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Post, Category


def registerPage(request):
    """
        View for handling user registration.

        This view is accessible to unauthenticated users only, thanks to the @unauthenticated_user decorator.
        It displays a registration form and handles form submission for new user registration.

        Parameters:
        - request: HttpRequest object

        Workflow:
        1. An empty UserAdminCreationForm is instantiated and displayed to the user when the request method is GET.
        2. Upon form submission (POST request), the form is re-instantiated with the POST data.
        3. The form data is validated:
           - If valid, a new user is created, marked as active, and saved to the database.
             A success message is displayed, and the user is redirected to the login page.
           - If invalid, the registration form is re-rendered with validation errors.

        Returns:
        - HttpResponse object rendering the 'accounts/register.html' template with the registration form context.
        """
    form = UserAdminCreationForm()
    if request.method == 'POST':
        form = UserAdminCreationForm(request.POST)
        email = request.POST['email']
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
            user.save()
            username = form.cleaned_data.get('first_name')

            messages.success(request, f'Your Account has been created!' + " " + username)
            return redirect('login')
        else:
            form = UserAdminCreationForm()
    return render(request, 'accounts/register.html', {'form': form})


def loginPage(request):
    """
      View for handling user login.

      This view allows users to log in to the system. It is accessible to unauthenticated users only,
      thanks to the @unauthenticated_user decorator. The view handles both the display of the login form
      and the form submission process.

      Parameters:
      - request: HttpRequest object

      Workflow:
      1. If the request method is POST, the function attempts to authenticate the user with the provided
         username and password.
      2. If authentication is successful, the user is logged in and redirected to their profile page.
      3. If authentication fails, an information message is displayed, and the login form is re-rendered.

      Returns:
      - HttpResponse object rendering the 'login.html' template. For POST requests, this depends on the
        outcome of the authentication process. For GET requests, it simply renders the form.
      """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, email=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('profile')
        else:
            messages.info(request, 'Username Or Password is incorrect')

    context = {}
    return render(request, 'login.html', context)


@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('login')


def profile(request):
    """
        Display the profile page for the logged-in user.

        This view fetches the posts created by the currently logged-in user, ordered by creation date in descending order.
        It then renders the 'accounts/profile.html' template, passing the user and their posts as context.

        Parameters:
        - request: HttpRequest object, containing metadata about the request.

        Returns:
        - HttpResponse object rendering the 'accounts/profile.html' template with the user and their posts as context.
        """
    user = request.user
    user_posts = Post.objects.filter(author=user).order_by('-created_at')
    return render(request, 'accounts/profile.html', {'user': user, 'user_posts': user_posts})


@login_required
def edit_profile(request):
    """
        View for handling user profile editing.

        This view allows authenticated users to edit their profile information. It uses the CustomUserChangeForm
        to display the user's current information in a form and to save the updated information upon form submission.

        The @login_required decorator ensures that only authenticated users can access this view. If an unauthenticated
        user attempts to access this view, they are redirected to the login page.

        Parameters:
        - request: HttpRequest object

        Workflow:
        1. If the request method is POST, the form is instantiated with the POST data and the current user instance.
           This allows for the user's information to be updated upon form submission.
        2. If the form is valid, the updated information is saved, and the user is redirected to their profile page.
        3. If the request method is not POST (e.g., GET), an instance of the form with the current user's information
           is created and displayed.

        Returns:
        - HttpResponse object rendering the 'accounts/edit_profile.html' template with the form context.
        """
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = CustomUserChangeForm(instance=request.user)
    return render(request, 'accounts/edit_profile.html', {'form': form})


def latest_blog_posts(request):
    """
        Display a paginated list of the latest blog posts.

        This view filters blog posts by category if a category ID is provided in the request's GET parameters.
        It paginates the posts, showing a specified number of posts per page.

        Parameters:
        - request: HttpRequest object, containing metadata about the request.

        Workflow:
        1. Checks if a 'category' ID is provided in the GET parameters of the request.
           - If yes, filters the posts by the specified category.
           - If no, selects all posts.
        2. Orders the selected posts by their creation date in descending order.
        3. Paginates the posts, showing a fixed number of posts per page.
        4. Fetches all categories for category filter options in the template.

        Returns:
        - HttpResponse object rendering the 'accounts/latest_blog_posts.html' template with the paginated posts,
          categories, and the selected category (if any) as context.
        """
    category_id = request.GET.get('category')
    if category_id:
        posts_list = Post.objects.filter(category_id=category_id).order_by('-created_at')
    else:
        posts_list = Post.objects.order_by('-created_at')

    paginator = Paginator(posts_list, 5)  # Show 5 blog posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    categories = Category.objects.all()

    return render(request, 'accounts/latest_blog_posts.html',
                  {'page_obj': page_obj, 'categories': categories, 'selected_category': category_id})


@login_required
def create_post(request):
    """
        View for creating a new blog post.

        This view allows authenticated users to create a new blog post. It displays a form for post creation
        and handles the form submission. Upon successful form submission, the new post is saved with the current
        user set as the author and redirects to the user's profile page.

        Parameters:
        - request: HttpRequest object

        Workflow:
        1. If the request method is POST, the form is instantiated with the POST data.
        2. If the form is valid, a new post instance is created but not saved to the database (commit=False).
           The current user is set as the author of the post, and then the post is saved.
        3. After saving the post, the user is redirected to their profile page.
        4. If the request method is not POST (e.g., GET), an empty form is displayed to the user.

        Returns:
        - HttpResponse object rendering the 'accounts/create_post.html' template with the form context for GET requests.
          For POST requests, redirects to the user's profile page upon successful post creation.
        """
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()
            return redirect('profile')
    else:
        form = PostForm()
    return render(request, 'accounts/create_post.html', {'form': form})


@login_required
def edit_post(request, pk):
    """
        View for editing an existing blog post.

        This view allows authenticated users to edit their own blog posts. It ensures that only the author of the post
        can edit it. The view handles both the display of the post form pre-filled with the post's current data and the
        form submission process for updating the post.

        Parameters:
        - request: HttpRequest object
        - pk: Primary key of the post to be edited

        Workflow:
        1. The post is fetched from the database using its primary key and the current user's information. If the post
           does not exist or the current user is not the author, a 404 error is raised.
        2. If the request method is POST, the form is instantiated with the POST data and the post instance. This allows
           for the post's information to be updated upon form submission.
        3. If the form is valid, the updated post information is saved, and the user is redirected to their profile page.
        4. If the request method is not POST (e.g., GET), an instance of the form pre-filled with the post's current data
           is created and displayed.

        Returns:
        - HttpResponse object rendering the 'accounts/edit_post.html' template with the form and post instance as context
          for GET requests. For POST requests, redirects to the user's profile page upon successful post update.
        """
    post = get_object_or_404(Post, pk=pk, author=request.user)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = PostForm(instance=post)
    return render(request, 'accounts/edit_post.html', {'form': form, 'post': post})


def post_detail(request, pk):
    """
        Display the details of a specific blog post.

        This view fetches the post with the given primary key (pk) from the database and displays its details.
        It also allows users to add comments to the post.

        Parameters:
        - request: HttpRequest object
        - pk: Primary key of the post to be displayed

        Workflow:
        1. The post is fetched from the database using its primary key. If the post does not exist, a 404 error is raised.
        2. Comments associated with the post are fetched and displayed.
        3. If the request method is POST, a new comment is created and saved to the database.
        4. The post details, comments, new comment instance, and comment form are passed to the template for rendering.

        Returns:
        - HttpResponse object rendering the 'accounts/post_detail.html' template with the post, comments, new comment,
          and comment form as context.
        """
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.filter(active=True)
    new_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(request, 'accounts/post_detail.html', {
        'post': post,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form
    })
