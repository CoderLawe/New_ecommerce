from django import forms
from store.models import CarouselData, Product, Order, Category


class CarouselForm(forms.ModelForm):
    class Meta:
        model = CarouselData

        fields = ['body', 'image']

        widgets = {
            'body': forms.Textarea(attrs={'class': 'form-group row'}),

            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),


        }


class CreateProduct(forms.ModelForm):

    class Meta:
        model = Product

        fields = ['name', 'price','category', 'digital', 'image', 'description', 'slug']

        widgets = {
            'name':forms.TextInput(attrs={'class':'form-group row'}),
            'price': forms.TextInput(attrs={'class': 'form-group row'}),
            'category': forms.TextInput(attrs={'class': 'form-group row'}),
            'digital': forms.CheckboxInput(attrs={'class': 'form-group row'}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
            'description': forms.Textarea(attrs={'class': 'form-group row'}),
            'slug': forms.TextInput(attrs={'class': 'form-group row'}),

        }

class CustomerLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'

class UpdateProduct(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'



