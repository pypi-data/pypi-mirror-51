(import json [pandas :as pd] [fbprophet [Prophet]] datetime)
(import [anarcute[*]])
(require [anarcute.lib[*]])
(defn predict-next [enumerated n &optional [all False][values thru][freq "MS"][interval-width 0.95]]
 
  (setv ts (do
             (setv ts [])
             (for [(, k v) enumerated]
               (ts.append {"ds" k  "y" v}))
             (pd.DataFrame.from-dict ts)))
  (setv m (Prophet :interval-width interval-width))
  (m.fit ts)
  (setv future (m.make-future-dataframe :periods n :freq freq))
  (setv prediction (m.predict future))
  (setv prediction (-> prediction (get ["ds" "yhat"]) (.as-matrix) list (#%(if all %1 (get %1 (slice (* -1 n) None))))))
  (setv prediction (do  
                     (for [row prediction]
                       (assoc row 0 (.strftime (get row 0) "%Y-%m-%d"))
                       (assoc row -1 (round (values (get row -1)) 2))) prediction))
  (#map list prediction))