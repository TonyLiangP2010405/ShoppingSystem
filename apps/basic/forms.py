from django import forms
from apps.basic.models import ShippingAddress


class ShippingAddressInfo(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ['receiver_name', 'receiver_phone', 'receiver_mobile', 'receiver_province', 'receiver_city',
                  'receiver_district', 'receiver_address', 'receiver_zip']
        labels = {
            "receiver_name": "receiver_name",
            "receiver_phone": "receiver_phone",
            "receiver_mobile": "receiver_mobile",
            "receiver_province": "receiver_province",
            "receiver_city": "receiver_city",
            "receiver_district": "receiver_district",
            "receiver_address": "receiver_address",
            "receiver_zip": "receiver_zip",
        }
        widgets = {
            "receiver_name": forms.widgets.TextInput(
                attrs={
                    "class": "form-control"
                }),
            "receiver_phone": forms.widgets.TextInput(
                attrs={
                    "class": "form-control"
                }),
            "receiver_province": forms.widgets.TextInput(
                attrs={
                    "class": "form-control"
                }),
            "receiver_city": forms.widgets.TextInput(
                attrs={
                    "class": "form-control"
                }),
            "receiver_mobile": forms.widgets.TextInput(
                attrs={
                    "class": "form-control"
                }),
            "receiver_district": forms.widgets.TextInput(
                attrs={
                    "class": "form-control"
                }),
            "receiver_address": forms.widgets.TextInput(
                attrs={
                    "class": "form-control"
                }),
            "receiver_zip": forms.widgets.TextInput(
                attrs={
                    "class": "form-control"
                }),
        }
        error_messages = {
            "receiver_name": {'required': 'the receiver name cannot be empty',
                              'max_length': 'the max length of receiver name is 50'},
            "receiver_province": {'required': 'the receiver province cannot be empty',
                                  'max_length': 'the max length of receiver province is 100'},
            "receiver_city": {'required': 'the city of receiver cannot be empty',
                              'max_length': 'the max length of receiver is 100'},
            "receiver_district": {'required': 'the district of receiver cannot be empty',
                                  'max_length': 'the max length of receiver district is 100'},
            "receiver_address": {'required': 'the address of receiver cannot be empty',
                                 'max_length': 'the max length of receiver address is 100'},
            "receiver_zip": {'required': 'the zip of receiver address cannot be empty'}
        }
