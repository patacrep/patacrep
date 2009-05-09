#!/bin/sh
for directory in songs/*; do
    images=`ls $directory/*.{jpg,png} 2> /dev/null`
    val=`echo $images | wc -w`
    for song in $directory/*.sg; do
	sg=`basename $song`
	sed -i '0,/\\gtab/s//\\cover\n\\gtab/' $song
	if [ $val -gt 1 ] 
	then
	    i=1
	    for image in $images; do
		img=`basename $image .jpg`
		img=`echo $img | sed 's/.png$//'`
		echo "Apply $img to $song ? ($i/$val)"
		i=$(($i+1))
		read answer
		case "$answer" in
		    "y")
			sed -i 's/beginsong{\([^}]*\)}\[\([^]]*\)\]/beginsong{\1}[\2,cov='$img']/' $song
			break;
			;;
		    "n")
			true
			;;
		esac
	    done; 
	elif [ $val -eq 1 ] 
	then
	    img=`basename $images .jpg`
	    img=`echo $img | sed 's/.png$//'`
	    echo "Applying $img to $sg"
	    sed -i 's/beginsong{\([^}]*\)}\[\([^]]*\)\]/beginsong{\1}[\2,cov='$img']/' $song
	fi;
    done; 
done; 
