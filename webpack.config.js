/* jshint node: true */
/* jshint strict: false */

const autoprefixer = require('autoprefixer');
const path = require('path');

const CssMinimizerPlugin = require("css-minimizer-webpack-plugin");
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const RemoveEmptyScriptsPlugin = require('webpack-remove-empty-scripts');
const TerserPlugin = require('terser-webpack-plugin');
const CopyPlugin = require("copy-webpack-plugin");

module.exports = {
  mode: 'production',
  entry: {
    index: path.resolve(__dirname, "assets", "js"),
  },
  output: {
    path: path.resolve(__dirname, "static", "js"),
    filename: '[name].js',
  },
  optimization: {
    minimize: true,
    minimizer: [
      new TerserPlugin({}),
      new CssMinimizerPlugin({}),
    ],
  },
  plugins: [
    new MiniCssExtractPlugin(),
    new RemoveEmptyScriptsPlugin(),
    new CopyPlugin({
      patterns: [
        {
          from: path.resolve(__dirname, "assets", "css"),
          to: path.resolve(__dirname, "static", "css")
        },
      ],
    }),
  ]
};
