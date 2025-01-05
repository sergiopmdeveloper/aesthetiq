from django.forms import ModelForm

from apps.tools.models import BackgroundRemoverResult


class BackgroundRemoverResultForm(ModelForm):
    """
    Background remover result form.
    """

    class Meta:
        """
        Metadata options.
        """

        model = BackgroundRemoverResult
        fields = ["user", "result_name"]
        error_messages = {"result_name": {"required": "Result name is required."}}
