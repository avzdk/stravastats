
function filterurl() {
    var query = "?";
    var id = getCookie("id");
    var distanceMin = document.getElementById("distanceFilterMin").value;
    var distanceMax = document.getElementById("distanceFilterMax").value;
    var startDate = document.getElementById("startDate").value;
    var endDate = document.getElementById("endDate").value;
    var tempoMin = document.getElementById("tempoFilterMin").value;
    var tempoMax = document.getElementById("tempoFilterMax").value;

    if (id != "") { query = query + `id=${id}&` }
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


function nextMondayISO(date) {
    date.setDate(date.getDate() + (1 + 7 - date.getDay()) % 7);
    datetxt = date.getFullYear() + "-" + String(date.getMonth() + 1).padStart(2, '0') + "-" + String(date.getDate()).padStart(2, '0');
    return datetxt;
}
function fillThisYear() {
    var firstmonday = new Date(new Date().getFullYear(), 0, 1);   // 1. januar
    datetxt = nextMondayISO(firstmonday);

    document.getElementById("startDate").value = datetxt;

}

function fillMdr(mdr) {
    var d1 = new Date();
    d1.setMonth(d1.getMonth() - mdr);
    datetxt = nextMondayISO(d1);
    document.getElementById("startDate").value = datetxt;
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