from django.shortcuts import render

# Create your views here.
from django.shortcuts import redirect
from .models import Review
from .forms import ReviewForm
from django.contrib import messages

def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    
    if request.method == "POST":
        try:
            reviews = Review.objects.get(user=request.user, product_id=product_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, "Your review has been updated.")
            return redirect(url)
        except:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = Review()
                data.subject = form.cleaned_data['subject']
                data.review = form.cleaned_data['review']
                data.rating = form.cleaned_data['rating']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, "Your review has been submitted.")
                return redirect(url)
