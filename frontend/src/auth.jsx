import { getCookie, setCookie } from "./cookie.jsx";

async function authenticate() {
    const token = getToken();

    if (token == null) {
        const username_input = document.getElementById("usernameInputField");
        const username = username_input.value;

        const password_input = document.getElementById("passwordInputField");
        const password = password_input.value;

        await send_authenticate(username, password);
    }
}

function getToken() {
    return getCookie("token");
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

export { authenticate as authenticate };
export { getToken as getToken };
