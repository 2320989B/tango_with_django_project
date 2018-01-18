from django.shortcuts import render
from rango.models import Category, Page
from rango.forms import CategoryForm


def index(request):
    # Query the database for a list of ALL categories currently stored.
    # Order the categories by number of likes in descending order.
    # Retrieve the top 5 only - or all if less than 5.
    # Place the list in our context_dict dictionary that will be passed
    # to the template engine.
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    context_dict = {'categories': category_list,
                    'pages': page_list}

    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.
    return render(request, "rango/index.html", context=context_dict)


def about(request):
    context_dict = {"boldmessage": "Crunchy, creamy, cookie, candy, cupcake!"}
    return render(request, "rango/about.html", context=context_dict)


def show_category(request, category_name_slug):
    # Create a context dictionary which we can pass to template rendering
    # engine.
    context_dict = {}

    try:
        # Get all categories which match category_name_slug (there will only
        # ever be zero or one, since all are unique).
        category = Category.objects.get(slug=category_name_slug)
        context_dict['category'] = category

        # Get the corresponding pages.
        pages = Page.objects.filter(category=category)
        context_dict['pages'] = pages

    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['pages'] = None

    return render(request, 'rango/category.html', context_dict)


def add_category(request):
    form = CategoryForm()

    if request.method == 'POST':
        form = CategoryForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            form.save(commit=True)
            # Direct the user back to the index page to allow them to see their addition.
            return index(request)
        # Handle form errors.
        else:
            # Print to terminal.
            print(form.errors)

    # Will handle the bad form, new form, or no form supplied cases.
    # Render the form with error messages (if any).
    return render(request, 'rango/add_category.html', {'form': form})
