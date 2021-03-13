const devServer = {
  host: "toptable.localhost",
  port: 8430,
  historyApiFallback: true,
  proxy: "http://toptable.localhost:8431"
};

module.exports = {
  lintOnSave: false,
  devServer
};
