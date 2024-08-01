from django.apps import AppConfig
from django.conf import settings

class RealEstatesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'real_estates'

    def ready(self) -> None:


            from .models import RealEstateChoice
            print('adding real estate choices')
            try:
                RealEstateChoice.add_default_rows()
            except Exception as e:
                print(e)
            print('done')

            return super().ready()
