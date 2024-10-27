function updateFields() {
    const userType = document.getElementById("userType").value;
    const usernameInput = document.getElementById("usernameInput");
    

    if (userType === "student") {
        usernameInput.placeholder = "Admission Number:";
    } else if (userType === "faculty") {
        usernameInput.placeholder = "Email";
        departmentField.style.display = "block";  // Show department field for faculty
    } else {
        departmentField.style.display = "none";  // Hide department if no role is selected
    }
}