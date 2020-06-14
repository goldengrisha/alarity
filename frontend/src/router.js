import VueRouter from "vue-router";
import ComparingContent from "./components/ComparingContent";
import UploadContent from "./components/UploadContent";

const routes = [
  { path: "/", component: UploadContent },
  { path: "/compare/:textId", component: ComparingContent },
  { path: "/upload", component: UploadContent },
];

export default new VueRouter({
  routes,
});
