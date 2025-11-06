from django.shortcuts import render, redirect
from django.views.generic import DeleteView
from django.urls import reverse_lazy
from .models import Product
from .forms import AddProductForm


def home_view(request):
    no_discounted = 0
    error = None
    form = AddProductForm(request.POST or None)

    if request.method == 'POST':
        try:
            if form.is_valid():
                form.save()
                # Redirect after successful save (prevents duplicate on refresh)
                return redirect('home-view')
        except AttributeError:
            error = "Oops! Couldn't get the name or price of the product."
        except Exception as e:
            error = f"Oops! Something went wrong: {str(e)}"

    # Fresh form for GET requests or after redirect
    form = AddProductForm()

    queryset = Product.objects.all()
    number_of_items = queryset.count()

    if number_of_items > 0:
        discount_list = [item for item in queryset if item.old_price > item.current_price]
        no_discounted = len(discount_list)

    context = {
        'queryset': queryset,
        'number_of_items': number_of_items,
        'no_discounted': no_discounted,
        'form': form,
        'error': error,
    }
    return render(request, 'products/index.html', context)


class DeleteProductView(DeleteView):
    model = Product
    template_name = 'products/confirm_delete.html'
    success_url = reverse_lazy('home-view')


def update_product(request):
    queryset = Product.objects.all()
    for product in queryset:
        product.save()
    return redirect('home-view')
