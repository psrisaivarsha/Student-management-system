from django.shortcuts import render, redirect, get_object_or_404
from myapp.forms import StudentForm
from myapp.models import Student, Profile
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User

# 🔐 Auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


# 🏠 HOME
def home(request):
    return render(request, 'myapp/home.html')


# 🔐 LOGIN
def login_view(request):
    error = None

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # ✅ ensure profile exists
            Profile.objects.get_or_create(
                user=user,
                defaults={'role': 'student'}
            )

            return redirect('students')
        else:
            error = "Invalid username or password"

    return render(request, 'myapp/login.html', {'error': error})


# 🔐 LOGOUT
def logout_view(request):
    logout(request)
    return redirect('login')


# 👨‍🎓 STUDENTS LIST
from django.db.models import Q



@login_required(login_url='login')
def getStudents(request):
    user = request.user

    profile, _ = Profile.objects.get_or_create(
        user=user,
        defaults={'role': 'student'}
    )

    # 🔹 TEACHER → no search
    if profile.role == 'teacher':
        students = Student.objects.all()
        query = ''

    # 🔹 STUDENT → live search
    else:
        students = Student.objects.filter(user=user)

        query = request.GET.get('q', '').strip()

        if query:
            students = students.filter(
                Q(stuName__icontains=query) |
                Q(stuId__icontains=query)
            )

    return render(request, 'myapp/student.html', {
        'studs': students,
        'query': query,
        'role': profile.role
    })

# ➕ REGISTER STUDENT
@login_required(login_url='login')
def registerStudent(request):
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)

        if form.is_valid():
            student = form.save(commit=False)
            student.user = request.user
            student.save()

            if student.stuEmail:
                send_mail(
                    'Registration Successful',
                    'Thank you for registering',
                    settings.EMAIL_HOST_USER,
                    [student.stuEmail],
                    fail_silently=True,
                )

            return redirect('students')

    else:
        form = StudentForm()

    return render(request, 'myapp/register.html', {'form': form})


# 🔍 VIEW STUDENT
@login_required(login_url='login')
def getStudent(request, id):
    student = get_object_or_404(Student, id=id)
    return render(request, 'myapp/find.html', {'student': student})


# ✏️ EDIT STUDENT
@login_required(login_url='login')
def editStudent(request, id):
    student = get_object_or_404(Student, id=id)

    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            return redirect('students')
    else:
        form = StudentForm(instance=student)

    return render(request, 'myapp/edit.html', {'form': form})


# ❌ DELETE STUDENT
@login_required(login_url='login')
def deleteStudent(request, id):
    student = get_object_or_404(Student, id=id)

    if request.method == 'POST':
        student.delete()
        return redirect('students')

    return render(request, 'myapp/delete.html', {'del': student})


# 🖼️ UPLOAD IMAGE
@login_required(login_url='login')
def upload_image(request, id):
    student = get_object_or_404(Student, id=id)

    if request.method == "POST":
        if 'photo' in request.FILES:
            student.photo = request.FILES['photo']
            student.save()
        return redirect('students')

    return render(request, 'myapp/image.html', {'student': student})


# 📊 DASHBOARD (FINAL FIXED)
@login_required(login_url='login')
def dashboard(request):
    students = Student.objects.all()

    total_students = students.count()

    avg_marks = 0
    top_score = 0
    pass_percent = 0

    if total_students > 0:
        marks_list = [s.stuMarks for s in students]

        total_marks = sum(marks_list)
        avg_marks = total_marks // total_students

        top_score = max(marks_list)

        passed = len([m for m in marks_list if m >= 35])
        pass_percent = round((passed / total_students) * 100, 2)

    return render(request, 'myapp/dashboard.html', {
        'studs': students,
        'total_students': total_students,
        'avg_marks': avg_marks,
        'top_score': top_score,
        'pass_percent': pass_percent,
    })
# 📝 SIGNUP
# 📝 SIGNUP
def signup_view(request):
    error = None

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')   # ✅ added
        role = request.POST.get('role') or 'student'  # ✅ safe default

        # check if user already exists
        if User.objects.filter(username=username).exists():
            error = "Username already exists"
        else:
            # create user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )

            # create profile safely
            Profile.objects.get_or_create(
                user=user,
                defaults={'role': role}
            )

            # ✅ SEND EMAIL
            if email:
                send_mail(
                    subject="Account Created Successfully",
                    message=f"Hi {username}, your account has been created successfully.",
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[email],
                    fail_silently=False,   # show error if email fails
                )

            return redirect('login')

    return render(request, 'myapp/signup.html', {'error': error})