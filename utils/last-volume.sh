#!/bin/sh
#Author: Romain Goffe
#Date: 07/05/2011
#Description: Generate an sb file containing all the songs that are not 
# already in previous volumes

GREP="$GREP_OPTIONS"
export GREP_OPTIONS=""

BOOKS_DIR="books"

#all songs
cd songs
ls -1 */*.sg > ../res1
cd ..

#get volume 1 list
tail -n +13 "$BOOKS_DIR/volume-1.sb" > tmp1
head -n -2 tmp1 > list1
sed -i -e "s/\",//g" -e "s/    \"//g" -e "s/\"//g" list1

#remove volume 1 songs
grep -vf list1 res1 > res2 

#get volume 2 list
tail -n +14 "$BOOKS_DIR/volume-2.sb" > tmp2
head -n -2 tmp2 > list2
sed -i -e "s/\",//g" -e "s/    \"//g" -e "s/\"//g" list2

#remove volume 2 songs
grep -vf list2 res2 > res3 

#get volume 3 list
tail -n +14 "$BOOKS_DIR/volume-3.sb" > tmp3
head -n -2 tmp3 > list3
sed -i -e "s/\",//g" -e "s/    \"//g" -e "s/\"//g" list3

#remove volume 3 songs
grep -vf list3 res3 > res4 

#format song list
sed -i -e "s/^/    \"/g" -e "s/$/\",/g" res4
head -c -2 res4 > res


#make volume 4 sb file
cat utils/header-last-volume > "$BOOKS_DIR/volume-4.sb"
cat res >> "$BOOKS_DIR/volume-4.sb"
echo "]" >> "$BOOKS_DIR/volume-4.sb"
echo "}" >> "$BOOKS_DIR/volume-4.sb"

#remove tmp files
rm -f res res1 res2 res3 res4 list1 list2 list3 tmp1 tmp2 tmp3

export GREP_OPTIONS="$GREP"
