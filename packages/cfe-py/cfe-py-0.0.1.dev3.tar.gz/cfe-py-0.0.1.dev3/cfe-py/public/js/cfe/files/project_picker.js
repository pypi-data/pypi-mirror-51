// Compiled by ClojureScript 1.10.439 {}
goog.provide('cfe.files.project_picker');
goog.require('cljs.core');
goog.require('reagent.core');
goog.require('cfe.common');
goog.require('cfe.files.file_listing');
cfe.files.project_picker.connect_to_project = (function cfe$files$project_picker$connect_to_project(_){
cfe.files.file_listing.load_files.call(null);

return cfe.common.switch_screen.call(null,cfe.files.file_listing.file_list_screen);
});
cfe.files.project_picker.project_changed = (function cfe$files$project_picker$project_changed(event){
return cljs.core.swap_BANG_.call(null,cfe.common.state,cljs.core.assoc,new cljs.core.Keyword(null,"project-address","project-address",360976148),event.target.value);
});
cfe.files.project_picker.start = (function cfe$files$project_picker$start(){
return new cljs.core.PersistentVector(null, 4, 5, cljs.core.PersistentVector.EMPTY_NODE, [new cljs.core.Keyword(null,"div","div",1057191632),new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [new cljs.core.Keyword(null,"label","label",1718410804),new cljs.core.PersistentArrayMap(null, 1, [new cljs.core.Keyword(null,"for","for",-1323786319),"address"], null),"Server address"], null),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [new cljs.core.Keyword(null,"input#address","input#address",-780963222),new cljs.core.PersistentArrayMap(null, 4, [new cljs.core.Keyword(null,"type","type",1174270348),"text",new cljs.core.Keyword(null,"name","name",1843675177),"address",new cljs.core.Keyword(null,"value","value",305978217),cljs.core.deref.call(null,cfe.common.state).call(null,new cljs.core.Keyword(null,"project-address","project-address",360976148)),new cljs.core.Keyword(null,"on-change","on-change",-732046149),cfe.files.project_picker.project_changed], null)], null),new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [new cljs.core.Keyword(null,"button","button",1456579943),new cljs.core.PersistentArrayMap(null, 1, [new cljs.core.Keyword(null,"on-click","on-click",1632826543),cfe.files.project_picker.connect_to_project], null),"Connect"], null)], null);
});

//# sourceMappingURL=project_picker.js.map
