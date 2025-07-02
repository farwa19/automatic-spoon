var currentTab = 0; // Current tab index (starting at 0)
var jk = false; // Flag for "Neck" selection
var x = []; // Array to hold tab elements
console.log("jj");

console.log("farwa");
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/; 
    return emailRegex.test(email);
}
document.addEventListener("DOMContentLoaded", function () {
    x = document.getElementsByClassName("tab"); // Initialize tabs after DOM loads
    console.log("Tabs loaded:", x);

    if (x.length > 0) {
        showTab(currentTab); // Show the first tab
    } else {
        console.error("No tabs found!");
    }
});
(() => {
    'use strict'
  
    // Fetch all the forms we want to apply custom Bootstrap validation styles to
    const forms = document.querySelectorAll('.needs-validation')
  
    // Loop over them and prevent submission
    Array.from(forms).forEach(form => {
      form.addEventListener('submit', event => {
        if (!form.checkValidity()) {
          event.preventDefault()
          event.stopPropagation()
        }
  
        form.classList.add('was-validated')
      }, false)
    })
  })()
// ✅ Function to Show the Current Tab
function showTab(n) {
    console.log("Showing tab:", n);

    if (!x || x.length === 0) {
        console.error("Tabs are not loaded!");
        return;
    }
    
    if (n!= 10) {
        neckSection.style.display = "none";
        
    }

    // Hide all tabs first
    for (let i = 0; i < x.length; i++) {
        x[i].style.display = "none";
    }

    // Display the selected tab
    x[n].style.display = "block";
    console.log(x[n])

    // Handle Previous Button Visibility
    document.getElementById("prevBtn").style.display = (n === 0) ? "none" : "inline";

    // Handle Next Button Behavior
    if (n === x.length - 1) {
        document.getElementById("nextBtn").innerHTML = "Submit";
        document.getElementById("nextBtn").type = "submit"; // Form submission on the last step
    } else {
        document.getElementById("nextBtn").innerHTML = "Next";
        console.log(n)
        document.getElementById("nextBtn").type = "button"; // Ensures it's not submitting before the last step
    }

    // Fix Step Indicator
    fixStepIndicator(n);
}

// ✅ Function to Update Step Indicator
function fixStepIndicator(n) {
    let steps = document.getElementsByClassName("step");
    if (!steps || steps.length === 0) {
        console.error("No step indicators found!");
        return;
    }

    // Remove "active" class from all steps
    for (let i = 0; i < steps.length; i++) {
        steps[i].classList.remove("active");
    }

    // Add "active" class to the current step (if exists)
    if (steps[n]) {
        steps[n].classList.add("active");
    } else {
        console.error(`Step indicator for index ${n} not found!`);
    }
}

// ✅ Function to Handle Neck Selection Visibility
function handleAreaSelection(event) {
    console.log(event,"jhhj");
    const selectedValue = event.target.value;
    console.log("User selected:", selectedValue);

    const neckSection = document.getElementById("neckSection");
    if (neckSection) {
        neckSection.style.display = (selectedValue === "Neck") ? "block" : "none";
        jk = (selectedValue === "Neck");
    }
    console.log("jk:", jk);
}
async function checkemail() {
    const errorMessage = document.getElementById("errorMessage");
    if (currentTab === 0) {
        let gh = document.getElementsByName("email")[0];
        let emailValue = gh.value;
        let neo = isValidEmail(emailValue)
        if (!neo){
            
            errorMessage.textContent = "Write a valid email!";

            return false}
        else{errorMessage.textContent = "This email already exists!";}

        try {
            const response = await fetch('submit-email', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ email: emailValue })
            });
            
            const result = await response.json();
            console.log("Server Response:", result.email);
            
            // Return the boolean value directly
            return result.email !== false;
        } catch (error) {
            console.error("Error:", error);
            return false; // Return false if there's an error
        }
    }
    return true; // Default return if not tab 1
}
async function validateForm() {
    var x, y, i, d, valid = true;
    x = document.getElementsByClassName("tab");
    y = x[currentTab].getElementsByTagName("input");
    d = x[currentTab].getElementsByTagName("select");
    
    // Loop through inputs and validate
    for (i = 0; i < y.length; i++) {
        console.log( "valid")
        console.log( valid)
        if (y[i].value.trim() === "") {
            console.log("ji")
            if(currentTab == 5 && y[i].type === "file" ) {
                y[i].classList.add("invalid");
                valid = false;
                const errorrecord = document.getElementById("errorrecord");
                const urdu = document.getElementById("errorrecordurdu");
                errorrecord.style.display = "block";
                urdu.style.display = "block";


                console.log("record audio")}

            y[i].classList.add("invalid");
            valid = false;
        } else {
            y[i].classList.remove("invalid");
            const errorrecord = document.getElementById("errorrecord");
            const urdu = document.getElementById("errorrecordurdu");
            errorrecord.style.display = "none";
            urdu.style.display = "none";

            
            // Special email validation for tab 1
            if (currentTab == 0 && y[i].type === "email") {
                try {
                    console.log("Checking email validity...");
                    const ck = await checkemail();
                    if (!ck) {
                        y[i].classList.add("invalid");
                        
                        const errorMessage = document.getElementById("errorMessage");
                        
            
                        errorMessage.style.display = "block";
                        valid = false;
                        console.log("check")
                        console.log(valid)
                        console.log("done")
                    return false;
                    }
                    else{errorMessage.style.display = "none";
                        
                    }
                } catch (error) {
                    console.error("Email validation failed:", error);
                    y[i].classList.add("invalid");
                    valid = false;
                    
                }
            }
            
        }

        // Add event listener to remove "invalid" when user types
        y[i].addEventListener("input", function() {

            if(currentTab == 5 && y[i].type === "file" ) {
                y[i].classList.add("invalid");
                valid = false;
                errorrecord.style.display = "block";
                urdu.style.display = "block";


                console.log("record audio")}

            if (this.value.trim() !== "") {
                this.classList.remove("invalid");
            }
        });
    }

    // Loop through selects and validate
    for (i = 0; i < d.length; i++) {
        console.log( valid)
        if (d[i].value === "Open this select menu") {
            d[i].classList.add("invalid");
            valid = false;
        } else {
            d[i].classList.remove("invalid");
        }

        d[i].addEventListener("change", function() {
            if (this.value !== "Open this select menu") {
                this.classList.remove("invalid");
            }
        });
    }

    if (currentTab == 8) {
        return true;
    }

    if (valid) {
        document.getElementsByClassName("step")[currentTab].classList.add("finish");
    }
    return valid;
}

async function nextPrev(n) {
    if (n === 1 && !(await validateForm())) {
        console.log("Validation failed, stopping navigation.");
        return; // Stop navigation if validation fails
    }

    // Hide current tab
    x[currentTab].style.display = "none";

    // Change current tab
    currentTab += n;
    console.log("Current tab index:", currentTab);
    console.log("Total tabs:", x.length);

    // Ensure tab index is within range
    if (currentTab >= x.length) {
        

        document.getElementById("audioForm").submit();
        return false;
    }

    // Show the new tab
    showTab(currentTab);
}


// ✅ Prevents Scroll From Interfering With Form
document.addEventListener('wheel', function(event) {}, { passive: true });

// ✅ Audio Recording Logic
document.addEventListener("DOMContentLoaded", () => {
    let mediaRecorder;
    let audioChunks = [];

    const startBtn = document.getElementById("startBtn");
    const stopBtn = document.getElementById("stopBtn");
    const audioPlayback = document.getElementById("audioPlayback");
    const audioFileInput = document.getElementById("audioFile");
    const form = document.getElementById("audioForm");

    const requestMicrophoneAccess = async () => {
        try {
            console.log("Requesting microphone access...");
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            mediaRecorder = new MediaRecorder(stream);
            mediaRecorder.ondataavailable = (event) => audioChunks.push(event.data);
            mediaRecorder.onstop = processAudio;
        } catch (error) {
            console.error("Microphone access denied:", error);
            alert("Please allow microphone access to record audio.");
        }
    };

    const processAudio = () => {
        console.log("Recording stopped. Processing audio...");
        const audioBlob = new Blob(audioChunks, { type: "audio/wav" });
        
        console.log("Blob size:", audioBlob.size);
        console.log("Blob type:", audioBlob.type);
        
        audioPlayback.src = URL.createObjectURL(audioBlob);
        
        const audioFile = new File([audioBlob], "recording.wav", { type: "audio/wav" });
        
        // Create a new DataTransfer object and add the file
        const dataTransfer = new DataTransfer();
        dataTransfer.items.add(audioFile);
        
        // Assign the DataTransfer files to the input
        audioFileInput.files = dataTransfer.files;
        
        console.log("Audio file attached successfully.");
        console.log("Files in input after assignment:", audioFileInput.files);
    };

    startBtn.addEventListener("click", async () => {
        if (!mediaRecorder) await requestMicrophoneAccess();
        
        if (mediaRecorder) {
            audioChunks = [];
            mediaRecorder.start();
            startBtn.disabled = true;
            stopBtn.disabled = false;
            console.log("Recording started...");
        }
    });

    stopBtn.addEventListener("click", () => {
        if (mediaRecorder?.state === "recording") {
            console.log("Stopping recording...");
            mediaRecorder.stop();
            startBtn.disabled = false;
            stopBtn.disabled = true;
        }
    });

    form.addEventListener("submit", (event) => {
        if (!audioFileInput.files.length) {
            event.preventDefault();
            alert("Please record an audio file before submitting.");
        }
    });
});