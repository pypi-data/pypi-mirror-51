// Compiled by ClojureScript 1.10.439 {}
goog.provide('reagent.debug');
goog.require('cljs.core');
reagent.debug.has_console = (typeof console !== 'undefined');
reagent.debug.tracking = false;
if((typeof reagent !== 'undefined') && (typeof reagent.debug !== 'undefined') && (typeof reagent.debug.warnings !== 'undefined')){
} else {
reagent.debug.warnings = cljs.core.atom.call(null,null);
}
if((typeof reagent !== 'undefined') && (typeof reagent.debug !== 'undefined') && (typeof reagent.debug.track_console !== 'undefined')){
} else {
reagent.debug.track_console = (function (){var o = ({});
o.warn = ((function (o){
return (function() { 
var G__639__delegate = function (args){
return cljs.core.swap_BANG_.call(null,reagent.debug.warnings,cljs.core.update_in,new cljs.core.PersistentVector(null, 1, 5, cljs.core.PersistentVector.EMPTY_NODE, [new cljs.core.Keyword(null,"warn","warn",-436710552)], null),cljs.core.conj,cljs.core.apply.call(null,cljs.core.str,args));
};
var G__639 = function (var_args){
var args = null;
if (arguments.length > 0) {
var G__640__i = 0, G__640__a = new Array(arguments.length -  0);
while (G__640__i < G__640__a.length) {G__640__a[G__640__i] = arguments[G__640__i + 0]; ++G__640__i;}
  args = new cljs.core.IndexedSeq(G__640__a,0,null);
} 
return G__639__delegate.call(this,args);};
G__639.cljs$lang$maxFixedArity = 0;
G__639.cljs$lang$applyTo = (function (arglist__641){
var args = cljs.core.seq(arglist__641);
return G__639__delegate(args);
});
G__639.cljs$core$IFn$_invoke$arity$variadic = G__639__delegate;
return G__639;
})()
;})(o))
;

o.error = ((function (o){
return (function() { 
var G__642__delegate = function (args){
return cljs.core.swap_BANG_.call(null,reagent.debug.warnings,cljs.core.update_in,new cljs.core.PersistentVector(null, 1, 5, cljs.core.PersistentVector.EMPTY_NODE, [new cljs.core.Keyword(null,"error","error",-978969032)], null),cljs.core.conj,cljs.core.apply.call(null,cljs.core.str,args));
};
var G__642 = function (var_args){
var args = null;
if (arguments.length > 0) {
var G__643__i = 0, G__643__a = new Array(arguments.length -  0);
while (G__643__i < G__643__a.length) {G__643__a[G__643__i] = arguments[G__643__i + 0]; ++G__643__i;}
  args = new cljs.core.IndexedSeq(G__643__a,0,null);
} 
return G__642__delegate.call(this,args);};
G__642.cljs$lang$maxFixedArity = 0;
G__642.cljs$lang$applyTo = (function (arglist__644){
var args = cljs.core.seq(arglist__644);
return G__642__delegate(args);
});
G__642.cljs$core$IFn$_invoke$arity$variadic = G__642__delegate;
return G__642;
})()
;})(o))
;

return o;
})();
}
reagent.debug.track_warnings = (function reagent$debug$track_warnings(f){
reagent.debug.tracking = true;

cljs.core.reset_BANG_.call(null,reagent.debug.warnings,null);

f.call(null);

var warns = cljs.core.deref.call(null,reagent.debug.warnings);
cljs.core.reset_BANG_.call(null,reagent.debug.warnings,null);

reagent.debug.tracking = false;

return warns;
});

//# sourceMappingURL=debug.js.map
