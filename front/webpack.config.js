const path = require("path");
const HtmlWebpackPlugin = require("html-webpack-plugin");
const webpack = require("webpack");

const env = process.env.NODE_ENV || 'development'

module.exports = {
    mode: env,
    entry: {
      index: './src/index.js',
    },
    output: {
      filename: '[name].bundle.js',
      chunkFilename: '[id].chunk.js',
      pathinfo: true,
      publicPath: "/"
    },
    resolve: {
      extensions: ['.ts', '.js'],
    },
    devServer: {
      contentBase: path.join(__dirname, "dist"),
      stats: 'errors-only',
      historyApiFallback:{
          index:'index.html',
          rewrites: [
            { from: /\/*/, to: '/index.html'}
          ]
        },
      compress: true,
      port: 3000,
      watchContentBase: true,
      overlay: true,
      open: true,
    },

    module: {
      rules: [
        {
          test: /\.m?js$/,
          exclude: /(node_modules|bower_components)/,
          use: {
            loader: "babel-loader"
          }
        },
        {
          test: /\.css$/,
          use: ['style-loader', 'css-loader'],
        },
        {
          test: /\.(png|svg|jpg|gif)$/,
          use: ["file-loader"]
        },
        {
          test: /\.(woff(2)?|eot|ttf|otf)$/,
          type: 'asset/inline',
        },
      ]
    },
    plugins: [
      new HtmlWebpackPlugin({
        template: "./src/index.html",
        title: 'Development',
        favicon: "./src/favicon.ico"
      }),
      new webpack.DefinePlugin({
            'process.env.API_HOST': JSON.stringify(process.env.API_HOST),
            })
    ],
    performance: {
      hints: false,
      maxEntrypointSize: 512000,
      maxAssetSize: 512000
    }
}
