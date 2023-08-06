// Compiled by ClojureScript 1.10.439 {}
goog.provide('cfe.files.file_listing');
goog.require('cljs.core');
goog.require('reagent.core');
goog.require('cfe.common');
goog.require('clojure.string');
goog.require('cljs_http.client');
goog.require('cljs.core.async');
goog.require('cfe.files.file_viewer');
cfe.files.file_listing.root_folder = (function cfe$files$file_listing$root_folder(file){
return cljs.core.first.call(null,cljs.core.butlast.call(null,clojure.string.split.call(null,new cljs.core.Keyword(null,"path","path",-188191168).cljs$core$IFn$_invoke$arity$1(file),"/")));
});
cfe.files.file_listing.clj_QMARK_ = (function cfe$files$file_listing$clj_QMARK_(file){
return ((((cljs.core._EQ_.call(null,cfe.files.file_listing.root_folder.call(null,file),null)) || (cljs.core._EQ_.call(null,cfe.files.file_listing.root_folder.call(null,file),"src")))) && (((clojure.string.ends_with_QMARK_.call(null,new cljs.core.Keyword(null,"name","name",1843675177).cljs$core$IFn$_invoke$arity$1(file),".clj")) || (clojure.string.ends_with_QMARK_.call(null,new cljs.core.Keyword(null,"name","name",1843675177).cljs$core$IFn$_invoke$arity$1(file),".cljs")) || (clojure.string.ends_with_QMARK_.call(null,new cljs.core.Keyword(null,"name","name",1843675177).cljs$core$IFn$_invoke$arity$1(file),".edn")))));
});
cfe.files.file_listing.load_files = (function cfe$files$file_listing$load_files(){
cljs.core.swap_BANG_.call(null,cfe.common.state,cljs.core.assoc,new cljs.core.Keyword(null,"loading-files","loading-files",-611285064),true);

var c__2336__auto__ = cljs.core.async.chan.call(null,(1));
cljs.core.async.impl.dispatch.run.call(null,((function (c__2336__auto__){
return (function (){
var f__2337__auto__ = (function (){var switch__2313__auto__ = ((function (c__2336__auto__){
return (function (state_2474){
var state_val_2475 = (state_2474[(1)]);
if((state_val_2475 === (1))){
var inst_2461 = cljs.core.deref.call(null,cfe.common.state);
var inst_2462 = inst_2461.call(null,new cljs.core.Keyword(null,"project-address","project-address",360976148));
var inst_2463 = [cljs.core.str.cljs$core$IFn$_invoke$arity$1(inst_2462),"/files"].join('');
var inst_2464 = [new cljs.core.Keyword(null,"with-credentials?","with-credentials?",-1773202222)];
var inst_2465 = [false];
var inst_2466 = cljs.core.PersistentHashMap.fromArrays(inst_2464,inst_2465);
var inst_2467 = cljs_http.client.get.call(null,inst_2463,inst_2466);
var state_2474__$1 = state_2474;
return cljs.core.async.impl.ioc_helpers.take_BANG_.call(null,state_2474__$1,(2),inst_2467);
} else {
if((state_val_2475 === (2))){
var inst_2469 = (state_2474[(2)]);
var inst_2470 = new cljs.core.Keyword(null,"body","body",-2049205669).cljs$core$IFn$_invoke$arity$1(inst_2469);
var inst_2471 = new cljs.core.Keyword(null,"files","files",-472457450).cljs$core$IFn$_invoke$arity$1(inst_2470);
var inst_2472 = cljs.core.swap_BANG_.call(null,cfe.common.state,cljs.core.assoc,new cljs.core.Keyword(null,"loading-files","loading-files",-611285064),false,new cljs.core.Keyword(null,"loaded-files","loaded-files",-1108283956),inst_2471);
var state_2474__$1 = state_2474;
return cljs.core.async.impl.ioc_helpers.return_chan.call(null,state_2474__$1,inst_2472);
} else {
return null;
}
}
});})(c__2336__auto__))
;
return ((function (switch__2313__auto__,c__2336__auto__){
return (function() {
var cfe$files$file_listing$load_files_$_state_machine__2314__auto__ = null;
var cfe$files$file_listing$load_files_$_state_machine__2314__auto____0 = (function (){
var statearr_2476 = [null,null,null,null,null,null,null];
(statearr_2476[(0)] = cfe$files$file_listing$load_files_$_state_machine__2314__auto__);

(statearr_2476[(1)] = (1));

return statearr_2476;
});
var cfe$files$file_listing$load_files_$_state_machine__2314__auto____1 = (function (state_2474){
while(true){
var ret_value__2315__auto__ = (function (){try{while(true){
var result__2316__auto__ = switch__2313__auto__.call(null,state_2474);
if(cljs.core.keyword_identical_QMARK_.call(null,result__2316__auto__,new cljs.core.Keyword(null,"recur","recur",-437573268))){
continue;
} else {
return result__2316__auto__;
}
break;
}
}catch (e2477){if((e2477 instanceof Object)){
var ex__2317__auto__ = e2477;
var statearr_2478_2480 = state_2474;
(statearr_2478_2480[(5)] = ex__2317__auto__);


cljs.core.async.impl.ioc_helpers.process_exception.call(null,state_2474);

return new cljs.core.Keyword(null,"recur","recur",-437573268);
} else {
throw e2477;

}
}})();
if(cljs.core.keyword_identical_QMARK_.call(null,ret_value__2315__auto__,new cljs.core.Keyword(null,"recur","recur",-437573268))){
var G__2481 = state_2474;
state_2474 = G__2481;
continue;
} else {
return ret_value__2315__auto__;
}
break;
}
});
cfe$files$file_listing$load_files_$_state_machine__2314__auto__ = function(state_2474){
switch(arguments.length){
case 0:
return cfe$files$file_listing$load_files_$_state_machine__2314__auto____0.call(this);
case 1:
return cfe$files$file_listing$load_files_$_state_machine__2314__auto____1.call(this,state_2474);
}
throw(new Error('Invalid arity: ' + arguments.length));
};
cfe$files$file_listing$load_files_$_state_machine__2314__auto__.cljs$core$IFn$_invoke$arity$0 = cfe$files$file_listing$load_files_$_state_machine__2314__auto____0;
cfe$files$file_listing$load_files_$_state_machine__2314__auto__.cljs$core$IFn$_invoke$arity$1 = cfe$files$file_listing$load_files_$_state_machine__2314__auto____1;
return cfe$files$file_listing$load_files_$_state_machine__2314__auto__;
})()
;})(switch__2313__auto__,c__2336__auto__))
})();
var state__2338__auto__ = (function (){var statearr_2479 = f__2337__auto__.call(null);
(statearr_2479[(6)] = c__2336__auto__);

return statearr_2479;
})();
return cljs.core.async.impl.ioc_helpers.run_state_machine_wrapped.call(null,state__2338__auto__);
});})(c__2336__auto__))
);

return c__2336__auto__;
});
cfe.files.file_listing.file_picked = (function cfe$files$file_listing$file_picked(file){
cfe.files.file_viewer.load_file.call(null,file);

return cfe.common.switch_screen.call(null,cfe.files.file_viewer.file_screen);
});
cfe.files.file_listing.file_item = (function cfe$files$file_listing$file_item(file){
return new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [new cljs.core.Keyword(null,"a","a",-2123407586),new cljs.core.PersistentArrayMap(null, 2, [new cljs.core.Keyword(null,"href","href",-793805698),"#",new cljs.core.Keyword(null,"on-click","on-click",1632826543),(function (){
return cfe.files.file_listing.file_picked.call(null,file);
})], null),file], null);
});
cfe.files.file_listing.file_list_screen = (function cfe$files$file_listing$file_list_screen(){
return new cljs.core.PersistentVector(null, 4, 5, cljs.core.PersistentVector.EMPTY_NODE, [new cljs.core.Keyword(null,"div","div",1057191632),cfe.common.back.call(null),(cljs.core.truth_(cljs.core.deref.call(null,cfe.common.state).call(null,new cljs.core.Keyword(null,"loading-files","loading-files",-611285064)))?new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [new cljs.core.Keyword(null,"p","p",151049309),"Loading..."], null):null),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [new cljs.core.Keyword(null,"ul","ul",-1349521403),(function (){var iter__4434__auto__ = (function cfe$files$file_listing$file_list_screen_$_iter__2482(s__2483){
return (new cljs.core.LazySeq(null,(function (){
var s__2483__$1 = s__2483;
while(true){
var temp__5735__auto__ = cljs.core.seq.call(null,s__2483__$1);
if(temp__5735__auto__){
var s__2483__$2 = temp__5735__auto__;
if(cljs.core.chunked_seq_QMARK_.call(null,s__2483__$2)){
var c__4432__auto__ = cljs.core.chunk_first.call(null,s__2483__$2);
var size__4433__auto__ = cljs.core.count.call(null,c__4432__auto__);
var b__2485 = cljs.core.chunk_buffer.call(null,size__4433__auto__);
if((function (){var i__2484 = (0);
while(true){
if((i__2484 < size__4433__auto__)){
var file = cljs.core._nth.call(null,c__4432__auto__,i__2484);
cljs.core.chunk_append.call(null,b__2485,cljs.core.with_meta(new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [new cljs.core.Keyword(null,"li","li",723558921),cfe.files.file_listing.file_item.call(null,file)], null),new cljs.core.PersistentArrayMap(null, 1, [new cljs.core.Keyword(null,"key","key",-1516042587),file], null)));

var G__2486 = (i__2484 + (1));
i__2484 = G__2486;
continue;
} else {
return true;
}
break;
}
})()){
return cljs.core.chunk_cons.call(null,cljs.core.chunk.call(null,b__2485),cfe$files$file_listing$file_list_screen_$_iter__2482.call(null,cljs.core.chunk_rest.call(null,s__2483__$2)));
} else {
return cljs.core.chunk_cons.call(null,cljs.core.chunk.call(null,b__2485),null);
}
} else {
var file = cljs.core.first.call(null,s__2483__$2);
return cljs.core.cons.call(null,cljs.core.with_meta(new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [new cljs.core.Keyword(null,"li","li",723558921),cfe.files.file_listing.file_item.call(null,file)], null),new cljs.core.PersistentArrayMap(null, 1, [new cljs.core.Keyword(null,"key","key",-1516042587),file], null)),cfe$files$file_listing$file_list_screen_$_iter__2482.call(null,cljs.core.rest.call(null,s__2483__$2)));
}
} else {
return null;
}
break;
}
}),null,null));
});
return iter__4434__auto__.call(null,cljs.core.deref.call(null,cfe.common.state).call(null,new cljs.core.Keyword(null,"loaded-files","loaded-files",-1108283956)));
})()], null)], null);
});

//# sourceMappingURL=file_listing.js.map
