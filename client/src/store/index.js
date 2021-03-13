import restaurant from "./restaurant";

const store = {
  list: [],
  install: (app, _options) => {
    app.config.globalProperties.$store = store;
    store.list.forEach(m => m.init?.());
  }
};

Object.entries({ restaurant }).forEach(([name, module]) => {
  store.list.push(module);
  store[name] = module;
});

export default store;
