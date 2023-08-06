(ns cfe.main
  (:require [reagent.core :as r]
            [cfe.common :refer [state switch-screen]]
            [cfe.files.project-picker :as project-picker]))

(defn wrapper
  [props] ((@state :active-screen)))

(defn main
  [] 
  (r/render 
   [wrapper]
   (.appendChild
    (.-body js/document)
    (.createElement js/document "div"))))

(defn loading
  [] [:p "Loading..."])

(switch-screen loading)

(.setTimeout js/window
  (fn [] (switch-screen project-picker/start))
  1000)

(main)