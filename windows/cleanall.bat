Rem remove pdf files
FOR %%A IN (*.pdf) DO DEL %%A
Rem manually performs "make cleanall"
windows\\clean.bat
