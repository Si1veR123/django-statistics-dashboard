
var root;

function setCookie(cname, cvalue, exdays) {
  var d = new Date();
  d.setTime(d.getTime() + (exdays*24*60*60*1000));
  var expires = "expires="+ d.toUTCString();
  document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

function getCookie(cname) {
  var name = cname + "=";
  var decodedCookie = decodeURIComponent(document.cookie);
  var ca = decodedCookie.split(';');
  for(var i = 0; i < ca.length; i++) {
    var c = ca[i];
    while (c.charAt(0) == ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}

function sendActivity(data) {
    return axios.post(root + "activity/", data)
}

function newPage() {
    {
        let scriptEl = document.createElement("script");
        scriptEl.setAttribute("src", "https://unpkg.com/axios/dist/axios.min.js");
        let body = document.getElementsByTagName("body")[0];
        body.appendChild(scriptEl);
    }

    let dataRoot = document.currentScript.getAttribute("data-root");
    if (dataRoot === null) {
        root = "/stats/"
    } else {
        root = dataRoot
    }

    axios.get(root + "config/?page=" + window.location.pathname)
    .then((response) => {
        const config = response.data;
        sendActivity({type: "navigate", info: window.location.pathname}).then(function() {
            if (getCookie("c3RhdHZpZXdlZA") === "") {
                sendActivity({type: "new_to_website", info: true});
                setCookie("c3RhdHZpZXdlZA", "1", 365);
            } else {
                sendActivity({type: "new_to_website", info: false});
            }

            // add event listeners for click
            for (let click of config.click) {
                let el = document.querySelector(click.selector);
                el.statsName = click.name;
                el.addEventListener("click", function(evt) {
                    sendActivity({type: "click", info: evt.target.statsName})
                });
            }
        })
    })
}

// SHOULD DETECT CHANGE ON SPAS, NEED TESTING
var lastUrl = window.location.pathname;

setTimeout(function() {
    if (window.location.pathname !== lastUrl) {
        sendActivity({type: "navigate", info: window.location.pathname});
        lastUrl = window.location.pathname;
    }
}, 1000)

window.onload = newPage