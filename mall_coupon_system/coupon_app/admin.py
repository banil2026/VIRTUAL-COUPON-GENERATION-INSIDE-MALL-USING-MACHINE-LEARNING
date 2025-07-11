from django.contrib import admin
from .models import Store, UserProfile, Coupon, Purchase, UploadedDataset

admin.site.register(Store)
admin.site.register(UserProfile)
admin.site.register(Coupon)
admin.site.register(Purchase)
admin.site.register(UploadedDataset)

