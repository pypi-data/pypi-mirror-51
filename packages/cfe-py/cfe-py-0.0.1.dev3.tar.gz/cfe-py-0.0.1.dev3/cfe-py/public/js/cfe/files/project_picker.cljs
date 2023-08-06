(ns cfe.files.project-picker
  (:require [reagent.core :as r]
            [cfe.common :refer [state  switch-screen back]]
            [cfe.files.file-listing :as file-listing]))

(defn connect-to-project
  [_]
  (file-listing/load-files)
  (switch-screen file-listing/file-list-screen))

(defn project-changed
  [event] 
  (swap! state assoc :project-address (.-value (.-target event))))

(defn start
  [] 
  [:div
   [:label {:for "address"} "Server address"]
   [:input#address
    {:type "text"
     :name "address"
     :value (@state :project-address)
     :on-change project-changed}]
   [:button
    {:on-click connect-to-project}
    "Connect"]])
