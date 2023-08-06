(import hashlib cloudpickle requests math [anarcute[*]] asyncio aiohttp
        os psutil [pegasi[*]] [pandas :as pd])


(setv i 10)



(setv arr (list (range 1500 1570)))
(defn mem[] (-> os (.getpid) psutil.Process (.memory-info) (. rss)))

(defn hash[key]
  (-> key (.encode "utf-8") hashlib.sha224 (.hexdigest)))
(defclass Dash[object]
  
  (defn --init--[self key &optional [api "http://0.0.0.0:8080/cloudpickle/"]]
    
    (setv self.key key
          
          self.api api
          self.hash (hash key)
          ))
  (defn dumps[self x] (-> x cloudpickle.dumps (.decode "latin1")))
  
  
  
  
  (defn legit[self] (self.run (fn[] {"code" 200 "status" "OK"})))
  (defn run[self f &optional [args []] [kwargs {}][star True][pickled False]] 
    (do 
      (setv f (if pickled f (self.dumps f)))
      (-> (requests.get self.api :params {"f" f "args" (self.dumps (if star args [args])) "kwargs" (self.dumps kwargs)
                                          "hash" self.hash}) 
          (.json)  )
      
      ))
  (defn map-a[self f args &optional [processes 80] [star False]]
    (setv f (self.dumps f))
    (setv r (get_map (* (len args) [self.api]) :params (list (map (fn[a]{"f" f "args" (self.dumps (if star a [a]))
                                                                         "hash" self.hash}) args))))
    (list (map (fn[x](try (json.loads x) (except[Exception]{"status" "error" "message" x}))) r))
    
    )
  (defn map[self f args &optional [processes 80] [star False]]
    (setv processes (if processes processes (len args)))
    (setv r (mapp (fn[a] (self.run (self.dumps f) :args a :star star )) args :processes processes))
    `(list (map (fn[x] (.json x)) r))
    r)
  
  
  (defn *map[self &rest args &kwargs kwargs] (self.map #*args #**kwargs :star True))
  (setv starmap *map)
  (defn filter[self f arr &rest args &kwargs kwargs]
    (setv res (self.map f arr #*args #**kwargs))
    (as-> (list (zip arr res)) it (filter last it) (map first it) (list it))))

