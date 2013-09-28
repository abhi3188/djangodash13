from django import forms

class SendMailForm(forms.Form):
    to_message = forms.EmailField(max_length=100)
    from_message = forms.EmailField(max_length=100)
    subject = forms.CharField(max_length=100)
    message = forms.CharField()
    cc_myself = forms.BooleanField(required=False)
