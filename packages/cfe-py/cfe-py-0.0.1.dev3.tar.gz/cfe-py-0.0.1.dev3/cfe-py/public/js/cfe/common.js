// Compiled by ClojureScript 1.10.439 {}
goog.provide('cfe.common');
goog.require('cljs.core');
goog.require('reagent.core');
cfe.common.state = reagent.core.atom.call(null,new cljs.core.PersistentArrayMap(null, 3, [new cljs.core.Keyword(null,"project-address","project-address",360976148),location.origin,new cljs.core.Keyword(null,"active-screen","active-screen",-1779681012),null,new cljs.core.Keyword(null,"previous-screens","previous-screens",-161703131),cljs.core.PersistentVector.EMPTY], null));
cfe.common.switch_screen_0 = (function cfe$common$switch_screen_0(to,state){
return cljs.core.assoc.call(null,state,new cljs.core.Keyword(null,"active-screen","active-screen",-1779681012),to,new cljs.core.Keyword(null,"previous-screens","previous-screens",-161703131),cljs.core.cons.call(null,new cljs.core.Keyword(null,"active-screen","active-screen",-1779681012).cljs$core$IFn$_invoke$arity$1(state),new cljs.core.Keyword(null,"previous-screens","previous-screens",-161703131).cljs$core$IFn$_invoke$arity$1(state)));
});
cfe.common.switch_screen = (function cfe$common$switch_screen(to){
return cljs.core.swap_BANG_.call(null,cfe.common.state,cljs.core.partial.call(null,cfe.common.switch_screen_0,to));
});
cfe.common.back_0 = (function cfe$common$back_0(state){
return cljs.core.assoc.call(null,state,new cljs.core.Keyword(null,"active-screen","active-screen",-1779681012),cljs.core.first.call(null,new cljs.core.Keyword(null,"previous-screens","previous-screens",-161703131).cljs$core$IFn$_invoke$arity$1(state)),new cljs.core.Keyword(null,"previous-screens","previous-screens",-161703131),cljs.core.rest.call(null,new cljs.core.Keyword(null,"previous-screens","previous-screens",-161703131).cljs$core$IFn$_invoke$arity$1(state)));
});
cfe.common.back = (function cfe$common$back(var_args){
var args__4647__auto__ = [];
var len__4641__auto___688 = arguments.length;
var i__4642__auto___689 = (0);
while(true){
if((i__4642__auto___689 < len__4641__auto___688)){
args__4647__auto__.push((arguments[i__4642__auto___689]));

var G__690 = (i__4642__auto___689 + (1));
i__4642__auto___689 = G__690;
continue;
} else {
}
break;
}

var argseq__4648__auto__ = ((((0) < args__4647__auto__.length))?(new cljs.core.IndexedSeq(args__4647__auto__.slice((0)),(0),null)):null);
return cfe.common.back.cljs$core$IFn$_invoke$arity$variadic(argseq__4648__auto__);
});

cfe.common.back.cljs$core$IFn$_invoke$arity$variadic = (function (args){
return new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [new cljs.core.Keyword(null,"a","a",-2123407586),new cljs.core.PersistentArrayMap(null, 2, [new cljs.core.Keyword(null,"href","href",-793805698),"#",new cljs.core.Keyword(null,"on-click","on-click",1632826543),(function (){
return cljs.core.swap_BANG_.call(null,cfe.common.state,cfe.common.back_0);
})], null),"Back"], null);
});

cfe.common.back.cljs$lang$maxFixedArity = (0);

/** @this {Function} */
cfe.common.back.cljs$lang$applyTo = (function (seq687){
var self__4629__auto__ = this;
return self__4629__auto__.cljs$core$IFn$_invoke$arity$variadic(cljs.core.seq.call(null,seq687));
});


//# sourceMappingURL=common.js.map
