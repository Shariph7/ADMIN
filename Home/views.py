from django.shortcuts import render, redirect, redirect, get_object_or_404
from functools import wraps
from Home.models import SignupData, Events, Students
from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password

# Custom login_required decorator using session
def login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('logged_in'):
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper

# Home page
def index(request):
    return render(request, "index.html")

# User signup view
def signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        hashed_password = make_password(password)
        try:
            new_user = SignupData(
                username=username,
                email=email,
                password=hashed_password
            )
            new_user.save()
            messages.success(request, "Your account has been registered!")
            return redirect("login")
        except Exception as e:
            messages.error(request, "An error occurred while registering your account. Please try again.")
            print(f"Signup error: {e}")
    return render(request, "Signup.html")

# User login view
def login(request):
    if request.session.get('logged_in'):
        return redirect("index")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            user_instance = SignupData.objects.get(username=username)

            if check_password(password, user_instance.password):
                request.session['logged_in'] = True
                request.session['username'] = user_instance.username
                messages.success(request, "Login Successful")
                return redirect("index")
            else:
                messages.error(request, "Invalid Password!")
        except SignupData.DoesNotExist:
            messages.error(request, "User does not exist. Please try again.")
    return render(request, "login.html")

@login_required
def adminpage(request):
    username = request.session.get('username')
    user = SignupData.objects.get(username=username)

    query_class = request.GET.get("for_class")
    query_academic = request.GET.get("academic")
    class_list = ["Nursery", "LKG", "UKG", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]

    if request.method == "POST" and "Delete_Event" in request.POST:
        event_id = request.POST.get("Delete_Event")
        event = get_object_or_404(Events, id=event_id, user=user)
        event.delete()
        return redirect("adminpage")

    items = Events.objects.filter(user=user)

    if query_class:
        items = items.filter(for_class__icontains=query_class)
    if query_academic:
        items = items.filter(academic_year=query_academic)

    return render(request, "adminpage.html", {
        'items': items,
        'class_list': class_list,
        'query_academic': query_academic,
        'query_class': query_class,
        "username": username
    })

# Logout view
def logout(request):
    request.session.flush()
    messages.info(request, "You have been logged out.")
    return redirect('/')

@login_required
def createEvent(request):
    if request.method == "POST":
        event = request.POST.get("event")
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")
        type = request.POST.get("type")
        start_time = request.POST.get("start_time")
        end_time = request.POST.get("end_time")
        venue = request.POST.get("venue")
        Money = request.POST.get("Money")
        for_class = ", ".join(request.POST.getlist("for_class"))
        description = request.POST.get("description")

        # 🔑 Get the currently logged-in user
        username = request.session.get('username')
        user = SignupData.objects.get(username=username)

        events = Events(
            user=user,
            event=event,
            start_date=start_date,
            end_date=end_date,
            type=type,
            start_time=start_time,
            end_time=end_time,
            Money=Money,
            venue=venue,
            for_class=for_class,
            description=description
        )
        events.save()
        return redirect("adminpage")
    return render(request, "createEvent.html")

def student_register(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        middle_name = request.POST.get("middle_name", "")
        last_name = request.POST.get("last_name")
        dob = request.POST.get("dob")
        student_id = request.POST.get("student_id")
        password = request.POST.get("password")
        street = request.POST.get("street")
        city = request.POST.get("city")
        province = request.POST.get("province")
        district = request.POST.get("district")
        zip_code = request.POST.get("zip")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        class_level = request.POST.get("class_level", None)
        faculty = request.POST.get("faculty")
        comments = request.POST.get("comments", "")

        hashed_password = make_password(password)

        student_instance = Students(
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            dob=dob,
            student_id=student_id,
            password=hashed_password,
            street=street,
            city=city,
            province=province,
            district=district,
            zip=zip_code,
            email=email,
            phone=phone,
            class_level=class_level,
            faculty=faculty,
            comments=comments
        )
        student_instance.save()
        messages.success(request, "Student registered successfully!")
        return redirect('adminpage')
    
    return render(request, "student_register.html")
