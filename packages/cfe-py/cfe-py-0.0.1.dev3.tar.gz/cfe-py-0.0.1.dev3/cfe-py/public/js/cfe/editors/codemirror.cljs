(ns cfe.editors.codemirror
  (:require [reagent.core :as r]
            [cfe.common :refer [state back switch-screen]]
            [cljsjs.codemirror]
            [cljsjs.parinfer]
            [cljsjs.parinfer-codemirror]))

(def editor-content (r/atom nil))
(def save-file (r/atom nil))

(defn load-content
  [content save-fn]
   (reset! editor-content content)
   (reset! save-file save-fn))

(defn mode
  [] "clojure")

(defn code-mirror
  [value-atom]
  (let [cm (atom nil)]
    (r/create-class
     {:component-did-mount
      (fn [this]
        (let [inst (js/CodeMirror. 
                    (r/dom-node this)
                    (clj->js 
                     {:lineNumbers false
                      :viewportMargin js/Infinity
                      :matchBrackets true
                      :autofocus true
                      :value @value-atom
                      :autoCloseBrackets true
                      :lineWrapping true
                      :mode (mode)}))]
          (reset! cm inst)
          (js/parinferCodeMirror.init inst "smart")
          (.on inst "change"
               (fn []
                 (let [value (.getValue inst)]
                   (when-not (= value @value-atom)
                     (reset! value-atom value)))))))

      :component-did-update
      (fn [this old-argv]
        (when-not (= @value-atom (.getValue @cm))
          (.setValue @cm @value-atom)
          ;; reset the cursor to the end of the text, if the text was changed externally
          (let [last-line (.lastLine @cm)
                last-ch (count (.getLine @cm last-line))]
            (.setCursor @cm last-line last-ch))))

      :reagent-render
      (fn [_ _ _]
        @value-atom
        [:div ])})))

(defn save
  [] 
  [:button
   {:on-click #(@save-file @editor-content)}
   "Save"])

(defn editor-screen
  []
 [:div
  (back)
  (save)
  (when (:saving-file @state) [:p "Saving"])
  [(code-mirror editor-content)]])