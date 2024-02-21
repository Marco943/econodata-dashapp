window.addEventListener("keyup", function (e) {
    if (e.key === "Enter") {
        if (e.target.id.slice(0, 5) === "login") {
            this.document.getElementById("login-btn").click();
        } else if (e.target.id.slice(0, 6) === "signup") {
            this.document.getElementById("signup-btn").click();
        };
    };
});