(import [anarcute.lib[*]])
(require[anarcute.lib[*]])
(import [luminati :as lm])
(import requests sys json)
(import [selectolax.parser[HTMLParser]])
(setv review-meta-template "https://reviewmeta.com/amazon/{}")
(setv LIMIT 1)
(defn parse[url &optional [session None]]
  (setv session (if session session requests))
  (setv lax (-> url session.get (. text) HTMLParser))
  
  (setv breadcrumbs (-> lax (.css-first "#state_built div.container div") (.css "a") (#map #%(.text %1))))
  (setv name (-> lax (.css-first "[itemprop=name]") (.text)))
  (setv brand (-> lax (.css-first "#product_name small") (.text) (.split " ") rest (#%(.join " " %1))))
  (setv amazon-rating (-> lax (.css-first ".orig-rating-dim") (.text) (.split "/") first))
  (setv amazon-reviews-count (-> lax (.css-first ".orig-rtg b") (.text)))
  (setv adjusted-rating (-> lax (.css-first "#adjusted_rating_location [itemprop=ratingValue]") (.text)))
  (setv adjusted-reviews-count (-> lax (.css-first "#adjusted_rating_location [itemprop=ratingCount]") (.text)))
  (setv pass (-> lax (.css ".pass-badge") rest (#map #%(-> %1 (. parent) (.text) trim (.split "PASS ") last (.split "Pass ") last (.split "\t") first)) ))
  (setv fail (-> lax (.css ".fail-badge") rest (#map #%(-> %1 (. parent) (.text) trim (.split "FAIL ") last (.split "Fail ") last (.split "\t") first)) ))
  (setv amazon-reviews-short (-> lax (.css "#sample_reviews")
                                 (#map #%(, (-> %1 (.css-first ".show-title") (.text)) (-> %1 (.css-first ".show-actual-review") (.text) trim (replace {"\t" ""}) (.split " ... [Go to full review]") first (.split "[Go to full review]") first)))))
  (setv res {"url" url "breadcrumbs" breadcrumbs "name" name "brand" brand "amazon_rating" amazon-rating "amazon_reviews_count" amazon-reviews-count
             "adjusted_rating" adjusted-rating "adjusted_reviews_count"  adjusted-reviews-count "amazon_reviews_short" amazon-reviews-short
             "pass" pass "fail" fail})
  res
  )
(if (= --name-- "__main__")
  (do
    (print (json.dumps (parse (get sys.argv 1))))))
