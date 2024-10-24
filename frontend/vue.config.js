const webpack = require('webpack');
const packageJson = require('./package.json');

module.exports = {
    devServer: {
        port: 9876
    },
    configureWebpack: {
        plugins: [
            new webpack.DefinePlugin({
                'process.env': {
                    PACKAGE_VERSION: JSON.stringify(packageJson.version),
                },
            }),
        ],
    },
};