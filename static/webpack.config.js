const path = require('path');
const webpack = require('webpack');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const CleanWebpackPlugin = require('clean-webpack-plugin');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');

module.exports = function(env) {

  var pack = require('./package.json');
  var production = !!(env && env.production === 'true');
  var asmodule = !!(env && env.module === 'true');
  var standalone = !!(env && env.standalone === 'true');

  var babelSettings = {
    extends: path.join(__dirname, '/.babelrc')
  };

  var config = {
    mode: production ? 'production' : 'development',
    entry: {
      app: './sources/app.js'
    },
    output: {
      path: path.join(__dirname, 'dist'),
      publicPath:'/dist/',
      filename: production ? '[name].[contenthash].js' : '[name].js',
      chunkFilename: production ? '[name].[contenthash].js' : '[name].js'
    },
    module: {
      rules: [
        {
          test: /\.js$/,
          exclude: /node_modules/,
          use: 'babel-loader?' + JSON.stringify(babelSettings)
        },
        {
          test: /\.(less|css)$/,
          use: [ MiniCssExtractPlugin.loader, 'css-loader', 'less-loader' ]
        },
        {
          test: /.(svg|png|jpg|gif|woff|woff2|ttf|eot)$/,
          exclude: /assets/,
          use: 'url-loader?limit=25000'
        }
      ]
    },
    stats:'minimal',
    resolve: {
      extensions: ['.js'],
      modules: ['./sources', 'node_modules'],
      alias:{
        'jet-views':path.resolve(__dirname, 'sources/views'),
        'jet-locales':path.resolve(__dirname, 'sources/locales')
      }
    },
    watchOptions: {
      poll: 1000,
      aggregateTimeout: 500,
      ignored: /node_modules/
    },
    plugins: [
      new HtmlWebpackPlugin({
        template: __dirname + '/sources/index.tmpl.html',
        filename: '../index.html'}
      ),
      new webpack.HashedModuleIdsPlugin(),
      new MiniCssExtractPlugin({
        filename:production ? '[name].[contenthash].css' : '[name].css'
      }),
      new webpack.DefinePlugin({
        VERSION: `"${pack.version}"`,
        APPNAME: `"${pack.name}"`,
        PRODUCTION : production,
        BUILD_AS_MODULE : (asmodule || standalone)
      })
    ],
    devServer:{
      stats:'errors-only'
    },
    optimization: {
      runtimeChunk: 'single',
      splitChunks: {
        cacheGroups: {
          vendor: {
            test: /[\\/]node_modules[\\/]/,
            name: 'vendors',
            chunks: 'all'
          }
        }
      }
    }
  };

  if (!production){
    config.devtool = 'inline-source-map';
  } else {
    config.plugins.push(new CleanWebpackPlugin(['dist']));
  }

  if (asmodule){
    if (!standalone){
      config.externals = config.externals || {};
      config.externals = [ 'webix-jet' ];
    }

    const out = config.output;
    const sub = standalone ? 'full' : 'module';

    out.library = pack.name.replace(/[^a-z0-9]/gi, '');
    out.libraryTarget= 'umd';
    out.path = path.join(__dirname, 'dist', sub);
    out.publicPath = '/dist/'+sub+'/';
  }

  return config;
};