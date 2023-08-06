(ns cfe.files.file-viewer
  (:require-macros [cljs.core.async.macros :refer [go]])
  (:require [reagent.core :as r]
            [cfe.common :refer [state back switch-screen]]
            [clojure.string :as s]
            [cljs-http.client :as http]
            [cljs.core.async :refer [<!]]
            [cfe.editors.codemirror :as cm]))

(defn load-file
  [file]
  (swap! state assoc 
         :file-content nil
         :file-loaded file
         :loading-file true)
  (go
    (swap! state assoc 
           :loading-file false
           :file-content
            (:body
             (<! (http/get (str (@state :project-address) "?file=" file)
                           {:with-credentials? false}))))))

(defn save-file
  [content]
  (swap! state assoc :saving-file true)
  (go
    (<! (http/post (str (@state :project-address) "?file=" (:file-loaded @state))
                   {:with-credentials? false
                    :headers {"Content-Type" "text/plain"}
                    :body content}))
    (swap! state assoc :saving-file false)))

(defn render-file
  [content]
  [:pre content])

(defn cm-edit
  []
  (cm/load-content (@state :file-content) save-file)
  (switch-screen cm/editor-screen))

(defn buttons
  [] 
  [:div 
   [:button 
    {:on-click cm-edit}
    "Edit"]])

(defn file-screen
  []
  [:div
   (back)
   [:h1 (@state :file-loaded)]
   (buttons)
   (when (@state :loading-file) [:p "Loading..."])
   (render-file  (@state :file-content))])

