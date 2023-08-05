window.addEventListener("load", function () {
    // Make the message box disapear after 5 seconds.
    const message_box = document.querySelector("ul#messages-box");
    if (message_box) {
        setTimeout(function () {
            message_box.style.opacity = 0;
        }, 5000)
    }
});