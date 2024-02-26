import os
import django

import sys
sys.path.insert(0, "C:\\Users\\champ\\Downloads\\499\\my_project\\WebScapping")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WebScapping.settings')
django.setup()

from api.models import Logs, Products

def add_log(id, field, value):
    old_data = Products.objects.get(ProductID=id)
    old_value = getattr(old_data, field)
    if old_value != value:
        new_log = Logs.objects.create(
            ProductID = id,
            EditBy = "User",
            EditAttrib = field,
            OldData = old_value,
            NewData = value,
        )
        print(new_log)

if __name__ == "__main__":
    print("This is function module")
else:
    pass