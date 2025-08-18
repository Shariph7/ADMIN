from django.shortcuts import render, redirect, get_object_or_404
from functools import wraps
from Home.models import SignupData, Events, Students
from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password
import openpyxl
from datetime import datetime
from django.db.models import Count

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
            new_user = SignupData(username=username, email=email, password=hashed_password)
            new_user.save()
            messages.success(request, "Your account has been registered!")
            return redirect("login")
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
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
            messages.error(request, "User does not exist.")
    return render(request, "login.html")

@login_required
def adminpage(request):
    username = request.session.get('username')
    user = SignupData.objects.get(username=username)

    query_class = request.GET.get("for_class")
    query_academic = request.GET.get("academic")
    class_list = ["Nursery", "LKG", "UKG"] + [str(i) for i in range(1, 13)]

    # Delete Event
    if request.method == "POST" and "Delete_Event" in request.POST:
        event_id = request.POST.get("Delete_Event")
        event = get_object_or_404(Events, id=event_id, user=user)
        event.delete()
        return redirect("adminpage")

    # Bulk Excel Upload
    if request.method == "POST" and "excel_file" in request.FILES:
        excel_file = request.FILES["excel_file"]
        try:
            wb = openpyxl.load_workbook(excel_file)
            sheet = wb.active
            for row in sheet.iter_rows(min_row=2, values_only=True):
                Students.objects.create(
                    first_name=row[0] or "",
                    middle_name=row[1] or "",
                    last_name=row[2] or "",
                    dob=row[3] or None,
                    student_id=row[4] or "",
                    password=make_password(row[5]) if row[5] else make_password("default123"),
                    street=row[6] or "",
                    city=row[7] or "",
                    province=row[8] or "",
                    district=row[9] or "",
                    zip=row[10] or "",
                    email=row[11] or "",
                    phone=row[12] or "",
                    class_level=int(row[13]) if row[13] else None,
                    faculty=row[14] or "",
                    comments=row[15] or ""
                )
            messages.success(request, "Excel file uploaded successfully!")
        except Exception as e:
            messages.error(request, f"Error uploading file: {e}")
        return redirect("adminpage")

    # Filter Events
    items = Events.objects.filter(user=user).annotate(
        total_registrations=Count('bookings')
    )
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
        username = request.session.get('username')
        user = SignupData.objects.get(username=username)

        # Parse time strings into time objects
        start_time_str = request.POST.get("start_time")
        end_time_str = request.POST.get("end_time")
        start_time = datetime.strptime(start_time_str, "%H:%M").time() if start_time_str else None
        end_time = datetime.strptime(end_time_str, "%H:%M").time() if end_time_str else None

        event = Events(
            user=user,
            event=request.POST.get("event"),
            start_date=request.POST.get("start_date"),
            end_date=request.POST.get("end_date"),
            type=request.POST.get("type"),
            start_time=start_time,
            end_time=end_time,
            available=request.POST.get("available"),
            Money=request.POST.get("Money"),
            venue=request.POST.get("venue"),
            for_class=", ".join(request.POST.getlist("for_class")),
            description=request.POST.get("description")
        )
        event.save()
        return redirect("adminpage")
    return render(request, "createEvent.html")

def student_register(request):
    if request.method == "POST":
        hashed_password = make_password(request.POST.get("password"))
        student_instance = Students(
            first_name=request.POST.get("first_name"),
            middle_name=request.POST.get("middle_name", ""),
            last_name=request.POST.get("last_name"),
            dob=request.POST.get("dob"),
            student_id=request.POST.get("student_id"),
            password=hashed_password,
            street=request.POST.get("street"),
            city=request.POST.get("city"),
            province=request.POST.get("province"),
            district=request.POST.get("district"),
            zip=request.POST.get("zip"),
            email=request.POST.get("email"),
            phone=request.POST.get("phone"),
            class_level=int(request.POST.get("class_level")) if request.POST.get("class_level") else None,
            faculty=request.POST.get("faculty"),
            comments=request.POST.get("comments", "")
        )
        student_instance.save()
        messages.success(request, "Student registered successfully!")
        return redirect('adminpage')
    return render(request, "student_register.html")