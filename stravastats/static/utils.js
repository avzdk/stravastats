function filter() {
    var query = "?";
    var distanceMin = document.getElementById("distanceFilterMin").value;
    var distanceMax = document.getElementById("distanceFilterMax").value;
    var startDate = document.getElementById("startDate").value;
    var endDate = document.getElementById("endDate").value;

    if (distanceMin != "") { query = query + `distanceMin=${distanceMin}&` }
    if (distanceMax != "") { query = query + `distanceMax=${distanceMax}&` }
    if (startDate != "") { query = query + `startDate=${startDate}&` }
    if (endDate != "") { query = query + `endDate=${endDate}&` }
    /*          
        window.location.href = window.location.pathname + `?distanceMin=${distanceMin}&distanceMax=${distanceMax}&startDate=${startDate}&endDate=${endDate}`;
        */
    window.location.href = window.location.pathname + query;
}

function chart() {
    var query = "?";
    var distanceMin = document.getElementById("distanceFilterMin").value;
    var distanceMax = document.getElementById("distanceFilterMax").value;
    var startDate = document.getElementById("startDate").value;
    var endDate = document.getElementById("endDate").value;
    if (distanceMin != "") { query = query + `distanceMin=${distanceMin}&` }
    if (distanceMax != "") { query = query + `distanceMax=${distanceMax}&` }
    if (startDate != "") { query = query + `startDate=${startDate}&` }
    if (endDate != "") { query = query + `endDate=${endDate}&` }
    console.log(window.location.pathname);
    console.log(window.location.host);
    window.location.href = "/chart" + query;
}

function filloutForm() {
    const urlParams = new URLSearchParams(window.location.search);
    document.getElementById("distanceFilterMin").value = urlParams.get("distanceMin");
    document.getElementById("distanceFilterMax").value = urlParams.get("distanceMax");
    document.getElementById("startDate").value = urlParams.get("startDate");
    document.getElementById("endDate").value = urlParams.get("endDate");
}