from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from .forms import UserForm, RegisterForm
from search.models import Product, Category, User, DetailProduct


def index(request):
    template = loader.get_template('search/index.html')
    return HttpResponse(template.render(request=request))

def listing(request):
    product_list = Product.objects.filter(category_id=1).order_by('barcode')
    paginator = Paginator(product_list, 9)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        products = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        products = paginator.page(paginator.num_pages)

    context = {
        'products': products,
        'paginate': True
    }
    return render(request, 'search/list_all.html', context)

# @login_required()
def search(request):
    template = loader.get_template('search/form.html')
    return HttpResponse(template.render(request=request))   

# @login_required()
def searching(request):
    query = request.GET.get('query')
    products_nutriscore = "d" # a revoir
    message = ""

    if not query:
        message = "Remplissez le champ de recherche"
    else:
        products = Product.objects.filter(product_name__icontains=query)[:1]
        # products_nutriscore = products.nutriscore_grade
        products_nutriscore = "d"
    if not products.exists():   
        message = "No Products found!"

    substitutes = Product.objects.filter(nutriscore_grade__lt=products_nutriscore)
    paginator = Paginator(substitutes, 9)
    page = request.GET.get('page')
    try:
        substitutes = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        substitutes = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        substitutes = paginator.page(paginator.num_pages)
    
    context = {
        'substitutes': substitutes,
        'products': products,
        'query': query,
        'paginate': True,
        'message': message
    }
    return render(request, 'search/list.html', context)

def login2(request):

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = UserForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            if form.cleaned_data:
                post = User()
                # post.username = request.POST.get('username')
                post.email = request.POST.get('email')
                # post.first_name = request.POST.get('first_name')
                # post.last_name = request.POST.get('last_name')
                post.password = request.POST.get('password')
                post.save()
            # redirect to a new URL:
            return HttpResponseRedirect('/search/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = UserForm()

    return render(request, 'search/login.html', {'form': form})

def logout2(request):

    logout(request)

    return redirect(reverse("index"))

def register(request):

    registered = False
    if request.method == 'POST':
        user_form = RegisterForm(data=request.POST)
        if user_form.is_valid():
            user_form.save()
            # user = user_form.save()
            """ user.set_password(user.password)
            user.save() """
            registered = True
        else:
            print(user_form.errors)
    else:
        user_form = RegisterForm()
    return render(request,'registration.html',
                          {'user_form':user_form,
                           'registered':registered})

def profile(request, username=None):

      if username:
        post_owner = get_object_or_404(User, username=username)

      else:
        post_owner = request.user

      args1 = {
        'post_owner': post_owner,
      }
      return render(request, 'profile.html', args1)

def mentions(request):
    template = loader.get_template('search/mentions.html')
    return HttpResponse(template.render(request=request))

# @login_required()
def detail(request, barcode):
    # product = get_object_or_404(Product, pk=barcode)
    products = Product.objects.filter(barcode__icontains=barcode)[:1]
    detail_products = DetailProduct.objects.filter(code_id__barcode__icontains=barcode)[:1]
    for product in products:
        product_dict = {
            'product_name': product.product_name,
            'product_grade': product.nutriscore_grade,
            'product_pic': product.picture_path,
            'product_url': product.url,
            'small_product_pic': product.small_picture_path
        }

    for detail_product in detail_products:
        detail_products_dict = {
            'energy_100g' : detail_product.energy_100g,
            'energy_unit' : detail_product.energy_unit,
            'sugars_100g' : detail_product.sugars_100g,
            'fiber_100g' : detail_product.fiber_100g,
            'salt_100g' : detail_product.salt_100g
        }

    context = {**product_dict, **detail_products_dict}

    return render(request, 'search/detail.html', context)

