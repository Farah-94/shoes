from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    display = forms.BooleanField(
        required=False,
        initial=True,
        label="Show this review publicly"
    )

    class Meta:
        model = Review
        fields = ["rating", "comment", "display"]
        widgets = {
            "rating": forms.RadioSelect,
            "comment": forms.Textarea(attrs={"rows": 4, "placeholder": "Write your review…"})
        }
        labels = {
            "rating": "Your Rating",
            "comment": "Your Review"
        }
