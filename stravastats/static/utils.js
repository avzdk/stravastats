
function filterurl() {
    var query = "?";
    var distanceMin = document.getElementById("distanceFilterMin").value;
    var distanceMax = document.getElementById("distanceFilterMax").value;
    var startDate = document.getElementById("startDate").value;
    var endDate = document.getElementById("endDate").value;
    var tempoMin = document.getElementById("tempoFilterMin").value;
    var tempoMax = document.getElementById("tempoFilterMax").value;

    if (distanceMin != "") { query = query + `distanceMin=${distanceMin}&` }
    if (distanceMax != "") { query = query + `distanceMax=${distanceMax}&` }
    if (startDate != "") { query = query + `startDate=${startDate}&` }
    if (endDate != "") { query = query + `endDate=${endDate}&` }
    if (tempoMin != "") { query = query + `tempoMin=${tempoMin}&` }
    if (tempoMax != "") { query = query + `tempoMax=${tempoMax}&` }
    return query;
}

function showlist() {
    window.location.href = "/filter" + filterurl();
}

function showchart() {
    window.location.href = "/chart" + filterurl();
}

function filloutForm() {
    const urlParams = new URLSearchParams(window.location.search);
    document.getElementById("distanceFilterMin").value = urlParams.get("distanceMin");
    document.getElementById("distanceFilterMax").value = urlParams.get("distanceMax");
    document.getElementById("tempoFilterMin").value = urlParams.get("tempoMin");
    document.getElementById("tempoFilterMax").value = urlParams.get("tempoMax");
    document.getElementById("startDate").value = urlParams.get("startDate");
    document.getElementById("endDate").value = urlParams.get("endDate");
}