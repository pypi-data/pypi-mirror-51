from django.db import models
from django.db.models.deletion import PROTECT
from edc_constants.constants import NOT_APPLICABLE
from edc_model.validators import date_not_future
from edc_model_fields.fields.other_charfield import OtherCharField
from edc_utils import get_utcnow

from ..choices import AE_GRADE
from ..models import AeClassification


class AeModelMixin(models.Model):

    ae_auto_created = models.BooleanField(max_length=25, default=False, editable=False)

    ae_auto_created_criteria = models.CharField(
        max_length=50, default=NOT_APPLICABLE, editable=False
    )

    report_datetime = models.DateTimeField(
        verbose_name="Report Date and Time", default=get_utcnow
    )

    ae_classification = models.ForeignKey(
        AeClassification,
        on_delete=PROTECT,
        verbose_name="Adverse Event (AE) Classification",
        null=True,
        blank=False,
    )

    ae_classification_other = OtherCharField(max_length=250, blank=True, null=True)

    ae_description = models.TextField(verbose_name="Adverse Event (AE) description")

    ae_awareness_date = models.DateField(
        verbose_name="AE Awareness date",
        default=get_utcnow,
        validators=[date_not_future],
    )

    ae_start_date = models.DateField(
        verbose_name="Actual Start Date of AE",
        default=get_utcnow,
        validators=[date_not_future],
    )

    ae_grade = models.CharField(
        verbose_name="Severity of AE", max_length=25, choices=AE_GRADE
    )

    class Meta:
        abstract = True
