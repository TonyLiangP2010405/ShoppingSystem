from apps.order.models import ReviewAndRating
from django.core.exceptions import ValidationError
from django import forms


class ReviewRatingChangeForm(forms.ModelForm):
    class Meta:
        model = ReviewAndRating
        fields = ['review', 'customer_rating']
        labels = {"review": "review",
                  "customer_rating": "customer_rating"}
        widgets = {
            "review": forms.widgets.Textarea(attrs={
                "class": 'form-control'
            }),
            "customer_rating": forms.widgets.Select(attrs={
                "class": "form-control"
            }),
        }
