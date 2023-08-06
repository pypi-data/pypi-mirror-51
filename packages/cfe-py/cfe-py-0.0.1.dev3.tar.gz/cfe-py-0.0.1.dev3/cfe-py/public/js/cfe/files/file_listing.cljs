(ns cfe.files.file-listing
  (:require-macros [cljs.core.async.macros :refer [go]])
  (:require [reagent.core :as r]
            [cfe.common :refer [state  switch-screen back]]
            [clojure.string :as s]
            [cljs-http.client :as http]
            [cljs.core.async :refer [<!]]
            [cfe.files.file-viewer :as file-viewer]))

(defn root-folder
  [file]
  (first (butlast (s/split (:path file) "/"))))

(defn clj?
  [file]
  (and
   (or
    (= (root-folder file) nil)
    (= (root-folder file) "src"))
   (or
    (s/ends-with? (:name file) ".clj")
    (s/ends-with? (:name file) ".cljs")
    (s/ends-with? (:name file) ".edn"))))

(defn load-files
  []
  (swap! state assoc :loading-files true)
  (go
    (swap! state assoc 
           :loading-files false
           :loaded-files
           (:files 
            (:body
             (<! (http/get (str (@state :project-address) "/files")
                           {:with-credentials? false})))))))

(defn file-picked
  [file]
  (file-viewer/load-file file)
  (switch-screen file-viewer/file-screen))

(defn file-item
  [file]
  [:a
   {:href "#"
    :on-click #(file-picked file)}
   file])

(defn file-list-screen
  []
  [:div
   (back)
   (when (@state :loading-files) [:p "Loading..."])
   [:ul
    (for [file (@state :loaded-files)]
      ^{:key file}
      [:li
       (file-item file)])]])
