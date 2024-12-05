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

window.addEventListener("load", () => {
    document.getElementById('search_form').onsubmit = () => {
        document.getElementById('loading_message').style.display = 'block';
    };
});
/*
const handleBibtexButtonClick = (resultId) => {
    fetch(`/bibtex/${encodeURIComponent(resultId)}`)
        .then(response => {
            if (response.ok) {
                console.log("Button pressed with resultId:", resultId);
                return response.text();
            } else {
                console.error("Failed to fetch BibTeX:", response.status);
                throw new Error(`Failed to fetch BibTeX for resultId: ${resultId}`);
            }
        })
        .catch(error => {
            console.error("Error pressing button:", error);
        });
};
*/

const handleBibtexButtonClick = (resultId) => {
    fetch(`/bibtex/${encodeURIComponent(resultId)}`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ result_id: resultId }),
    })
        .then(response => {
            if (response.ok) {
                console.log("Button pressed with resultId:", resultId);
                return response.text();
            } else {
                console.error("Failed to fetch BibTeX:", response.status);
                throw new Error(`Failed to fetch BibTeX for resultId: ${resultId}`);
            }
        })
        .catch(error => {
            console.error("Error pressing button:", error);
        });
};

function createReferenceFormButtons() {
    document.getElementById("toggle_optionals_button").addEventListener("click", toggleOptionals);
    document.getElementById("add_author_button").addEventListener("click", addNewAuthor);
    document.getElementById("new_reference").addEventListener("submit", validateForm);
    document.getElementById("entry_type").addEventListener("change", toggleBook);
};

function toggleOptionals() {
    toggleBook();
    var opt = document.getElementById("optional_fields");
    var btn = document.getElementById("toggle_optionals_button");

    if (opt.style.display === "none") {
        opt.style.display = "block";
        btn.textContent = "Hide optionals";
    }
    else {
        opt.style.display = "none";
        btn.textContent = "Show optionals";
    }
}

function toggleBook() {
    let book = document.getElementById("book_fields");
    let article = document.getElementById("article_fields");
    let select = document.getElementById("entry_type");
    if (select.value === "book") {
        book.style.display = "block";
        article.style.display = "none";
    }
    else if (select.value === "article") {
        book.style.display = "none";
        article.style.display = "block";
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