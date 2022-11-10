function filter() {
    var distanceMin = document.getElementById("distanceFilterMin").value;
    var distanceMax = document.getElementById("distanceFilterMax").value;
    var startDate = document.getElementById("startDate").value;
    var endDate = document.getElementById("endDate").value;
    window.location.href = window.location.pathname + `?distanceMin=${distanceMin}&distanceMax=${distanceMax}&startDate=${startDate}&endDate=${endDate}`;
}