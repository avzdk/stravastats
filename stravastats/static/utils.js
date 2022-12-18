
function filterurl() {
    var query = "?";
    var username = getCookie("username");
    var distanceMin = document.getElementById("distanceFilterMin").value;
    var distanceMax = document.getElementById("distanceFilterMax").value;
    var startDate = document.getElementById("startDate").value;
    var endDate = document.getElementById("endDate").value;
    var tempoMin = document.getElementById("tempoFilterMin").value;
    var tempoMax = document.getElementById("tempoFilterMax").value;

    if (username != "") { query = query + `username=${username}&` }
    if (distanceMin != "") { query = query + `distanceMin=${distanceMin}&` }
    if (distanceMax != "") { query = query + `distanceMax=${distanceMax}&` }
    if (startDate != "") { query = query + `startDate=${startDate}&` }
    if (endDate != "") { query = query + `endDate=${endDate}&` }
    if (tempoMin != "") { query = query + `tempoMin=${tempoMin}&` }
    if (tempoMax != "") { query = query + `tempoMax=${tempoMax}&` }

    return query;
}

function changeurl(page) {
    window.location.href = "./" + page + filterurl();
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



function fillThisYear() {
    document.getElementById("startDate").value = "2022-01-01";
}

function fillMdr(mdr) {
    var d1 = new Date();
    d1.setMonth(d1.getMonth() - mdr);
    var str = d1.toISOString().substring(0, 10);
    document.getElementById("startDate").value = str;
}

function getCookie(cname) {
    let name = cname + "=";
    let decodedCookie = decodeURIComponent(document.cookie);
    let ca = decodedCookie.split(';');
    for (let i = 0; i < ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}