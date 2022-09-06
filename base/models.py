from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    group = models.CharField(max_length=20)
    price = models.IntegerField()
    total = models.IntegerField('Amount available')

    def __str__(self):
        return self.group

class Room(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    room_number = models.CharField(max_length=3)
    STATUSES = [
        ('v', 'vacant'),
        ('o', 'occupied'),
        ('b', 'booked'),
    ]
    status = models.CharField(max_length=1, choices=STATUSES, default='v')
    occupant = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, default=None)

    class Meta:
        ordering = ['room_number', 'category', 'status', 'occupant']

    def __str__(self):
        return f"Room-{self.room_number}"

class Hall(models.Model):
    hall = models.CharField(max_length=20)
    price = models.IntegerField()
    def __str__(self):
        return self.hall

class Customer(models.Model):
    full_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=11)
    email = models.EmailField(null=True)
    default_room = Room.objects.get(room_number='001').pk
    default_hall = Hall.objects.get(hall='Hall-0').pk
    room = models.ForeignKey(Room, on_delete=models.SET_DEFAULT, default=default_room)
    hall = models.ForeignKey(Hall, on_delete=models.SET_DEFAULT, default=default_hall)
    user_link = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)
    gym_status = models.BooleanField(default=False)
    hall_status = models.BooleanField(default=False)
    check_in_date = models.DateField(null=True, default='0001-01-01')
    book_date = models.DateField(null=True, default='0001-01-01')

    def __str__(self):
        return self.full_name

    class Meta():
        ordering = ['full_name']

class GymUser(models.Model):
    MEMBERSHIP_GROUPS = [
        ('d', 'diamond'),
        ('p', 'platinum'),
        ('g', 'gold'),
    ]
    membership_group = models.CharField(max_length=1, choices=MEMBERSHIP_GROUPS)
    TRAINERS = [
        ('t', 'Trent'),
        ('m', 'Mandy'),
        ('J', 'Jake'),
        ('b', 'Brad'),
        ('e', 'Erika'),
    ]
    trainer = models.CharField(max_length=1, choices=TRAINERS)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    SUBSCRIPTIONS = [
        ('w', 'week'),
        ('m', 'month'),
        ('y', 'year'),
    ]
    subscription = models.CharField(max_length=1, choices=SUBSCRIPTIONS)
    start_date = models.DateField(null=True, default='0001-01-01')

    def __str__(self):
        return str(self.customer)

    class Meta:
        ordering = ['membership_group', 'trainer']

class HallBook(models.Model):
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    book_date = models.DateField()

    def __str__(self):
        return str(self.customer)
    
    class Meta:
        ordering = ['book_date']
