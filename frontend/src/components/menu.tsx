import { getToken } from "../auth";

export async function Menu() {
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
