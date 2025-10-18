from django.db import models
from core_utils.utils.generics.generic_models import CoreGenericModel
import uuid



class paidfile(CoreGenericModel):
    id = models.UUIDField(
        primary_key= True,
        editable= False,
        db_column="PAID_ID",
        default=uuid.uuid4
    )
    loan_account_no = models.CharField(
        max_length= 20,
        db_column="LOAN_ACCOUNT_NO",
        null= False,
        unique= True,
        blank= False
    )
    payment_mode_code= models.CharField(
        max_length= 10,
        db_column="PAYMENT_MODE_CODE",
        null= False,
        blank= False
    )
    payment_amt= models.IntegerField(
       
        db_column="PAYMENT_AMT",
        null= False,
        blank= False,
    )
    payment_date = models.DateField(
        db_column="PAYMENT_DATE",
        null= False,
        blank= False
    )
