webpackJsonp([5],{lO7g:function(n,t,e){"use strict";Object.defineProperty(t,"__esModule",{value:!0});var o=e("mtWM"),a=e.n(o),r={data:function(){return{randomNumber:0}},methods:{getRandom:function(){var n=this;a.a.get("http://localhost:5042/api/random").then(function(t){n.randomNumber=t.data.randomNumber}).catch(function(n){console.log(n)})}},created:function(){this.getRandom()}},u={render:function(){var n=this,t=n.$createElement,e=n._self._c||t;return e("div",[e("p",[n._v("Home page")]),n._v(" "),e("p",[n._v("Random number from backend: "+n._s(n.randomNumber))]),n._v(" "),e("button",{on:{click:n.getRandom}},[n._v("New random number")]),n._v(" "),e("router-link",{attrs:{to:"/about"}},[e("a",[n._v("about")])]),n._v(" "),e("router-link",{attrs:{to:"/api/login"}},[e("a",[n._v("login")])]),n._v(" "),e("router-link",{attrs:{to:"/api/signin"}},[e("a",[n._v("signin")])])],1)},staticRenderFns:[]},i=e("VU/8")(r,u,!1,null,null,null);t.default=i.exports}});
//# sourceMappingURL=5.9f7d5250681a653c94d4.js.map