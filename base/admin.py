from django.contrib import admin
from .models import Room, Hall, Customer, Category, GymUser, HallBook

admin.site.register(Room)
admin.site.register(Hall)
admin.site.register(Customer)
admin.site.register(Category)
admin.site.register(GymUser)
admin.site.register(HallBook)
