// const path = require("path");
const VueLoaderPlugin = require('vue-loader/lib/plugin');

module.exports = {
    mode: 'development',
    // mode: 'production',
    entry: "./src_vue/index.js",
    output: {
        filename: 'app.js',
        // path: path.resolve(__dirname, "static"),
        path: "C:/Almacen/static/builder",
    },
    /*optimization: {
        splitChunks: {chunks: 'all'}
    },*/
    resolve: {
        alias: {
            'vue$': 'vue/dist/vue.js'
        },
        // fallback: {
        //     // "stream": require.resolve("stream-browserify")
        //     "stream": false,
        //     "crypto": false,
        //     "util": false,
        //     "url": false,
        //     "timers": false,
        //     "os": false,
        //     "path": false,
        //     "http": false,
        //     "zlib": false,
        // },
    },
    module: {
        rules: [
            {test: /\.vue$/, use: 'vue-loader'},
            {test: /\.css$/i, use: ['style-loader', 'css-loader']}
        ]
    },
    plugins: [
        new VueLoaderPlugin()
    ]
}