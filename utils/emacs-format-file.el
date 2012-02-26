;;; File: emacs-format-file.el
;;; Description: use this for batch indentation with emacs (see indent.sh)
;;; Author: Romain Goffe
;;; Date: 27/10/2010
;;; Commentary: based on the work of Stan Warford (emacs-format-mode) and Scott Andrew Borton (indent-mode)

(defun songbook-indent-line ()
  "Indent current line as SONGBOOK code."
  (interactive)
  (beginning-of-line)
  (if (bobp)
      (indent-line-to 0)	   ; First line is always non-indented
    (let ((not-indented t) cur-indent)
      (if (looking-at "^[ \t]*\\(\\\\end\\)") ; If the line we are looking at is the end of a block, then decrease the indentation
	  (progn
	    (save-excursion
	      (forward-line -1)
	      (setq cur-indent (- (current-indentation) 2)))
	    (if (< cur-indent 0) ; We can't indent past the left margin
		(setq cur-indent 0)))
	(save-excursion
	  (while not-indented ; Iterate backwards until we find an indentation hint
	    (forward-line -1)
	    (if (looking-at "^[ \t]*\\(\\\\end\\)") ; This hint indicates that we need to indent at the level of the END_ token
		(progn
		  (setq cur-indent (current-indentation))
		  (setq not-indented nil))
	      (if (looking-at "^[ \t]*\\(\\\\begin\\)") ; This hint indicates that we need to indent an extra level
		  (progn
		    (setq cur-indent (+ (current-indentation) 2)) ; Do the actual indenting
		    (setq not-indented nil))
		(if (bobp)
		    (setq not-indented nil)))))))
      (if cur-indent
	  (indent-line-to cur-indent)
	(indent-line-to 0))))) ; If we didn't see an indentation hint, then allow no indentation

(defun emacs-format-function ()
  "Format the whole buffer."
  (set (make-local-variable 'indent-line-function) 'songbook-indent-line)  
  (indent-region (point-min) (point-max) nil)
  (untabify (point-min) (point-max))
  (save-buffer)
  )
