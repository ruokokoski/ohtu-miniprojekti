function setCurrentYearAsMax(id) {
    var year = new Date().getFullYear();
    document.getElementById(id).setAttribute("max", year);
}

function searchTable(inputId, tableId, column) {
    // Declare variables
    var input, filter, table, tbody, tr, td, i, txtValue;
    input = document.getElementById(inputId);
    filter = input.value.toUpperCase();
    table = document.getElementById(tableId);
    tbody = table.getElementsByTagName("tbody")[0];
    tr = tbody.getElementsByTagName("tr");
  
    // Loop through all table rows, and hide those who don't match the search query
    for (i = 0; i < tr.length; i+=2) {
        td = tr[i].getElementsByTagName("td")[column];
        if (td) {
            txtValue = td.textContent || td.innerText;
            if (txtValue.toUpperCase().indexOf(filter) > -1) {
                tr[i].style.display = "";
            } else {
                tr[i].style.display = "none";
            }
        }
    }
}


function filterYear(inputId, tableId, column, min) {
    // Declare variables
    var input, filter, table, tbody, tr, td, i, year;
    input = document.getElementById(inputId);
    filter = input.value;
    table = document.getElementById(tableId);
    tbody = table.getElementsByTagName("tbody")[0];
    tr = tbody.getElementsByTagName("tr");
  
    // Loop through all table rows, and hide those who don't match the search query
    for (i = 0; i < tr.length; i+=2) { //jump over extrafields rows
        td = tr[i].getElementsByTagName("td")[column];
        if (td) {
            year = td.textContent || td.innerText;
            if (min) {
                if (Number(year) >= filter) {
                    tr[i].style.display = "";
                } else {
                    tr[i].style.display = "none";
                }
            } else {
                if (Number(year) <= filter) {
                    tr[i].style.display = "";
                } else {
                    tr[i].style.display = "none";
                }
            }
        }
    }
}

function show(id) {
    var element = document.getElementById(id);
    if (element.style.display === "none") {
        element.style.display = "block";
    } else {
        element.style.display = "none";
    }
  }

const hideFlashMessage = () => {
    const flashMessages = document.getElementById("flash-messages");
    if (flashMessages) {
        setTimeout(() => {
            flashMessages.style.display = "none";
        }, 5000);
    }
}
window.addEventListener("load", hideFlashMessage);

/*
window.addEventListener("load", () => {
    document.getElementById('search_form').onsubmit = () => {
        document.getElementById('loading_message').style.display = 'block';
    };
});
*/

function createReferenceFormListeners() {
    document.getElementById("add_author_button").addEventListener("click", addNewAuthor);
    document.getElementById("new_reference").addEventListener("submit", validateForm);
    document.getElementById("entry_type").addEventListener("change", createInputFields);
};

function createEditFormListeners() {
    document.getElementById("add_author_button").addEventListener("click", addNewAuthor);
    document.getElementById("new_reference").addEventListener("submit", validateForm);   
}

function createInputFields() {
    const fieldProfiles = JSON.parse(document.getElementById("field_profiles").textContent);
    const entryType = document.getElementById("entry_type").value;
    const fields = fieldProfiles[entryType] || { required: [], optional: [] };
    const requiredContainer = document.getElementById("required_fields");
    const optionalContainer = document.getElementById("optional_fields");

    // Clear existing fields
    requiredContainer.innerHTML = "";
    optionalContainer.innerHTML = "";

    if (fields.required && fields.required.length > 0) {

        fields.required.forEach(field => {
            if (field === "author") return;

            const div = document.createElement("div");
            div.className = "form-group";

            const label = document.createElement("label");
            label.innerHTML = `<b>${field}:</b>`;
            div.appendChild(label);

            const input = document.createElement("input");
            input.type = "text";
            input.className = "form-control";
            input.id = field;
            input.name = field;
            input.required = true;
            input.placeholder = "required"
            div.appendChild(input);

            requiredContainer.appendChild(div);
        });
    }

    if (fields.optional && fields.optional.length > 0) {

        fields.optional.forEach(field => {
            if (field === "author") return;

            const div = document.createElement("div");
            div.className = "form-group";

            const label = document.createElement("label");
            label.innerHTML = `<b>${field}:</b>`;
            div.appendChild(label);

            const input = document.createElement("input");
            input.type = "text";
            input.className = "form-control";
            input.id = field;
            input.name = field;
            div.appendChild(input);

            optionalContainer.appendChild(div);
        });
    }
}   

function addNewAuthor() {
    var firstName = document.getElementById("first_name");
    var lastName = document.getElementById("last_name");
    var authorList = document.getElementById("author_list");

    if (firstName.value.trim() != "" && lastName.value.trim() != "") {

        var container = document.createElement("div");
        container.className = "row justify-content-between";
        var person = document.createElement("li");
        person.textContent = lastName.value + ", " + firstName.value;

        var deletePerson = document.createElement("button");
        deletePerson.className = "btn btn-danger";
        deletePerson.textContent = "Delete";

        container.appendChild(person);
        container.appendChild(deletePerson);
        authorList.appendChild(container);

        deletePerson.addEventListener("click", () => deletePerson.parentElement.remove());

        firstName.value = "";
        lastName.value = "";
    } 
    else {
        alert("Add firstname and lastname");
    }
}

function validateForm(event) {
    var authorList = document.getElementById("author_list");
    var author = document.getElementById("author");
    
    if (authorList.children.length === 0) {
        alert("Add atleast one author before submitting.");
        event.preventDefault();
                return;
    }

    author.value = Array.from(authorList.children).map(li => li.firstChild.textContent).join(" and ");

    var form = document.getElementById("new_reference");
    var inputs = form.querySelectorAll("input[type='text'], input[type='number']");

    inputs.forEach(function(input) {
        if (!input.value.trim()) {
            input.disabled = true;
        }
    });
}

function addAuthor(firstName, lastName) {
    var authorList = document.getElementById("author_list");

    var container = document.createElement("div");
    container.className = "row justify-content-between";

    var person = document.createElement("li");
    person.textContent = lastName + ", " + firstName;

    var deletePerson = document.createElement("button");
    deletePerson.className = "btn btn-danger";
    deletePerson.textContent = "Delete";

    container.appendChild(person);
    container.appendChild(deletePerson);
    authorList.appendChild(container);

    deletePerson.addEventListener("click", () => deletePerson.parentElement.remove());
}

function downloadReferences() {
    fetch('/download', {
        method: 'POST',
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            showFlashMessage(data.message);

            let link = document.createElement('a');
            link.href = '/download';
            link.download = 'references.bib';
            link.click();
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function showFlashMessage(message) {
    let flashMessage = document.createElement('div');
    flashMessage.className = 'alert alert-success';
    flashMessage.textContent = message;
    document.body.appendChild(flashMessage);

    setTimeout(() => {
        flashMessage.remove();
    }, 15000);
}