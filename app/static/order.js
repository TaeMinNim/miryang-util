const createGroupBtn = document.getElementById("create-group");
const groupForm = document.getElementById("group-form");

function showGroupForm(){
    groupForm.classList.toggle("hidden");
}

createGroupBtn.addEventListener("click", showGroupForm);