function setCurrentYearAsMax(id) {
    var year = new Date().getFullYear();
    document.getElementById(id).setAttribute("max", year);
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
        btn.textContent = "Piilota valinnaiset";
    }
    else {
        opt.style.display = "none";
        btn.textContent = "Näytä valinnaiset";
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
        var person = document.createElement("li");
        person.textContent = lastName.value + ", " + firstName.value;

        var deletePerson = document.createElement("button");
        deletePerson.className = "btn btn-warning"
        deletePerson.textContent = "Poista"

        person.appendChild(deletePerson);
        authorList.appendChild(person);

        deletePerson.addEventListener("click", () => deletePerson.parentElement.remove());

        firstName.value = "";
        lastName.value = "";
    } 
    else {
        alert("Syötä etu- ja sukunimi");
    }
}

function validateForm(event) {
    var authorList = document.getElementById("author_list");
    var author = document.getElementById("author");

    if (authorList.children.length === 0) {
        alert("Lisää ainakin yksi author ennen lomakkeen lähettämistä.");
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
    var person = document.createElement("li");

    person.textContent = lastName + ", " + firstName;

    var deletePerson = document.createElement("button");
    deletePerson.className = "btn btn-warning"
    deletePerson.textContent = "Poista"

    person.appendChild(deletePerson);
    authorList.appendChild(person);

    deletePerson.addEventListener("click", () => deletePerson.parentElement.remove());
}
