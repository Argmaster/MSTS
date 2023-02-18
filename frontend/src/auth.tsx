import { getCookie, setCookie } from "./cookie";

export async function authenticate() {
    const token = getToken();

    if (token == null) {
        const username_input = document.getElementById(
            "usernameInputField"
        ) as HTMLInputElement;
        const username = username_input.value;

        const password_input = document.getElementById(
            "passwordInputField"
        ) as HTMLInputElement;
        const password = password_input.value;

        await send_authenticate(username, password);
    }
}

export function getToken() {
    return getCookie("token");
}

async function send_authenticate(username: string, password: string) {
    const formData = new FormData();
    formData.append("username", username);
    formData.append("password", password);

    const response = await fetch("/token", {
        method: "POST",
        body: formData,
    });
    const content = await response.json();

    setToken(content.access_token);
    console.log(`Authenticated; token ${content.access_token}`);
}

function setToken(token: string) {
    setCookie("token", token, 29);
}
