Rem manually performs "make clean"
FOR %%A IN (*.aux *.d *.toc *.out *.log *.nav *.snm *.sbx *.sxd) DO DEL %%A
Rem remove temporary covers
FOR %%A IN (covers\*.*) DO DEL %%A
