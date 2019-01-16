(defun issorted (L)
	(if (or (null L) (null (cdr L)))
            T
            (if (< (car L) (car (cdr L)))
                (issorted(cdr L))
                nil)
        )
)

(defun numbers (N)
        (if (>= 0 N)
            nil
            (append (numbers (- N 1)) (cons N nil) )
        )
)

(defun palindrome(G)
        (if (equal(myreverse G) G) T nil))
	
(defun myreverse (L)
      (if (null L)
          L
          (append (myreverse (cdr L))
                  (cons (car L) nil))
      )
)

(defun replace1 (A B L)
    (if (null L)
        null
        (if (equal A L)
            