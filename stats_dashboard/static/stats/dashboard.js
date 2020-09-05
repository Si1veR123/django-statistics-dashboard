function changePageSession(browserSessionToken) {
    for (let page of document.querySelectorAll(".panel:nth-child(3) ul")) {
        page.style.opacity = 0;
        page.style.display = "none";
    }

    let pages = document.querySelector("ul[data-browser-uuid='" + browserSessionToken + "']");
    pages.style.opacity = 1;
    pages.style.display = "initial";

    if (pages.children.length === 0) {
        let emptyMessage = document.createElement("li");
        emptyMessage.innerText = "No tracked pages were visited";
        pages.appendChild(emptyMessage);
    }
}

function changeActions(pageId) {
    for (let action of document.querySelectorAll(".panel:nth-child(4) ul")) {
        action.style.opacity = 0;
        action.style.display = "none";
    }

    let actions = document.querySelector("ul[data-page-id='" + pageId + "']");
    actions.style.opacity = 1;
    actions.style.display = "initial";
}

function filterBrowserSessions(evt) {
    let start = evt.target.parentNode.querySelector('input[name=start]').value;
    let end = evt.target.parentNode.querySelector('input[name=end]').value;

    if (start === "") {
        start = 0
    }

    if (end === "") {
        end = Date.now()
    }

    let startDate = new Date(start);
    let endDate = new Date(end);

    for (session of document.querySelectorAll("#sessions-panel li")) {
        let time = new Date(session.getAttribute("data-time"));
        if (!(time > startDate && time < endDate)) {
            session.style.display = "none";
        } else {
            session.style.display = "list-item";
        }
    }
}

function resetBrowserFilter(evt) {
    let start = evt.target.parentNode.parentNode.querySelector('input[name=start]');
    let end = evt.target.parentNode.parentNode.querySelector('input[name=end]');
    start.value = "";
    end.value = "";

    var fakeEvent = {
        target: start,
    }

    filterBrowserSessions(fakeEvent);
}


function convertToBold(text) {
    return "<span style='font-weight: bold;'>" + text + "</span>"
}

{
    var browsers = document.querySelectorAll("#sessions-panel li");
    var ipAddresses = [];

    for (let browser of browsers) {
        ipAddresses.push(browser.getAttribute("data-ip"));
        let browser_name = browser.getAttribute("data-browser");
        let device = browser.getAttribute("data-device");
        browser.innerHTML += " on " + convertToBold(browser_name + " " + device);
    }

    let xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            for (let result of JSON.parse(xhttp.responseText)) {
               let location = result["country"];
               let resultBrowsers = Array.prototype.slice.call(browsers).filter(b => b.getAttribute("data-ip") === result["query"]);
               for (browser of resultBrowsers) {
                   if (location !== undefined) {
                       browser.innerHTML += " in " + convertToBold(location);
                   }
               }
            }
        }
    }
    xhttp.open("POST", "http://ip-api.com/batch/");
    xhttp.send(JSON.stringify(ipAddresses));
}

function toListPage() {
    document.getElementById("graph-page").style.display = "none";
    document.getElementById("list-page").style.display = "initial";
}

function toGraphPage() {
    document.getElementById("list-page").style.display = "none";
    document.getElementById("graph-page").style.display = "initial";

    let xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            let chartGrid = document.getElementById("chart-grid");
            chartGrid.innerHTML = "";
            for (chartData of JSON.parse(xhttp.responseText)) {
                let container = document.createElement("div");
                container.classList.add("chart-container");

                let title = document.createElement("h2");
                title.innerText = chartData["name"];
                title.classList.add("chart-title");

                let canvas = document.createElement("canvas");
                canvas.setAttribute("id", chartData["name"].replace(" ", "-") + "-chart");

                container.appendChild(title);
                container.appendChild(canvas);
                chartGrid.appendChild(container);

                let ctx = canvas.getContext("2d");

                var data = chartData["data"]

                let chart = new Chart(ctx, {
                    type: chartData["type"],
                    data: data,
                    options: chartData["options"]
                })
            }
        }
    }
    xhttp.open("GET", "charts/");
    xhttp.send();
}

