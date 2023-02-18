import { authenticate } from "../auth";
import React from "react";

export const App = () => (
    <main>
        <div className="container text-center min-vh-100 d-flex flex-column">
            <div className="row align-items-center justify-content-center flex-grow-1">
                <div className="col-11 col-sm-9 col-md-6 col-lg-5 col-xl-4 col-xxl-3">
                    <div>
                        <h2 className="mb-5">Log in</h2>
                        <div className="mb-3">
                            <label
                                htmlFor="usernameInputField"
                                className="form-label"
                            >
                                User name
                            </label>
                            <input
                                type="text"
                                className="form-control"
                                id="usernameInputField"
                                name="username"
                                autoComplete="username"
                            />
                        </div>
                        <div className="mb-5">
                            <label
                                htmlFor="passwordInputField"
                                className="form-label"
                            >
                                Password
                            </label>
                            <input
                                type="password"
                                className="form-control"
                                id="passwordInputField"
                                name="password"
                                autoComplete="current-password"
                            />
                        </div>
                        <button
                            type="button"
                            className="btn btn-primary"
                            id="login-submit"
                            onClick={async () => {
                                await authenticate();
                            }}
                        >
                            Submit
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </main>
);
