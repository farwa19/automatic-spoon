from django.shortcuts import render
from django.conf import settings
from .models import MedicalCondition, Name, Doct, Tests,Review
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden
from .forms import DocumentUploadForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.db.models import Q
from django.urls import reverse
from django.shortcuts import redirect
from django.core.files.storage import default_storage
# views.py
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt # Or use standard CSRF protection

@csrf_exempt
def check_username(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get('username', '')
            print(f"Checking username: {username}")  # Debugging

            # Check if user exists in standard Django User model
            if Name.objects.filter(username=username).exists():
                return JsonResponse({'exists': True})
            else:
                return JsonResponse({'exists': False})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=400)
def home(request):
    return render(request, 'myapp/index.html')
def login_view(request):
    doctors = Doct.objects.all()
    context = {
        'doctors': doctors
    }
    return render(request, "myapp/login.html", context)

    return render(request, "myapp/login.html")
# views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os


# Function to verify a password
def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password)


@csrf_exempt
def upload_audio(request):
    print("lllllll")
    if request.method == "POST":

        email = request.POST.get("email")
        password= request.POST.get("password")
        ha = hash_password(password)
        print(ha)
        name = request.POST.get("name")
        nae = request.POST.get("doct")
        print(nae,"farea")
        print(email,"jjjjjjj")
        user = Name.objects.create_user(
            username=name,
            email=email,
            password=password,
            specialization=nae,
            role=Name.PATIENT,
        )
        user_id = user.id
        print(user_id, "savedjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj")

        audio_file = request.FILES.get("audio_file")

        if audio_file:
            # Define the save directory
            save_dir = os.path.join(settings.MEDIA_ROOT, "audio")  # Use MEDIA_ROOT for user-uploaded files
            os.makedirs(save_dir, exist_ok=True)  # Create the directory if it doesn't exist

            # Generate a unique filename
            filename = f"recording_{user_id}.wav"  # Example: recording_1a2b3c4d.wav
            save_path = os.path.join(save_dir, filename)

            # Save the file
            with open(save_path, "wb+") as destination:
                for chunk in audio_file.chunks():
                    destination.write(chunk)

            print(f"File saved to: {save_path}")
        document_file = request.FILES.get("document_file")
        new_test = Tests.objects.create(
        patient=user,
        audio=audio_file,  # Handle uploaded audio file
        report_file=document_file)
        print('jkdonemmmmmmmmmmmmm')

        if document_file:
            # Define the directory to save the file
            save_dir = os.path.join(settings.MEDIA_ROOT, "documents")
            os.makedirs(save_dir, exist_ok=True)  # Create the directory if it doesn't exist

            # Generate a unique filename
            filename = f"document_{user_id}_{document_file.name}"  # Example: document_john@example.com_file.pdf
            save_path = os.path.join(save_dir, filename)

            # Save the file to the server
            with open(save_path, "wb+") as destination:
                for chunk in document_file.chunks():
                    destination.write(chunk)

            print(f"File saved to: {save_path}")
            # Save other form data (e.g., name and email) to the database
            # Example: YourModel.objects.create(name=name, email=email, audio_file=save_path)

            return JsonResponse({"status": "success", "message": "Form submitted successfully."})
        else:
            return JsonResponse({"status": "error", "message": "No audio file provided."}, status=400)

    return JsonResponse({"status": "error", "message": "Invalid request method."}, status=405)
from django.shortcuts import render
from .forms import DocumentUploadForm

def upload_document(request):
    if request.method == 'POST':
        form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Handle form processing here
            pass
    else:
        form = DocumentUploadForm()

    return render(request, 'your_template.html', {'form': form})
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("home"))
from django.contrib.auth.models import User  # Ensure you import the correct model

def user_login(request):
    if request.method == "POST":
        # Get username and password from request
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()




        # Authenticate user properly
        user = authenticate(request, username=username, password=password)


        print(f"🔹 Authenticated User: {user}")  # Debugging

        if user is not None:
            print(user.check_password(password))
            login(request, user)  # Corrected login function
            messages.success(request, "Welcome back! Login successful. (خوش آمدید)")
            return HttpResponseRedirect(reverse("home"))
        else:
            print("❌ Authentication failed: Incorrect password or user is inactive")
            messages.error(request, "Invalid username or password. (غلط پاس ورڈ)")
            return render(request, "myapp/have.html", {"message": "Incorrect password or user is inactive غلط پاس ورڈ ہے۔  "})

    return render(request, "myapp/have.html")
@login_required  # Ensures that only authenticated users can access this page
def page(request):
    user = request.user  # This gets the currently logged-in user


    username = user.username
    password = user.password
    print(username,password)
    hj = False
    tests = Tests.objects.filter(patient=user).first()
    if tests.area_of_pain == "Neck":
        hj = True



    context = {
            "test": tests,
        'kl':  user,

        "ty": hj,
        'j': False
              # Example of passing additional info
        }
    return render(request, "myapp/profile.html", context)

from django.shortcuts import render, get_object_or_404
from .models import Name, Tests, UploadedDocument

def patient_info(request, patient_id):
    patient = get_object_or_404(Name, id=patient_id, role=Name.PATIENT)
    if request.user.role != Name.DOCTOR or patient not in request.user.patients.all():
        return HttpResponseForbidden("You are not authorized to view this patient's information.")
    tests = Tests.objects.filter(patient=patient)
    documents = UploadedDocument.objects.filter(patient=patient)  # Assuming you add a ForeignKey to UploadedDocument
    context = {
        'patient': patient,
        'tests': tests,
        'documents': documents,
    }
    return render(request, 'patient_info.html', context)
@login_required
def patient(request):
    h = Doct.objects.all()
    for i in h:
        print(i,"doctor")
        print(i.patients.all(),"patients")

    user = request.user

    # Get the doctor profile associated with the current user
    try:
        doctor_profile = Doct.objects.get(user=request.user)
    except Doct.DoesNotExist:
        doctor_profile = None

    # Filter patients based on doctor profile
    if doctor_profile:
        # 1. Start with patients linked via the Admin (M2M)
        # 2. OR patients linked via a Test
        patients_list = Name.objects.filter(
            role="patient"
        ).filter(
            # Check BOTH relationships
            Q(doctor_profile=doctor_profile) | Q(tests__doctor=doctor_profile)
        ).filter(
            # Keep your treatment filter if you only want pending cases
            Q(tests__ilaj__exact="") | Q(tests__ilaj__isnull=True)
        ).distinct()
    else:
        patients_list = Name.objects.none()

    print(patients_list,"patients_list")

    context = {
        "tests": patients_list  # Pass the tests to the template
    }
    return render(request, "myapp/kl.html", context)


def save_file(file, new_name):
    if file:
        ext = os.path.splitext(file.name)[1]  # Get file extension
        filename = f"{new_name}{ext}"  # Rename file
        path = default_storage.save(f"uploads/{filename}", ContentFile(file.read()))  # Save file
        return path
    return None
@login_required
def new(request):
    name = request.POST["name"]
    selected_codes = request.POST.getlist('past_history')



        # 2. Get the single Doctor ID selected
    doctor_id = request.POST.get('doctor')

    password = request.POST["password"]
    email = request.POST["email"]
    full_name = request.POST["full_name"]
    age = request.POST["age"]
    sex = request.POST["sex"]
    profession = request.POST["profession"]
    address = request.POST["address"]
    interval = request.POST["interval"]
    print(name, password, email, full_name)
    user = Name.objects.create_user(
        username=name,
        email=email,
        password=password,
        full_name=full_name,
        age=age,
        sex=sex,
        profession=profession,
        address=address,
        role=Name.PATIENT,
    )
    print("created")

    area_of_pain = request.POST["area_of_pain"]
    cause_of_pain = request.POST["cause_of_pain"]
    aggravation = request.POST["aggravation"]
    relief = request.POST["relief"]
    numbness = request.POST["numbness"]
    walking_tolerance = request.POST["walking_tolerance"]
    trouble = request.POST["trouble"]
    support = request.POST["support"]
    if support == "yes":
        support = True
    else:
        support = False



    if area_of_pain == "neck":

        grip = request.POST["grip"]
    else:
        grip = 00



            # If strictly one doctor per patient record (ForeignKey):

    audio_file = request.FILES.get("audio_file")
    mri = request.FILES.get("Mri")
    mri = save_file(mri, f'{user.id}mri')
    Xrays = request.FILES.get("Xrays")
    Xrays= save_file(Xrays, f'{user.id}Xrays')
    Blood = request.FILES.get("Blood")
    Blood= save_file(Blood, f'{user.id}blood')
    ct = request.FILES.get("ct")
    ct= save_file(ct, f'{user.id}ct')
    neck_pain_severity = request.POST.get("neck_pain_severity", 0)
    arm_pain_severity = request.POST.get("arm_pain_severity", 0)
    new_test = Tests.objects.create(
        patient=user,
        doctor = get_object_or_404(Doct, id=doctor_id) if doctor_id else None,


         cause_of_pain = cause_of_pain,
         area_of_pain= area_of_pain,
         aggravation= aggravation,
         pain_trouble=trouble,
         neckPain = neck_pain_severity,
            armPain = arm_pain_severity,
            neckpain_inteference = request.POST.get("interfere"),
            living_with_pain = request.POST.get("feeling"),
            quality_of_life = request.POST.get("quality_of_life"),
            cutdownactivities = request.POST.get("cutdown"),
            neck_problems_work_leave = 3,



         relief = relief,
         numbness = numbness,
         walking_tolerance= walking_tolerance,
         support = support,

         grip = grip,
         examination= interval,
        audio=audio_file,
          # Handle uploaded audio file
        report_file=mri,
        Bloodtest = Blood,
        xray = Xrays,
        ctscan = ct

        )
    selected_codes = request.POST.getlist('past_history')


    if 'none' in selected_codes:
        selected_codes.remove('none')

    # 2. Only run the database query if there are items left
    if selected_codes:
        conditions = MedicalCondition.objects.filter(name__in=selected_codes)
        new_test.past_history.set(conditions)

        # --- 7. AUTHENTICATE AND LOGIN ---
    user_auth = authenticate(request, username=name, password=password)
    if user_auth is not None:
        login(request, user_auth) # Actually logs the user in
        return render(request, 'myapp/index.html')
# views.py example
def add_review(request, doctor_id):
    # Only allow POST from authenticated users and allow one review per user per doctor
    if request.method == "POST" and request.user.is_authenticated:
        doctor = get_object_or_404(Doct, id=doctor_id)

        # Prevent a user from adding more than one review for the same doctor
        if Review.objects.filter(doctor=doctor, user=request.user).exists():
            messages.error(request, "You have already posted a review for this doctor.")
            return redirect('doctor_profile', doctor_id=doctor_id)

        rating = request.POST.get('rating')
        comment = request.POST.get('comment')

        Review.objects.create(
            doctor=doctor,
            user=request.user,
            rating=rating,
            comment=comment
        )
        # Recalculate average rating here if not done via signals
        return redirect('doctor_profile', doctor_id=doctor_id)
def doctor_profile(request, doctor_id):
    doctor = get_object_or_404(Doct, id=doctor_id)
    doctor = get_object_or_404(Doct, id=doctor_id)
    reviews = doctor.reviews.all().order_by('-created_at')

    # 1. Get Real Patient Count (Dynamic)
    # This counts the actual users in the ManyToMany field
    from django.db.models import Q


    actual_patient_count = Name.objects.filter(
        role="patient"
    ).filter(
        Q(doctors=doctor) | Q(tests__doctor=doctor)
    ).filter(
        Q(tests__ilaj__isnull=False) & ~Q(tests__ilaj__exact="")
    ).distinct().count()
    print(actual_patient_count, "actual_patient_count")

    # 2. Rating Breakdown Logic (From previous step)
    star_breakdown = []
    rating_counts = doctor.get_rating_counts()
    for star in range(5, 0, -1):
        star_breakdown.append({
            'stars': star,
            'percentage': doctor.get_rating_percentage(star),
            'count': rating_counts[star]
        })

    context = {
        'doctor': doctor,
        'reviews': reviews,
        'star_breakdown': star_breakdown,
        'patient_count': actual_patient_count, # Pass the real count here
    }
    return render(request, 'myapp/doctors.html', context)
    return render(request, 'myapp/doctors.html', context)
def doctors(request):
    doctors = doctors = Doct.objects.all()
    print(doctors,"doctors")
    context = {
        "doctors": doctors  # Pass the tests to the template
            # Example of passing additional info
    }
    return render(request, "myapp/doct.html", context)
def more_info(request, id):
    use = True
    patient = get_object_or_404(Name, id=id)
    print(patient)
    test = Tests.objects.filter(patient=patient).first()

    hj = False
    if test:
        print(test.audio,'l')
    else:
        print("No test found.")
    if test.area_of_pain != None:
        if test.area_of_pain == "Neck":
            hj = True

    if test.ilaj == None:
        use = False

    else:
        use = True




    context = {
            "test": test,
        'kl':  patient,
        "ty": hj,
        'j': use
              # Example of passing additional info
        }
    return render(request, "myapp/profile.html", context)
    # Process the ID and return a response
from django.shortcuts import render, redirect, get_object_or_404
from .models import Name, Tests  # Ensure these are imported

@login_required
def addquestion(request):
    if request.method == "POST":
        user_id = request.POST.get("user_id")
        patient = get_object_or_404(Name, id=user_id)

        # Verify user is either the patient or their doctor
        if request.user.id != patient.id and request.user.role != Name.DOCTOR:
            print(f"Unauthorized access attempt by user {request.user.id} for patient {patient.id}")
            return HttpResponseForbidden("Unauthorized")

        # Get the patient's test record
        test = Tests.objects.filter(patient=patient).first()

        if not test:
            return HttpResponseForbidden("Test record not found")

        # Check which question number was submitted and save accordingly
        num = request.POST.get("num")  # This gets '1', '2', or '3'

        if num == "1":
            test.addquestion1 = request.POST.get("extraquestion1")
        elif num == "2":
            test.addquestion2 = request.POST.get("extraquestion2")
        elif num == "3":
            test.addquestion3 = request.POST.get("extraquestion3")

        test.save()
        print(f"Saved Question {num} for {patient.full_name}")

        # Redirect back to the dashboard or patient list
        # using 'HTTP_REFERER' sends them back to the exact same page they were on
        return redirect(request.META.get('HTTP_REFERER', 'patient'))
def save_answer(request):
    if request.method == "POST":
        # 1. Identify the logged-in patient
        # Assuming your 'Name' model is linked to the logged-in user via email or a OneToOneField
        # If 'Name' IS your user model, you can just use request.user.id

        try:

            patient = Name.objects.get(email=request.user.email)

            # OR if you are passing user_id in the form (add <input type="hidden" name="user_id" value="{{ kl.id }}"> to the patient form if needed)
            # patient = get_object_or_404(Name, id=request.POST.get("user_id"))

            test = Tests.objects.filter(patient=patient).first()
        except Name.DoesNotExist:
            print("Patient not found")
            return redirect('home')

        # 2. Get the question number and the answer text
        q_num = request.POST.get("question_num")

        if test:
            if q_num == "1":
                test.addanswer1 = request.POST.get("answer1")
            elif q_num == "2":
                test.addanswer2 = request.POST.get("answer2")
            elif q_num == "3":
                test.addanswer3 = request.POST.get("answer3")
            test.save()
            print(f"Saved Answer {q_num} for {patient.full_name}")

        # Redirect patient back to their home dashboard
        return redirect('more_info', id=patient.id)
def add(request):
    if request.method == "POST":
        user = request.POST["user_id"]
        ilaj = request.POST["ilaj"]
        patient = get_object_or_404(Name, id=user)
        test = Tests.objects.filter(patient=patient).first()
        test.ilaj = ilaj
        test.save()
        print("saved")
        print(test.ilaj,ilaj,"issame")
        return redirect('patient')

@csrf_exempt  # Disable CSRF protection for testing (use proper security in production)
def submit_email(request):
    if request.method == 'POST':
        data = json.loads(request.body)  # Parse JSON request body
        email = data.get('email')  # Extract 'email' value
        print("Received email:", email)  # Debugging
        if Name.objects.filter(email__iexact=email).exists():
            kl = True
        else:
            kl = False


        return JsonResponse({"message": "Email received", "email": kl})

    return JsonResponse({"error": "Invalid request"}, status=400)
