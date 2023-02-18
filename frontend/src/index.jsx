import { authenticate, getToken } from "./auth.jsx";

async function redirectToMenu() {
    const token = getToken();

    if (token === null) {
        return false;
    }

    const response = await fetch("/menu", {
        method: "GET",
        headers: {
            Authorization: `Bearer ${token}`,
        },
    });
    const content = await response.text();

    const body = document.getElementById("body-container");
    body.innerHTML = content;

    return true;
}

(async () => {
    const was_redirected = false; // await redirectToMenu();

    if (!was_redirected) {
        const login_submit = document.getElementById("login-submit");
        login_submit.addEventListener("click", async () => {
            await authenticate();
            await redirectToMenu();
        });
    }
})();
