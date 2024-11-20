function set_current_year_as_max(id) {
    var year = new Date().getFullYear();
    document.getElementById(id).setAttribute("max", year)
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