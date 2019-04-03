module.exports = {
  baseUrl: "",
  productionSourceMap: false,
  devServer: {
    proxy: "http://127.0.0.1:10000"//'http://127.0.0.1:10000'//'http://118.25.208.216:10000'
  }
};
