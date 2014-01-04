(defproject babble "0.0.69"
  :description "A poopy butt"
  :source-paths ["src-clj"]
  :dependencies [[org.clojure/clojure "1.5.1"]
                 [org.clojure/clojurescript "0.0-2014"
                  :exclusions [org.apache.ant/ant]]
                 [compojure "1.1.6"]
		 [rotary "0.4.0"]
                 [hiccup "1.0.4"]]
  :plugins [[lein-cljsbuild "1.0.1"]
            [lein-ring "0.8.7"]]
  :cljsbuild {
    :builds [{:source-paths ["src-cljs"]
              :compiler {:output-to "resources/public/js/babble.js"
                         :optimizations :whitespace
                         :pretty-print true}}]}
  :ring {:handler example.routes/app})