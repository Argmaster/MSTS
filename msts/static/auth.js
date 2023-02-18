async function authenticate() {
    const token = getToken();

    if (token == null) {
        const username_input = document.getElementById("usernameInputField");
        const username = username_input.value;

        const password_input = document.getElementById("passwordInputField");
        const password = password_input.value;

        await send_authenticate(username, password);
    }

    await redirectToMenu();
}

function getToken() {
    return getCookie("token");
}

function getCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(";");
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == " ") c = c.substring(1, c.length);
        if (c.indexOf(nameEQ) == 0)
            return c.substring(nameEQ.length, c.length);
    }
    return null;
}

async function send_authenticate(username, password) {
    const formData = new FormData();
    formData.append("username", username);
    formData.append("password", password);

    const response = await fetch("/token", {
        method: "POST",
        body: formData,
    });
    const content = await response.json();

    setToken(content.access_token);
}

function setToken(token) {
    setCookie("token", token, 29);
}

function setCookie(name, value, minutes) {
    var expires = "";
    if (minutes) {
        var date = new Date();
        date.setTime(date.getTime() + minutes * 60 * 1000);
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + (value || "") + expires + "; path=/";
}

function eraseCookie(name) {
    document.cookie =
        name + "=; Path=/; Expires=Thu, 01 Jan 1970 00:00:01 GMT;";
}

async function redirectToMenu() {
    const token = getToken();

    if (token === null) {
        return;
    }

    const response = await fetch("/menu", {
        method: "GET",
        headers: {
            Authorization: `Bearer ${token}`,
        },
    });
    const content = await response.text();

    const body = document.getElementById("body-container");
    console.log(body);
    body.innerHTML = content;
}

redirectToMenu();
