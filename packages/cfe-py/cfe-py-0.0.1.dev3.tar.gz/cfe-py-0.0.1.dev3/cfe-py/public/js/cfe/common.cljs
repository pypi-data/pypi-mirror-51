(ns cfe.common
  (:require [reagent.core :as r]))

(def state 
  (r/atom 
   {:project-address (.-origin js/location)
    :active-screen nil
    :previous-screens []}))

(defn switch-screen-0
  [to state] 
  (assoc state
         :active-screen to
         :previous-screens (cons (:active-screen state) (:previous-screens state))))

(defn switch-screen
  [to]
  (swap! state (partial switch-screen-0 to)))

(defn back-0
  [state] 
  (assoc state
         :active-screen (first (:previous-screens state))
         :previous-screens (rest (:previous-screens state))))

(defn back
  [ & args ] 
  [:a 
   {:href "#"
    :on-click
    #(swap! state back-0)}
   "Back"])


