#!/bin/bash

LITTERBOX="java -jar /../../IdeaProjects/litterbox/target/Litterbox-1.7-SNAPSHOT.jar"

TMP_STATS=/tmp/_lb_tmp_stat.csv
TMP_BUGS=/tmp/_lb_tmp_bug.csv
TMP_PROJECT=/tmp/_lb_tmp_proj.csv

OUTPUT=$(PWD)/data.csv

for STUNDE in 1 2 3 4 5 6; do
    echo "Current week: $STUNDE"
    pushd .
    cd session$STUNDE

    for SCHUELER in $(ls); do
	pushd .
	cd $SCHUELER
	for PROJECT in *.sb3; do
	    rm -f $TMP_STATS $TMP_BUGS $TMP_PROJECT
	    echo week,additional,participant,project > $TMP_PROJECT
	    echo $STUNDE,0,$SCHUELER,$(echo $PROJECT | sed -e s/\.sb3//) >> $TMP_PROJECT
	    $LITTERBOX --check -p $PROJECT -o $TMP_BUGS
	    $LITTERBOX --stats -p $PROJECT -o $TMP_STATS

	    if [ -e $OUTPUT ]; then
		join -t, -1 4 -2 1 $TMP_PROJECT $TMP_STATS | join -t, -1 1 -2 1 - $TMP_BUGS | sed -e "s/\r//g" | grep -v avg_block_statement_count >> $OUTPUT
	    else
		join -t, -1 4 -2 1 $TMP_PROJECT $TMP_STATS | join -t, -1 1 -2 1 - $TMP_BUGS | sed -e "s/\r//g" >> $OUTPUT
	    fi
	done
	popd 
    done
    
    cd ..
    cd session${STUNDE}add

    for SCHUELER in $(ls); do
	pushd .
	cd $SCHUELER
	for PROJECT in *.sb3; do
	    rm -f $TMP_STATS $TMP_BUGS $TMP_PROJECT
	    echo week,additional,participant,project > $TMP_PROJECT
	    echo $STUNDE,1,$SCHUELER,$(echo $PROJECT | sed -e s/\.sb3//) >> $TMP_PROJECT
	    $LITTERBOX --check -p $PROJECT -o $TMP_BUGS
	    $LITTERBOX --stats -p $PROJECT -o $TMP_STATS

	    if [ -e $OUTPUT ]; then
		join -t, -1 4 -2 1 $TMP_PROJECT $TMP_STATS | join -t, -1 1 -2 1 - $TMP_BUGS | sed -e "s/\r//g" | grep -v avg_block_statement_count >> $OUTPUT
	    else
		join -t, -1 4 -2 1 $TMP_PROJECT $TMP_STATS | join -t, -1 1 -2 1 - $TMP_BUGS | sed -e "s/\r//g" >> $OUTPUT
	    fi
	done
	popd 
    done
    
    popd
done

