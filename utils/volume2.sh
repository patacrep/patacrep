#!/bin/sh

# volume-2.sgl generation
ls -1 songs/*/*.sg > tmp ;
grep -vf tmp volume-1.sgl > volume-2.sgl ;
rm -f tmp ;

