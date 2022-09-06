from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
import datetime as dt

from .models import Room, Hall, User, Category, Customer, GymUser, HallBook
from .forms import GymForm, CreateUserForm
from .decorators import authenticated_user, allowed_users

def show_control(request):
    if request.user.is_authenticated:
        group = request.user.groups.all()[0].name
        return group
    else:
        return None

def home_page(request):
    group = show_control(request)
    context = {'group': group}
    return render(request, 'base/home.html', context)

@login_required(login_url='login_page')
def get_room(request):
    context = {}
    user = request.user
    customer = Customer.objects.get(user_link=user)
    if request.method == 'GET' and request.GET.get('category_selector') == 'category':
        cat = request.GET.get('room_cat')
        cat_model = Category.objects.get(group__iexact=cat)
        rooms = Room.objects.filter(category=cat_model, status='v')
        context = {'rooms': rooms, 'msg': f'Showing Available {cat} Rooms', 'book': False}

    if request.method == 'GET' and request.GET.get('book_room') == 'book':
        default_room = Room.objects.get(room_number='001')
        if customer.room == default_room:
            room = request.GET.get('room')
            room_number = str(room[5:])
            room = Room.objects.get(room_number=room_number)
            room.status = 'b'
            room.occupant = user
            room.save()
            context['book'] = True
            context['room'] = room
            customer.is_active = True
            customer.room = room
            customer.save()
            messages.success(request, f'Room {room_number} booked successfully')
            return redirect('home_page')
        else:
            messages.success(request, 'Sorry, You Already Have A Room')
            return redirect('home_page')

    group = show_control(request)
    context['group'] = group

    return render(request, 'base/get_room.html', context)

'''
@login_required(login_url='login_page')
def get_hall(request):
    group = show_control(request)

    sm_hall_status = Hall.objects.get(hall__iexact='small hall').status
    md_hall_status = Hall.objects.get(hall__iexact='medium hall').status
    lg_hall_status = Hall.objects.get(hall__iexact='large hall').status
    context = {'sm_hall_status': sm_hall_status, 'md_hall_status': md_hall_status, 'lg_hall_status': lg_hall_status, 'group': group}

    return render(request, 'base/get_hall.html', context)

@login_required(login_url='login_page')
def book_sm_hall(request):
    hall = Hall.objects.get(hall__iexact='small hall')
    hall.status = 'b'
    hall.occupant = request.user
    hall.save()
    messages.success(request, 'Hall Booked')
    return redirect('hall_page')

@login_required(login_url='login_page')
def book_md_hall(request):
    hall = Hall.objects.get(hall__iexact='medium hall')
    hall.status = 'b'
    hall.occupant = request.user
    hall.save()
    messages.success(request, 'Hall Booked')
    return redirect('hall_page')

@login_required(login_url='login_page')
def book_lg_hall(request):
    hall = Hall.objects.get(hall__iexact='large hall')
    hall.status = 'b'
    hall.occupant = request.user
    hall.save()
    messages.success(request, 'Hall Booked')
    return redirect('hall_page')
'''

@login_required(login_url='login_page')
def gym_page(request):
    group = show_control(request)
    form = GymForm()
    context = {'form': form, 'group': group}
    
    if request.method == 'POST':
        mem_group = request.POST.get('mem_grp')
        trainer = request.POST.get('trainer')
        user = request.user
        customer = Customer.objects.get(user_link=user)
        sub = request.POST.get('sub')
        start_date = request.POST.get('date')

        new_user = GymUser(
            membership_group=mem_group,
            trainer=trainer,
            customer=customer,
            subscription=sub,
            start_date=start_date
        )
        new_user.save()
        customer.gym_status = True
        customer.save()

        messages.success(request, 'Registration Complete')
        return redirect('home_page')
        
    return render(request, 'base/gym_reg.html', context)

@authenticated_user
def user_reg(request):
    form = CreateUserForm()

    if request.method == 'POST':
        fullname = request.POST.get('full_name')
        phone_no = request.POST.get('phone_no')

        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()

            #create customer model
            customer = Customer(
                full_name=fullname,
                phone_number=phone_no,
                email=user.email,
            )
            customer.save()
            user.save()

            group = Group.objects.get(name='customer')
            user.groups.add(group)
            
            login(request, user)
            return redirect('home_page')
        else:
            messages.error(request, 'Sorry, an error occurred. Try again')

    context = {'form': form}
    return render(request, 'base/login_reg.html', context)

@authenticated_user
def login_page(request):
    page = 'login'
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        check = True
        try:
            user = User.objects.get(username=username)
        except:
            check = False
            messages.error(request, 'User does not Exist')
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home_page')
        elif check:
            messages.error(request, 'Incorrect Password')
        
    context = {'page': page}
    return render(request, 'base/login_reg.html', context)

def logout_page(request):
    logout(request)
    return redirect('home_page')

@allowed_users(allowed_roles=['staff'])
def control_page(request):
    group = show_control(request)
    user_form = CreateUserForm()

    # Add User
    if request.method == 'POST' and request.POST.get('check1') == 'add_user':
        full_name = request.POST.get('fullname')
        phone = request.POST.get('phone')

        user_form = CreateUserForm(request.POST)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            #create customer model
            customer = Customer(
                full_name=full_name,
                phone_number=phone,
                email=user.email,
                user_link=user
            )
            customer.save()

            group = Group.objects.get(name='customer')
            user.groups.add(group)
            messages.success(request, 'User Registered')
            return redirect('control_page')
        else:
            messages.error(request, 'Sorry, an error occurred. Try again')
    
    # Get Room
    if request.method == 'POST' and request.POST.get('check2') == 'book_room':
        username = request.POST.get('username').lower()
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User doesn't exist")
            return redirect('control_page')
        category = request.POST.get('room_cat')
        room_no = request.POST.get('room_no')
        action = request.POST.get('action')
        if request.POST.get('check_in_date') == '':
            check_in_date = '0001-01-01'
        else:
            check_in_date = request.POST.get('check_in_date')
        if request.POST.get('book_date') == '':
            book_date = '0001-01-01'
        else:
            book_date = request.POST.get('book_date')
        try:
            cat = Category.objects.get(group=category)
            room = Room.objects.get(category=cat, room_number=room_no)
        except:
            messages.error(request, f"{category} and {room_no} number don't match")
            return redirect('control_page')
        if room.status == 'v':
            if action == 'o' and check_in_date == '':
                messages.error(request, "Action don't match date")
                return redirect('control_page')
            if action == 'b' and book_date == '':
                messages.error(request, "Action don't match date")
                return redirect('control_page')

            room.category = cat
            room.status = action
            room.occupant = user
            
            customer = Customer.objects.get(user_link=user)
            customer.room = room
            customer.is_active = True
            customer.book_date = book_date
            customer.check_in_date = check_in_date
            room.save()
            customer.save()

            messages.success(request, 'Action Successful')
            return redirect('control_page')
        else:
            messages.error(request, 'Room not vacant')
            return redirect('control_page')
    
    # Book Hall
    if request.method == 'POST' and request.POST.get('check3') == 'book_hall':
        hall = request.POST.get('hall')
        hall = Hall.objects.get(hall=hall)
        username = request.POST.get('username')
        date = request.POST.get('date')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User Does Not Exist')
            return redirect('control_page')
        customer = Customer.objects.get(user_link=user)
        customer.hall = hall
        customer.hall_status = True
        book_hall = HallBook(
            hall=hall, customer=customer, book_date=date
        )
        book_hall.save()
        customer.save()
        messages.success(request, f'{hall} Booked Successfully')

    # Reg Gym
    if request.method == 'POST' and request.POST.get('check4') == 'reg_gym':
        username = request.POST.get('username').lower()
        mem_grp = request.POST.get('mem_grp')
        trainer = request.POST.get('trainer')
        sub_duration = request.POST.get('sub_duration')
        start_date = request.POST.get('start_date')
        if start_date == '':
            messages.error(request, 'Enter Start Date')
            return redirect('control_page')
        try:
            user = User.objects.get(username=username)
            customer = Customer.objects.get(user_link=user)
        except:
            messages.error(request, 'User Does Not Exist')
            return redirect('control_page')

        gym_user = GymUser(
            membership_group=mem_grp,
            trainer=trainer,
            customer=customer,
            subscription=sub_duration,
            start_date=start_date
        )
        gym_user.save()
        customer.gym_status = True
        customer.save()

        messages.success(request, 'Registration Complete')
        return redirect('control_page')

    customers = Customer.objects.exclude(full_name='Tafida')
    rooms = Room.objects.exclude(room_number='001')
    gym_users = GymUser.objects.all()
    admin = User.objects.get(username='admin')
    room_001 = Room.objects.get(room_number='001')
    hall_0 = Hall.objects.get(hall='Hall-0')
    shall_books = HallBook.objects.filter(hall=Hall.objects.get(hall='Small Hall'))
    mhall_books = HallBook.objects.filter(hall=Hall.objects.get(hall='Medium Hall'))
    lhall_books = HallBook.objects.filter(hall=Hall.objects.get(hall='Large Hall'))
    context = {'rooms': rooms, 'gym_users': gym_users, 'admin': admin, 'customers': customers, 'room_001': room_001, 'hall_0':hall_0, 'shall_books': shall_books, 'mhall_books': mhall_books, 'lhall_books': lhall_books, 'user_form': user_form, 'group': group}
    return render(request, 'base/control_page.html', context)

def checkout(request, room_num):
    staff = request.user
    role = staff.groups.all()[0].name
    if role == 'staff':
        room = Room.objects.get(room_number=room_num)
        if room.status == 'b' or room.status == 'o':
            room.status = 'v'
            room.occupant = User.objects.get(username='admin')
            try:
                user = Customer.objects.get(room=room)
                user.room = Room.objects.get(room_number='001')
                user.is_active = False
                user.save()
                room.save()
            except:
                pass
            
            messages.success(request, f'{room} checked out successfully')
            return redirect('control_page')
        else:
            messages.success(request, f'{room} is vacant')
            return redirect('control_page')
    else:
        messages.success(request, "You Don't Have Permission to Perform this Action")
        return redirect('home_page')

def user_page(request):
    group = show_control(request)
    user = request.user
    customer = Customer.objects.get(user_link=user)
    try:
        room = Room.objects.get(occupant=user)
    except:
        room = None
    try:
        gym_user = GymUser.objects.get(customer=customer)
    except:
        gym_user = None
    try:
        hall_book = HallBook.objects.get(customer=customer)
    except:
        hall_book = None
    context = {'user': user, 'customer': customer, 'room': room, 'gym_user': gym_user, 'hall_book': hall_book, 'group': group}
    return render(request, 'base/user_page.html', context)

def user_page2(request, name):
    staff = request.user
    role = staff.groups.all()[0].name
    if role == 'staff':
        try:
            customer = Customer.objects.get(full_name=name)
            user = customer.user_link
        except:
            user = User.objects.get(username=name)
            customer = Customer.objects.get(user_link=user)
        try:
            room = Room.objects.get(occupant=user)
        except:
            room = None
        try:
            gym_user = GymUser.objects.get(customer=customer)
        except:
            gym_user = None
        try:
            hall_book = HallBook.objects.get(customer=customer)
        except:
            hall_book = None
            # customer = Customer.objects.get(full_name='Tafida')
            # hall_book = HallBook.objects.get(customer=customer)
        group = show_control(request)
        context = {'user': user, 'customer': customer, 'room': room, 'gym_user': gym_user, 'hall_book': hall_book, 'group': group}
        return render(request, 'base/user_page2.html', context)
    else:
        messages.success(request, "You Don't Have Permission to View This Page")
        return redirect('home_page')

def checkin(request, name):
    staff = request.user
    role = staff.groups.all()[0].name
    if role == 'staff':
        user = User.objects.get(username=name)
        customer = Customer.objects.get(user_link=user)
        customer.check_in_date = dt.date.today()
        room = Room.objects.get(occupant=user)
        room.status = 'o'
        customer.save()
        room.save()
        return redirect('control_page')
    else:
        messages.success(request, "You Don't Have Permission to View This Page")
        return redirect('home_page')
