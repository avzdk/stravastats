function filter() {
    var distanceMin = document.getElementById("distanceFilterMin").value;
    var distanceMax = document.getElementById("distanceFilterMax").value;
    var startDate = document.getElementById("startDate").value;
    var endDate = document.getElementById("endDate").value;
    window.location.href = window.location.pathname + `?distanceMin=${distanceMin}&distanceMax=${distanceMax}&startDate=${startDate}&endDate=${endDate}`;
}

function chart() {
    var distanceMin = document.getElementById("distanceFilterMin").value;
    var distanceMax = document.getElementById("distanceFilterMax").value;
    var startDate = document.getElementById("startDate").value;
    var endDate = document.getElementById("endDate").value;
    console.log(window.location.pathname);
    console.log(window.location.host);
    window.location.href = "/chart" + `?distanceMin=${distanceMin}&distanceMax=${distanceMax}&startDate=${startDate}&endDate=${endDate}`;
}