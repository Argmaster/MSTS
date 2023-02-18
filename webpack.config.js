const path = require("path");

module.exports = {
    entry: path.resolve(__dirname, "frontend", "src", "index.jsx"),
    output: {
        path: path.resolve(__dirname, "backend", "msts", "static"),
        filename: "bundle.js",
    },
    devtool: false,
};
