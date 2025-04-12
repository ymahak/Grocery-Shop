from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Count
from .models import Category, Product
from django.core.paginator import Paginator

def home(request):
    categories = Category.objects.all()
    featured_products = Product.objects.filter(available=True)[:8]
    return render(request, 'products/home.html', {
        'categories': categories,
        'featured_products': featured_products,
    })

def product_list(request):
    products = Product.objects.filter(available=True)
    categories = Category.objects.all()
    
    # Filter by category
    category_slug = request.GET.get('category')
    if category_slug:
        products = products.filter(category__slug=category_slug)
    
    # Filter by price range
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)
    
    # Search
    query = request.GET.get('q')
    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )
    
    return render(request, 'products/product_list.html', {
        'products': products,
        'categories': categories,
    })

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, available=True)
    return render(request, 'products/product_detail.html', {
        'product': product,
    })

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category, available=True)
    
    # Handle sorting
    sort = request.GET.get('sort', 'name')
    if sort in ['name', '-name', 'price', '-price']:
        products = products.order_by(sort)
    
    # Handle price filtering
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        products = products.filter(price__gte=float(min_price))
    if max_price:
        products = products.filter(price__lte=float(max_price))
    
    # Handle in stock filter
    if request.GET.get('in_stock'):
        products = products.filter(stock__gt=0)
    
    # Pagination
    paginator = Paginator(products, 9)  # Show 9 products per page
    page = request.GET.get('page')
    products = paginator.get_page(page)
    
    context = {
        'category': category,
        'products': products,
        'is_paginated': paginator.num_pages > 1,
        'page_obj': products,
        'total_products': products.paginator.count if products else 0
    }
    
    return render(request, 'products/category_detail.html', context)

def search(request):
    query = request.GET.get('q', '')
    sort = request.GET.get('sort', '')
    products = Product.objects.filter(available=True)
    
    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query)
        )
    
    # Apply sorting
    if sort:
        if sort == 'price_asc':
            products = products.order_by('price')
        elif sort == 'price_desc':
            products = products.order_by('-price')
        elif sort == 'name_asc':
            products = products.order_by('name')
        elif sort == 'name_desc':
            products = products.order_by('-name')
    else:
        products = products.order_by('-created')  # Default sorting by newest first
    
    # Pagination
    paginator = Paginator(products, 12)  # Show 12 products per page
    page = request.GET.get('page')
    products = paginator.get_page(page)
    
    return render(request, 'products/search_results.html', {
        'query': query,
        'products': products,
        'sort': sort,
        'is_paginated': paginator.num_pages > 1,
        'page_obj': products,
    }) 