// Compiled by ClojureScript 1.10.439 {}
goog.provide('cfe.files.file_viewer');
goog.require('cljs.core');
goog.require('reagent.core');
goog.require('cfe.common');
goog.require('clojure.string');
goog.require('cljs_http.client');
goog.require('cljs.core.async');
goog.require('cfe.editors.codemirror');
cfe.files.file_viewer.load_file = (function cfe$files$file_viewer$load_file(file){
cljs.core.swap_BANG_.call(null,cfe.common.state,cljs.core.assoc,new cljs.core.Keyword(null,"file-content","file-content",-1595262238),null,new cljs.core.Keyword(null,"file-loaded","file-loaded",-1556708244),file,new cljs.core.Keyword(null,"loading-file","loading-file",-381923221),true);

var c__2336__auto__ = cljs.core.async.chan.call(null,(1));
cljs.core.async.impl.dispatch.run.call(null,((function (c__2336__auto__){
return (function (){
var f__2337__auto__ = (function (){var switch__2313__auto__ = ((function (c__2336__auto__){
return (function (state_2426){
var state_val_2427 = (state_2426[(1)]);
if((state_val_2427 === (1))){
var inst_2414 = cljs.core.deref.call(null,cfe.common.state);
var inst_2415 = inst_2414.call(null,new cljs.core.Keyword(null,"project-address","project-address",360976148));
var inst_2416 = [cljs.core.str.cljs$core$IFn$_invoke$arity$1(inst_2415),"?file=",cljs.core.str.cljs$core$IFn$_invoke$arity$1(file)].join('');
var inst_2417 = [new cljs.core.Keyword(null,"with-credentials?","with-credentials?",-1773202222)];
var inst_2418 = [false];
var inst_2419 = cljs.core.PersistentHashMap.fromArrays(inst_2417,inst_2418);
var inst_2420 = cljs_http.client.get.call(null,inst_2416,inst_2419);
var state_2426__$1 = state_2426;
return cljs.core.async.impl.ioc_helpers.take_BANG_.call(null,state_2426__$1,(2),inst_2420);
} else {
if((state_val_2427 === (2))){
var inst_2422 = (state_2426[(2)]);
var inst_2423 = new cljs.core.Keyword(null,"body","body",-2049205669).cljs$core$IFn$_invoke$arity$1(inst_2422);
var inst_2424 = cljs.core.swap_BANG_.call(null,cfe.common.state,cljs.core.assoc,new cljs.core.Keyword(null,"loading-file","loading-file",-381923221),false,new cljs.core.Keyword(null,"file-content","file-content",-1595262238),inst_2423);
var state_2426__$1 = state_2426;
return cljs.core.async.impl.ioc_helpers.return_chan.call(null,state_2426__$1,inst_2424);
} else {
return null;
}
}
});})(c__2336__auto__))
;
return ((function (switch__2313__auto__,c__2336__auto__){
return (function() {
var cfe$files$file_viewer$load_file_$_state_machine__2314__auto__ = null;
var cfe$files$file_viewer$load_file_$_state_machine__2314__auto____0 = (function (){
var statearr_2428 = [null,null,null,null,null,null,null];
(statearr_2428[(0)] = cfe$files$file_viewer$load_file_$_state_machine__2314__auto__);

(statearr_2428[(1)] = (1));

return statearr_2428;
});
var cfe$files$file_viewer$load_file_$_state_machine__2314__auto____1 = (function (state_2426){
while(true){
var ret_value__2315__auto__ = (function (){try{while(true){
var result__2316__auto__ = switch__2313__auto__.call(null,state_2426);
if(cljs.core.keyword_identical_QMARK_.call(null,result__2316__auto__,new cljs.core.Keyword(null,"recur","recur",-437573268))){
continue;
} else {
return result__2316__auto__;
}
break;
}
}catch (e2429){if((e2429 instanceof Object)){
var ex__2317__auto__ = e2429;
var statearr_2430_2432 = state_2426;
(statearr_2430_2432[(5)] = ex__2317__auto__);


cljs.core.async.impl.ioc_helpers.process_exception.call(null,state_2426);

return new cljs.core.Keyword(null,"recur","recur",-437573268);
} else {
throw e2429;

}
}})();
if(cljs.core.keyword_identical_QMARK_.call(null,ret_value__2315__auto__,new cljs.core.Keyword(null,"recur","recur",-437573268))){
var G__2433 = state_2426;
state_2426 = G__2433;
continue;
} else {
return ret_value__2315__auto__;
}
break;
}
});
cfe$files$file_viewer$load_file_$_state_machine__2314__auto__ = function(state_2426){
switch(arguments.length){
case 0:
return cfe$files$file_viewer$load_file_$_state_machine__2314__auto____0.call(this);
case 1:
return cfe$files$file_viewer$load_file_$_state_machine__2314__auto____1.call(this,state_2426);
}
throw(new Error('Invalid arity: ' + arguments.length));
};
cfe$files$file_viewer$load_file_$_state_machine__2314__auto__.cljs$core$IFn$_invoke$arity$0 = cfe$files$file_viewer$load_file_$_state_machine__2314__auto____0;
cfe$files$file_viewer$load_file_$_state_machine__2314__auto__.cljs$core$IFn$_invoke$arity$1 = cfe$files$file_viewer$load_file_$_state_machine__2314__auto____1;
return cfe$files$file_viewer$load_file_$_state_machine__2314__auto__;
})()
;})(switch__2313__auto__,c__2336__auto__))
})();
var state__2338__auto__ = (function (){var statearr_2431 = f__2337__auto__.call(null);
(statearr_2431[(6)] = c__2336__auto__);

return statearr_2431;
})();
return cljs.core.async.impl.ioc_helpers.run_state_machine_wrapped.call(null,state__2338__auto__);
});})(c__2336__auto__))
);

return c__2336__auto__;
});
cfe.files.file_viewer.save_file = (function cfe$files$file_viewer$save_file(content){
cljs.core.swap_BANG_.call(null,cfe.common.state,cljs.core.assoc,new cljs.core.Keyword(null,"saving-file","saving-file",-689555801),true);

var c__2336__auto__ = cljs.core.async.chan.call(null,(1));
cljs.core.async.impl.dispatch.run.call(null,((function (c__2336__auto__){
return (function (){
var f__2337__auto__ = (function (){var switch__2313__auto__ = ((function (c__2336__auto__){
return (function (state_2450){
var state_val_2451 = (state_2450[(1)]);
if((state_val_2451 === (1))){
var inst_2434 = cljs.core.deref.call(null,cfe.common.state);
var inst_2435 = inst_2434.call(null,new cljs.core.Keyword(null,"project-address","project-address",360976148));
var inst_2436 = cljs.core.deref.call(null,cfe.common.state);
var inst_2437 = new cljs.core.Keyword(null,"file-loaded","file-loaded",-1556708244).cljs$core$IFn$_invoke$arity$1(inst_2436);
var inst_2438 = [cljs.core.str.cljs$core$IFn$_invoke$arity$1(inst_2435),"?file=",cljs.core.str.cljs$core$IFn$_invoke$arity$1(inst_2437)].join('');
var inst_2439 = [new cljs.core.Keyword(null,"with-credentials?","with-credentials?",-1773202222),new cljs.core.Keyword(null,"headers","headers",-835030129),new cljs.core.Keyword(null,"body","body",-2049205669)];
var inst_2440 = ["Content-Type"];
var inst_2441 = ["text/plain"];
var inst_2442 = cljs.core.PersistentHashMap.fromArrays(inst_2440,inst_2441);
var inst_2443 = [false,inst_2442,content];
var inst_2444 = cljs.core.PersistentHashMap.fromArrays(inst_2439,inst_2443);
var inst_2445 = cljs_http.client.post.call(null,inst_2438,inst_2444);
var state_2450__$1 = state_2450;
return cljs.core.async.impl.ioc_helpers.take_BANG_.call(null,state_2450__$1,(2),inst_2445);
} else {
if((state_val_2451 === (2))){
var inst_2447 = (state_2450[(2)]);
var inst_2448 = cljs.core.swap_BANG_.call(null,cfe.common.state,cljs.core.assoc,new cljs.core.Keyword(null,"saving-file","saving-file",-689555801),false);
var state_2450__$1 = (function (){var statearr_2452 = state_2450;
(statearr_2452[(7)] = inst_2447);

return statearr_2452;
})();
return cljs.core.async.impl.ioc_helpers.return_chan.call(null,state_2450__$1,inst_2448);
} else {
return null;
}
}
});})(c__2336__auto__))
;
return ((function (switch__2313__auto__,c__2336__auto__){
return (function() {
var cfe$files$file_viewer$save_file_$_state_machine__2314__auto__ = null;
var cfe$files$file_viewer$save_file_$_state_machine__2314__auto____0 = (function (){
var statearr_2453 = [null,null,null,null,null,null,null,null];
(statearr_2453[(0)] = cfe$files$file_viewer$save_file_$_state_machine__2314__auto__);

(statearr_2453[(1)] = (1));

return statearr_2453;
});
var cfe$files$file_viewer$save_file_$_state_machine__2314__auto____1 = (function (state_2450){
while(true){
var ret_value__2315__auto__ = (function (){try{while(true){
var result__2316__auto__ = switch__2313__auto__.call(null,state_2450);
if(cljs.core.keyword_identical_QMARK_.call(null,result__2316__auto__,new cljs.core.Keyword(null,"recur","recur",-437573268))){
continue;
} else {
return result__2316__auto__;
}
break;
}
}catch (e2454){if((e2454 instanceof Object)){
var ex__2317__auto__ = e2454;
var statearr_2455_2457 = state_2450;
(statearr_2455_2457[(5)] = ex__2317__auto__);


cljs.core.async.impl.ioc_helpers.process_exception.call(null,state_2450);

return new cljs.core.Keyword(null,"recur","recur",-437573268);
} else {
throw e2454;

}
}})();
if(cljs.core.keyword_identical_QMARK_.call(null,ret_value__2315__auto__,new cljs.core.Keyword(null,"recur","recur",-437573268))){
var G__2458 = state_2450;
state_2450 = G__2458;
continue;
} else {
return ret_value__2315__auto__;
}
break;
}
});
cfe$files$file_viewer$save_file_$_state_machine__2314__auto__ = function(state_2450){
switch(arguments.length){
case 0:
return cfe$files$file_viewer$save_file_$_state_machine__2314__auto____0.call(this);
case 1:
return cfe$files$file_viewer$save_file_$_state_machine__2314__auto____1.call(this,state_2450);
}
throw(new Error('Invalid arity: ' + arguments.length));
};
cfe$files$file_viewer$save_file_$_state_machine__2314__auto__.cljs$core$IFn$_invoke$arity$0 = cfe$files$file_viewer$save_file_$_state_machine__2314__auto____0;
cfe$files$file_viewer$save_file_$_state_machine__2314__auto__.cljs$core$IFn$_invoke$arity$1 = cfe$files$file_viewer$save_file_$_state_machine__2314__auto____1;
return cfe$files$file_viewer$save_file_$_state_machine__2314__auto__;
})()
;})(switch__2313__auto__,c__2336__auto__))
})();
var state__2338__auto__ = (function (){var statearr_2456 = f__2337__auto__.call(null);
(statearr_2456[(6)] = c__2336__auto__);

return statearr_2456;
})();
return cljs.core.async.impl.ioc_helpers.run_state_machine_wrapped.call(null,state__2338__auto__);
});})(c__2336__auto__))
);

return c__2336__auto__;
});
cfe.files.file_viewer.render_file = (function cfe$files$file_viewer$render_file(content){
return new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [new cljs.core.Keyword(null,"pre","pre",2118456869),content], null);
});
cfe.files.file_viewer.cm_edit = (function cfe$files$file_viewer$cm_edit(){
cfe.editors.codemirror.load_content.call(null,cljs.core.deref.call(null,cfe.common.state).call(null,new cljs.core.Keyword(null,"file-content","file-content",-1595262238)),cfe.files.file_viewer.save_file);

return cfe.common.switch_screen.call(null,cfe.editors.codemirror.editor_screen);
});
cfe.files.file_viewer.buttons = (function cfe$files$file_viewer$buttons(){
return new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [new cljs.core.Keyword(null,"div","div",1057191632),new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [new cljs.core.Keyword(null,"button","button",1456579943),new cljs.core.PersistentArrayMap(null, 1, [new cljs.core.Keyword(null,"on-click","on-click",1632826543),cfe.files.file_viewer.cm_edit], null),"Edit"], null)], null);
});
cfe.files.file_viewer.file_screen = (function cfe$files$file_viewer$file_screen(){
return new cljs.core.PersistentVector(null, 6, 5, cljs.core.PersistentVector.EMPTY_NODE, [new cljs.core.Keyword(null,"div","div",1057191632),cfe.common.back.call(null),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [new cljs.core.Keyword(null,"h1","h1",-1896887462),cljs.core.deref.call(null,cfe.common.state).call(null,new cljs.core.Keyword(null,"file-loaded","file-loaded",-1556708244))], null),cfe.files.file_viewer.buttons.call(null),(cljs.core.truth_(cljs.core.deref.call(null,cfe.common.state).call(null,new cljs.core.Keyword(null,"loading-file","loading-file",-381923221)))?new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [new cljs.core.Keyword(null,"p","p",151049309),"Loading..."], null):null),cfe.files.file_viewer.render_file.call(null,cljs.core.deref.call(null,cfe.common.state).call(null,new cljs.core.Keyword(null,"file-content","file-content",-1595262238)))], null);
});

//# sourceMappingURL=file_viewer.js.map
