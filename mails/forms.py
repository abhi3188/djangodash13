from django import forms

class SendMailForm(forms.Form):
    to_message = forms.EmailField(max_length=100)
    from_message = forms.EmailField(max_length=100,required=False)
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    cc_myself = forms.EmailField(required=False,max_length=100)
    upload = forms.FileField(required=False)
