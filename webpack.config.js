const path = require("path");

module.exports = {
    entry: path.resolve(__dirname, "frontend", "src", "index.tsx"),
    module: {
        rules: [
            {
                test: /(\.tsx?|\.jsx?)$/,
                use: "ts-loader",
                exclude: /node_modules/,
            },
        ],
    },
    resolve: {
        extensions: [".tsx", ".ts", ".jsx", ".js"],
    },
    output: {
        path: path.resolve(__dirname, "backend", "msts", "static"),
        filename: "bundle.js",
    },
    devtool: false,
};
