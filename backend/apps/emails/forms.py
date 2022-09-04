from apps.emails.models import EmailTemplate
from ckeditor.widgets import CKEditorWidget
from django.forms import ModelForm


class HTMLTextField(ModelForm):
    """This form overrides widget for a body field."""

    class Meta:
        model = EmailTemplate
        widgets = {
            "body": CKEditorWidget(),
        }
        fields = "__all__"
