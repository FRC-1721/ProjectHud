const path = require("path");

module.exports = {
    entry: "./node_modules/@gitgraph/js",
    output: {
        path: path.resolve(__dirname, "app/static/scripts"),
        filename: "gitgraph.bundle.js",
        library: "GitgraphJS", // Expose GitgraphJS as a global variable
        libraryTarget: "var", // Attach it to the window object
    },
    mode: "production",
};