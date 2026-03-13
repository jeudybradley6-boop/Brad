from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .models import Product, CartItem, Commande
from .forms import ProductForm, LoginForm
from django.contrib.auth.forms import UserCreationForm


# ----- Home -----
def home(request):
    return render(request, 'home.html')


def commande_success(request):
    return render(request, 'commande_success.html')


# ----- Produit CRUD -----
@login_required
def product_list(request):
    produits = Product.objects.all()
    return render(request, 'product_list.html', {'produits': produits})


@login_required
def add_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()

    return render(request, "add_product.html", {"form": form})


@login_required
def edit_product(request, pk):
    produit = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=produit)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm(instance=produit)

    return render(request, 'edit_product.html', {'form': form})


@login_required
def delete_product(request, pk):
    produit = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        produit.delete()
        return redirect('product_list')

    return render(request, 'delete_product.html', {'produit': produit})


# ----- Panier -----
@login_required
def add_to_cart(request, pk):
    product = get_object_or_404(Product, id=pk)

    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        produit=product
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart')


@login_required
def cart(request):
    items = CartItem.objects.filter(user=request.user)

    for item in items:
        item.subtotal = item.produit.price * item.quantity

    total = sum(item.subtotal for item in items)

    return render(request, 'cart.html', {
        'items': items,
        'total': total
    })


@login_required
def remove_from_cart(request, pk):
    item = get_object_or_404(CartItem, id=pk)
    item.delete()
    return redirect('cart')


# ----- Checkout -----
@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)

    if request.method == "POST":

        if not cart_items.exists():
            return redirect('cart')

        total_price = sum(item.produit.price * item.quantity for item in cart_items)

        commande = Commande.objects.create(
            user=request.user,
            prix_total=total_price
        )

        produits_list = ", ".join([
            f"{item.produit.name} x{item.quantity}" for item in cart_items
        ])

        commande.produit = produits_list
        commande.save()

        # vide panier
        cart_items.delete()

        return redirect('commande_success')

    return render(request, 'checkout.html', {
        'cart_items': cart_items
    })


# ----- Confirmation -----
@login_required
def confirm_order(request):
    return render(request, 'confirm_order.html')


# ----- Mes Commandes -----
@login_required
def mes_commandes(request):
    commandes = Commande.objects.filter(
        user=request.user
    ).order_by('-date_commande')

    return render(request, 'mes_commandes.html', {
        'commandes': commandes
    })


# ----- Auth -----
def signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('product_list')
    else:
        form = UserCreationForm()

    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('product_list')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')