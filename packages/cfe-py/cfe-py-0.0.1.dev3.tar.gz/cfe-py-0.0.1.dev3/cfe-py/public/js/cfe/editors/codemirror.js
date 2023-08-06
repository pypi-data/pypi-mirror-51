// Compiled by ClojureScript 1.10.439 {}
goog.provide('cfe.editors.codemirror');
goog.require('cljs.core');
goog.require('reagent.core');
goog.require('cfe.common');
goog.require('cljsjs.codemirror');
goog.require('cljsjs.parinfer');
goog.require('cljsjs.parinfer_codemirror');
cfe.editors.codemirror.editor_content = reagent.core.atom.call(null,null);
cfe.editors.codemirror.save_file = reagent.core.atom.call(null,null);
cfe.editors.codemirror.load_content = (function cfe$editors$codemirror$load_content(content,save_fn){
cljs.core.reset_BANG_.call(null,cfe.editors.codemirror.editor_content,content);

return cljs.core.reset_BANG_.call(null,cfe.editors.codemirror.save_file,save_fn);
});
cfe.editors.codemirror.mode = (function cfe$editors$codemirror$mode(){
return "clojure";
});
cfe.editors.codemirror.code_mirror = (function cfe$editors$codemirror$code_mirror(value_atom){
var cm = cljs.core.atom.call(null,null);
return reagent.core.create_class.call(null,new cljs.core.PersistentArrayMap(null, 3, [new cljs.core.Keyword(null,"component-did-mount","component-did-mount",-1126910518),((function (cm){
return (function (this$){
var inst = (new CodeMirror(reagent.core.dom_node.call(null,this$),cljs.core.clj__GT_js.call(null,new cljs.core.PersistentArrayMap(null, 8, [new cljs.core.Keyword(null,"lineNumbers","lineNumbers",1374890941),false,new cljs.core.Keyword(null,"viewportMargin","viewportMargin",948056881),Infinity,new cljs.core.Keyword(null,"matchBrackets","matchBrackets",1256448936),true,new cljs.core.Keyword(null,"autofocus","autofocus",-712814732),true,new cljs.core.Keyword(null,"value","value",305978217),cljs.core.deref.call(null,value_atom),new cljs.core.Keyword(null,"autoCloseBrackets","autoCloseBrackets",1157493311),true,new cljs.core.Keyword(null,"lineWrapping","lineWrapping",1248501985),true,new cljs.core.Keyword(null,"mode","mode",654403691),cfe.editors.codemirror.mode.call(null)], null))));
cljs.core.reset_BANG_.call(null,cm,inst);

parinferCodeMirror.init(inst,"smart");

return inst.on("change",((function (inst,cm){
return (function (){
var value = inst.getValue();
if(cljs.core._EQ_.call(null,value,cljs.core.deref.call(null,value_atom))){
return null;
} else {
return cljs.core.reset_BANG_.call(null,value_atom,value);
}
});})(inst,cm))
);
});})(cm))
,new cljs.core.Keyword(null,"component-did-update","component-did-update",-1468549173),((function (cm){
return (function (this$,old_argv){
if(cljs.core._EQ_.call(null,cljs.core.deref.call(null,value_atom),cljs.core.deref.call(null,cm).getValue())){
return null;
} else {
cljs.core.deref.call(null,cm).setValue(cljs.core.deref.call(null,value_atom));

var last_line = cljs.core.deref.call(null,cm).lastLine();
var last_ch = cljs.core.count.call(null,cljs.core.deref.call(null,cm).getLine(last_line));
return cljs.core.deref.call(null,cm).setCursor(last_line,last_ch);
}
});})(cm))
,new cljs.core.Keyword(null,"reagent-render","reagent-render",-985383853),((function (cm){
return (function (_,___$1,___$2){
cljs.core.deref.call(null,value_atom);

return new cljs.core.PersistentVector(null, 1, 5, cljs.core.PersistentVector.EMPTY_NODE, [new cljs.core.Keyword(null,"div","div",1057191632)], null);
});})(cm))
], null));
});
cfe.editors.codemirror.save = (function cfe$editors$codemirror$save(){
return new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [new cljs.core.Keyword(null,"button","button",1456579943),new cljs.core.PersistentArrayMap(null, 1, [new cljs.core.Keyword(null,"on-click","on-click",1632826543),(function (){
return cljs.core.deref.call(null,cfe.editors.codemirror.save_file).call(null,cljs.core.deref.call(null,cfe.editors.codemirror.editor_content));
})], null),"Save"], null);
});
cfe.editors.codemirror.editor_screen = (function cfe$editors$codemirror$editor_screen(){
return new cljs.core.PersistentVector(null, 5, 5, cljs.core.PersistentVector.EMPTY_NODE, [new cljs.core.Keyword(null,"div","div",1057191632),cfe.common.back.call(null),cfe.editors.codemirror.save.call(null),(cljs.core.truth_(new cljs.core.Keyword(null,"saving-file","saving-file",-689555801).cljs$core$IFn$_invoke$arity$1(cljs.core.deref.call(null,cfe.common.state)))?new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [new cljs.core.Keyword(null,"p","p",151049309),"Saving"], null):null),new cljs.core.PersistentVector(null, 1, 5, cljs.core.PersistentVector.EMPTY_NODE, [cfe.editors.codemirror.code_mirror.call(null,cfe.editors.codemirror.editor_content)], null)], null);
});

//# sourceMappingURL=codemirror.js.map
