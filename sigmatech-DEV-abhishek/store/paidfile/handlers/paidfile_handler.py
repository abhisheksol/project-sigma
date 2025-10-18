

from ctypes import Union
from core_utils.utils.generics.serializers.mixins import CoreGenericBaseHandler
from django.db import transaction
import pandas as pd
from store.paidfile.models import paidfile as PaidfileModel
class Paidfilehandler(CoreGenericBaseHandler):
    def validate(self):
        print("file path:---------->", self.data.get("file_path"))
        file_path : Union[str, None] = self.data.get("file_path")

        self.df : pd.DataFrame = pd.read_csv(file_path)
        required_columns= ['LAN', 'Payment Mode', 'Payment Amount', 'Payment Date']
        for col in required_columns:
            if col not in self.df.columns:
                return self.set_error_message(f"Missing required column: {col}", key=col)
            
        

    def create(self):
        with transaction.atomic():
            print("Creating paidfile instances from CSV data...")
            for _, row in self.df.iterrows():
                paidfile_instance : PaidfileModel = self.queryset.create(
                    loan_account_no= row['LAN'],
                    payment_mode_code= row['Payment Mode'],
                    payment_amt= row['Payment Amount'],
                    payment_date= row['Payment Date'],
                )
            self.logger.info(f"Paidfile instance created {paidfile_instance.pk} successfully.")
           

