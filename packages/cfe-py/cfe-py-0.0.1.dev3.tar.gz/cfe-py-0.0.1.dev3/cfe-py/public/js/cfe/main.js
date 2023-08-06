// Compiled by ClojureScript 1.10.439 {}
goog.provide('cfe.main');
goog.require('cljs.core');
goog.require('reagent.core');
goog.require('cfe.common');
goog.require('cfe.files.project_picker');
cfe.main.wrapper = (function cfe$main$wrapper(props){
return cljs.core.deref.call(null,cfe.common.state).call(null,new cljs.core.Keyword(null,"active-screen","active-screen",-1779681012)).call(null);
});
cfe.main.main = (function cfe$main$main(){
return reagent.core.render.call(null,new cljs.core.PersistentVector(null, 1, 5, cljs.core.PersistentVector.EMPTY_NODE, [cfe.main.wrapper], null),document.body.appendChild(document.createElement("div")));
});
cfe.main.loading = (function cfe$main$loading(){
return new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [new cljs.core.Keyword(null,"p","p",151049309),"Loading..."], null);
});
cfe.common.switch_screen.call(null,cfe.main.loading);
window.setTimeout((function (){
return cfe.common.switch_screen.call(null,cfe.files.project_picker.start);
}),(1000));
cfe.main.main.call(null);

//# sourceMappingURL=main.js.map
