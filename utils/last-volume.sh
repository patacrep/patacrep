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

for i in 1 2 3 4
do
    #get volume i list
    tail -n +14 "$BOOKS_DIR/volume-$i.sb" > tmp$i
    head -n -2 tmp$i > list$i
    sed -i -e "s/\",//g" -e "s/    \"//g" -e "s/\"//g" list$i

    #remove volume i songs
    grep -vf list$i res$i > res$(($i+1))
done

#format song list
sed -i -e "s/^/    \"/g" -e "s/$/\",/g" res$(($i+1))
head -c -2 res$(($i+1)) > res


#make volume i+1 sb file
cat utils/header-last-volume > "$BOOKS_DIR/volume-$(($i+1)).sb"
cat res >> "$BOOKS_DIR/volume-$(($i+1)).sb"
echo "]" >> "$BOOKS_DIR/volume-$(($i+1)).sb"
echo "}" >> "$BOOKS_DIR/volume-$(($i+1)).sb"

#remove tmp files
for i in 1 2 3 4
do
  rm -f res$i list$i tmp$i
done
rm -f res res$(($i+1))

export GREP_OPTIONS="$GREP"
