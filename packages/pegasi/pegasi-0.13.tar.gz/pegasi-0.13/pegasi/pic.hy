(import hashlib cloudpickle requests math [anarcute[*]]
        os psutil)


(setv i 10)



(setv arr (list (range 1500 1570)))
(defn mem[] (-> os (.getpid) psutil.Process (.memory-info) (. rss)))

(defn hash[key]
  (-> key (.encode "utf-8") hashlib.sha224 (.hexdigest)))
(defclass Dash[object]
  
  (defn --init--[self key]
    (setv self.key key
          self.api "https://cloud-msrhohb4sa-ew.a.run.app/cloudpickle/"
          ; self.api "http://0.0.0.0:8080/cloudpickle/"
          self.hash (hash key)
          ))
  (defn dumps[self x] (-> x cloudpickle.dumps (.decode "latin1")))
  
  (defn run[self f &optional [args []] [kwargs {}][star True]] 
    (do 
      (-> (requests.get self.api :params {"f" (self.dumps f) "args" (self.dumps (if star args [args])) "kwargs" (self.dumps kwargs)
                                          "hash" self.hash})
          (.json)  )
      
      ))
  (defn legit[self] (self.run (fn[] {"code" 200 "status" "OK"})))
  (defn map[self f args &optional [processes None] [star False]]
    (setv processes (if processes processes (len args)))
    (mapp (fn[a] (self.run f :args a :star star)) args))
  
  (defn *map[self &rest args &kwargs kwargs] (self.map #*args #**kwargs :star True))
  (setv starmap *map)
  (defn filter[self f arr &rest args &kwargs kwargs]
    (setv res (self.map f arr #*args #**kwargs))
    (as-> (list (zip arr res)) it (filter last it) (map first it) (list it))))