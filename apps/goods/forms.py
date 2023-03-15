from django.core.exceptions import ValidationError
from django import forms
from apps.goods.models import ProductsCategory, Product


class ProductsCategoryInfo(forms.ModelForm):
    class Meta:
        model = ProductsCategory
        fields = ['name']
        labels = {
            "name": "product_category_name"
        }
        widgets = {
            "name": forms.widgets.TextInput(attrs={
                "class": "form-control"
            }),
        }
        error_messages = {
            "name": {'required': 'the product category name cannot be empty'}
        }

    def clean_name(self):
        new_name = self.cleaned_data.get('name')
        product_categories = ProductsCategory.objects.all()
        for productCategory in product_categories:
            if productCategory.name == new_name:
                self.add_error("name", ValidationError("the product category has been existed"))


class ProductInfo(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'price', 'property1', 'property2', 'property3', 'property4', 'property5',
                  'property6', 'main_image',
                  'temporary_status', 'photo1',
                  'photo2', 'photo3', 'photo4',
                  ]
        labels = {
            "name": "name",
            "category": "product_category",
            "price": "product_price",
            "property1": "property1",
            "property2": "property2",
            "property3": "property3",
            "property4": "property4",
            "property5": "property5",
            "property6": "property6",
            "main_image": "product_main_image",
            "temporary_status": "temporary_status",
            "photo1": "photo1",
            "photo2": "photo2",
            "photo3": "photo3",
            "photo4": "photo4",
        }
        widgets = {
            "name": forms.widgets.TextInput(attrs={
                "class": "form-control"
            }),
            "price": forms.widgets.NumberInput(attrs={
                "class": "form-control"
            }),
            "property1": forms.widgets.TextInput(attrs={
                "class": "form-control"
            }),
            "property2": forms.widgets.TextInput(attrs={
                "class": "form-control"
            }),
            "property3": forms.widgets.TextInput(attrs={
                "class": "form-control"
            }),
            "property4": forms.widgets.TextInput(attrs={
                "class": "form-control"
            }),
            "property5": forms.widgets.TextInput(attrs={
                "class": "form-control"
            }),
            "property6": forms.widgets.TextInput(attrs={
                "class": "form-control"
            }),
            "main_image": forms.widgets.FileInput(attrs={
                "class": 'custom-file-input'
            }),
            "category": forms.widgets.Select(attrs={
                "class": "form-control"
            }),
            "temporary_status": forms.widgets.Select(attrs={
                "class": "form-control"
            }),
            "photo1": forms.widgets.FileInput(attrs={
                "class": 'custom-file-input'
            }),
            "photo2": forms.widgets.FileInput(attrs={
                "class": 'custom-file-input'
            }),
            "photo3": forms.widgets.FileInput(attrs={
                "class": 'custom-file-input'
            }),
            "photo4": forms.widgets.FileInput(attrs={
                "class": 'custom-file-input'
            }),
        }
        error_messages = {
            "name": {'required': 'the product name cannot be empty',
                     'max_length': 'the max length of product name is 50'},
            "category": {'required': 'the product category cannot be empty'},
            "price": {'required': 'the product price cannot be empty',
                      'max_digits': 'the max digits of product price is 32',
                      'decimal_places': 'the decimal place of product price is 8'},
            "property1": {'required': 'the property1 of product cannot be empty',
                          'max_length': 'the max length of property1 is 5000'},
            "property2": {'required': 'the property2 of product cannot be empty',
                          'max_length': 'the max length of property2 is 5000'},
            "property3": {'required': 'the property3 of product cannot be empty',
                          'max_length': 'the max length of property3 is 5000'},
            "property4": {'required': 'the property4 of product cannot be empty',
                          'max_length': 'the max length of property4 is 5000'},
            "property5": {'required': 'the property5 of product cannot be empty',
                          'max_length': 'the max length of property5 is 5000'},
            "property6": {'required': 'the property6 of product cannot be empty',
                          'max_length': 'the max length of property6 is 5000'},
            "createDate": {'required': 'the create date of product cannot be empty'},
        },

    def clean(self):
        new_product_name = self.cleaned_data.get('name')
        products = Product.objects.all()
        for product in products:
            if product.name == new_product_name:
                self.add_error("name", ValidationError("the product name has been existed"))


class ProductInfoChange(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'price', 'property1', 'property2', 'property3', 'property4', 'property5',
                  'property6', 'customer_rating', 'review', 'main_image',
                  'temporary_status', 'photo1',
                  'photo2', 'photo3', 'photo4',
                  ]
        labels = {
            "name": "name",
            "category": "product_category",
            "price": "product_price",
            "property1": "property1",
            "property2": "property2",
            "property3": "property3",
            "property4": "property4",
            "property5": "property5",
            "property6": "property6",
            "main_image": "product_main_image",
            "temporary_status": "temporary_status",
            "photo1": "photo1",
            "photo2": "photo2",
            "photo3": "photo3",
            "photo4": "photo4",
        }
        widgets = {
            "name": forms.widgets.TextInput(attrs={
                "class": "form-control"
            }),
            "price": forms.widgets.NumberInput(attrs={
                "class": "form-control"
            }),
            "property1": forms.widgets.TextInput(attrs={
                "class": "form-control"
            }),
            "property2": forms.widgets.TextInput(attrs={
                "class": "form-control"
            }),
            "property3": forms.widgets.TextInput(attrs={
                "class": "form-control"
            }),
            "property4": forms.widgets.TextInput(attrs={
                "class": "form-control"
            }),
            "property5": forms.widgets.TextInput(attrs={
                "class": "form-control"
            }),
            "property6": forms.widgets.TextInput(attrs={
                "class": "form-control"
            }),
            "main_image": forms.widgets.FileInput(attrs={
                "class": 'custom-file-input'
            }),
            "category": forms.widgets.Select(attrs={
                "class": "form-control"
            }),
            "temporary_status": forms.widgets.Select(attrs={
                "class": "form-control"
            }),
            "photo1": forms.widgets.FileInput(attrs={
                "class": 'custom-file-input'
            }),
            "photo2": forms.widgets.FileInput(attrs={
                "class": 'custom-file-input'
            }),
            "photo3": forms.widgets.FileInput(attrs={
                "class": 'custom-file-input'
            }),
            "photo4": forms.widgets.FileInput(attrs={
                "class": 'custom-file-input'
            }),
        }
        error_messages = {
            "name": {'required': 'the product name cannot be empty',
                     'max_length': 'the max length of product name is 50'},
            "category": {'required': 'the product category cannot be empty'},
            "price": {'required': 'the product price cannot be empty',
                      'max_digits': 'the max digits of product price is 32',
                      'decimal_places': 'the decimal place of product price is 8'},
            "property1": {'required': 'the property1 of product cannot be empty',
                          'max_length': 'the max length of property1 is 5000'},
            "property2": {'required': 'the property2 of product cannot be empty',
                          'max_length': 'the max length of property2 is 5000'},
            "property3": {'required': 'the property3 of product cannot be empty',
                          'max_length': 'the max length of property3 is 5000'},
            "property4": {'required': 'the property4 of product cannot be empty',
                          'max_length': 'the max length of property4 is 5000'},
            "property5": {'required': 'the property5 of product cannot be empty',
                          'max_length': 'the max length of property5 is 5000'},
            "property6": {'required': 'the property6 of product cannot be empty',
                          'max_length': 'the max length of property6 is 5000'},
            "createDate": {'required': 'the create date of product cannot be empty'},
        },

class ProductPhotoChange(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['main_image', 'photo1', 'photo2', 'photo3', 'photo4']
        labels = {
            "main_image": "main_image",
            "photo1": "photo1",
            "photo2": "photo2",
            "photo3": "photo3",
            "photo4": "photo4",
        }
        widgets = {
            "main_image": forms.widgets.FileInput(attrs={
                "class": 'custom-file-input'
            }),
            "photo1": forms.widgets.FileInput(attrs={
                "class": 'custom-file-input'
            }),
            "photo2": forms.widgets.FileInput(attrs={
                "class": 'custom-file-input'
            }),
            "photo3": forms.widgets.FileInput(attrs={
                "class": 'custom-file-input'
            }),
            "photo4": forms.widgets.FileInput(attrs={
                "class": 'custom-file-input'
            }),
        }
