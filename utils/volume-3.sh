#!/bin/sh
#Author: Romain Goffe
#Date: 07/05/2011
#Description: Generate an sb file containing all the songs that are not 
# already in volume-1 and volume-2

#all songs
cd songs
ls -1 */*.sg > ../res1
cd ..

#get volume 1 list
tail -n +12 volume-1.sb > tmp1
head -n -2 tmp1 > list1
sed -i -e "s/\",//g" -e "s/    \"//g" -e "s/\"//g" list1

#remove volume 1 songs
grep -vf list1 res1 > res2 

#get volume 2 list
tail -n +13 volume-2.sb > tmp2
head -n -2 tmp2 > list2
sed -i -e "s/\",//g" -e "s/    \"//g" -e "s/\"//g" list2

#remove volume 2 songs
grep -vf list2 res2 > res3 

#format song list
sed -i -e "s/^/    \"/g" -e "s/$/\",/g" res3
head -c -2 res3 > res


#make volume 3 sb file
cat utils/header-volume-3 > volume-3.sb
cat res >> volume-3.sb
echo "]" >> volume-3.sb
echo "}" >> volume-3.sb

#remove tmp files
rm -f res res1 res2 res3 list1 list2 tmp1 tmp2
