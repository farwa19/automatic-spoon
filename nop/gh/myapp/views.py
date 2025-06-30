from django.shortcuts import render
from django.conf import settings
from .models import Name, Doct, Tests
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import DocumentUploadForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.db.models import Q
from django.urls import reverse
from django.shortcuts import redirect
from django.core.files.storage import default_storage

def home(request):
    return render(request, 'myapp/index.html')
def login_view(request):
    
    return render(request, "myapp/login.html")
# views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os

import bcrypt

# Function to hash a password
def hash_password(plain_password):
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(plain_password.encode('utf-8'), salt)
    return hashed_password

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
        user = Name.objects.create_user(username=name, email=email, password=password, specialization=nae)
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
        
        user = Name.objects.filter(username=username).first()

        print(f"🔹 Username: {username}, Password: {password}")
        print(user.check_password(password))

        # Authenticate user properly
        user = authenticate(request, username=username, password=password)

        print(f"🔹 Authenticated User: {user}")  # Debugging

        if user is not None:
            login(request, user)  # Corrected login function
            return HttpResponseRedirect(reverse("home"))
        else:
            print("❌ Authentication failed: Incorrect password or user is inactive")
            return render(request, "myapp/have.html", {"message": "Invalid credentials."})
    
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
def patient(request):
    user = request.user 
    
    
    
    tests = Name.objects.filter(role="patient").filter(
    Q(tests__ilaj__exact="") | Q(tests__ilaj__isnull=True)
).distinct()

    print(tests)


    

    context = {
        "tests": tests  # Pass the tests to the template
            # Example of passing additional info
    }
    return render(request, "myapp/kl.html", context)


def save_file(file, new_name):
    if file:
        ext = os.path.splitext(file.name)[1]  # Get file extension
        filename = f"{new_name}{ext}"  # Rename file
        path = default_storage.save(f"uploads/{filename}", ContentFile(file.read()))  # Save file
        return path
    return None
def new(request):
    name = request.POST["name"]
    password = request.POST["password"]
    email = request.POST["email"]
    full_name = request.POST["full_name"]
    age = request.POST["age"]
    sex = request.POST["sex"]
    profession = request.POST["profession"]
    address = request.POST["address"]
    user = Name.objects.create_user(username=name, 
    email=email, 
    password=password,
    full_name=full_name,
    age=age,
    sex= sex,
    profession=profession,
    address=address)
    print("created")
    past_history = request.POST["past_history"]
    area_of_pain = request.POST["area_of_pain"]
    cause_of_pain = request.POST["cause_of_pain"]
    aggravation = request.POST["aggravation"]
    relief = request.POST["relief"]
    numbness = request.POST["numbness"]
    walking_tolerance = request.POST["walking_tolerance"]
    support = request.POST["support"]
    if support == "yes":
        support = True
    else:
        support = False


    urine_control = request.POST["urine_control"]
    if urine_control == "yes":
        urine_control = True
    else:
        urine_control = False

    grip = request.POST["grip"]
    if grip == "'Open this select menu'":
        grip = 00
    


    audio_file = request.FILES.get("audio_file")
    mri = request.FILES.get("Mri")
    mri = save_file(mri, f'{user.id}mri')
    Xrays = request.FILES.get("Xrays")
    Xrays= save_file(Xrays, f'{user.id}Xrays')
    Blood = request.FILES.get("Blood")
    Blood= save_file(Blood, f'{user.id}blood')
    ct = request.FILES.get("ct")
    ct= save_file(ct, f'{user.id}ct')
    new_test = Tests.objects.create(
        patient=user,
         past_history = past_history,
         cause_of_pain = cause_of_pain,
         area_of_pain= area_of_pain,
         aggravation= aggravation,
         relief = relief,
         numbness = numbness,
         walking_tolerance= walking_tolerance,
         support = support,
         urine_control = urine_control,
         grip = grip,
        audio=audio_file,
          # Handle uploaded audio file
        report_file=mri,
        Bloodtest = Blood,
        xray = Xrays,
        ctscan = ct

        )
    return render(request, 'myapp/index.html')
    
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
            kl = False
        else:
            kl = True

        
        return JsonResponse({"message": "Email received", "email": kl})

    return JsonResponse({"error": "Invalid request"}, status=400)