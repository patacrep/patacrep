#!/bin/sh

# volume-2.sgl generation
ls -1 songs/*/*.sg > tmp ;
grep -vf volume-1.sgl tmp > volume-2.sgl ;

