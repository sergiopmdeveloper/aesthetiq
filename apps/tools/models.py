from django.db import models

from authentication.models import AppUser


class BackgroundRemoverResult(models.Model):
    """
    Background remover result model.
    """

    user = models.ForeignKey(
        AppUser, on_delete=models.CASCADE, related_name="background_remover_results"
    )

    result_name = models.CharField(max_length=255)
    original_image = models.BinaryField()
    processed_image = models.BinaryField()

    def __str__(self) -> str:
        """
        String representation of the background remover result.

        Returns
        -------
        str
            The background remover result name.
        """

        return self.result_name

    class Meta:
        """
        Metadata options.
        """

        db_table = "background_remover_results"
        verbose_name_plural = "Background remover results"
