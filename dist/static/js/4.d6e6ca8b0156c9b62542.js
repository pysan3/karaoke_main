webpackJsonp([4],{xJsL:function(e,s,t){"use strict";Object.defineProperty(s,"__esModule",{value:!0});var n=t("mtWM"),u=t.n(n),r={data:function(){return{user_name:"master",user_password:"hogehoge",isFound:0,user_id:0,result:0}},methods:{tryLogin:function(){var e=this;u.a.post("http://localhost:5042/api/login",{user_name:"takuto",user_password:"000"}).then(function(s){e.isFound=s.data.isFound,e.user_id=s.data.user_id,e.result=s.data.result}).catch(function(e){console.log(e)})}},created:function(){this.tryLogin()}},o={render:function(){var e=this,s=e.$createElement,t=e._self._c||s;return t("div",[t("p",[e._v("LOGIN")]),e._v(" "),t("p",[e._v("login succeeded "+e._s(e.isFound))]),e._v(" "),t("p",[e._v("login user_id "+e._s(e.user_id))]),e._v(" "),t("p",[e._v("signin user_name "+e._s(e.user_name))]),e._v(" "),t("p",[e._v("login result "+e._s(e.result))])])},staticRenderFns:[]},i=t("VU/8")(r,o,!1,null,null,null);s.default=i.exports}});
//# sourceMappingURL=4.d6e6ca8b0156c9b62542.js.map