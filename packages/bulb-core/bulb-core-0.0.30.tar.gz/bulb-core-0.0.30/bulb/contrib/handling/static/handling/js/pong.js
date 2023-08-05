import {AJAXRequest} from "../../utils/js/ajax.js";

console.log("aa");

function print(response) {
    console.log(response)
}

function ping () {
    AJAXRequest("GET", "http://127.0.0.1:8000/admin/gestion/pong", print, true);
}

setInterval(ping, 3000);