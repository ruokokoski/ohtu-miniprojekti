function set_current_year_as_max(id) {
    var year = new Date().getFullYear();
    document.getElementById(id).setAttribute("max", year)
}