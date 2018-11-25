#!/bin/bash
clear
echo "sort stared"
#sort -u -o test.text test.text
sort -u -o terms.txt terms.txt

sort -u -o prices.txt prices.txt
sort -n -o prices.txt prices.txt
sort -u -o pdates.txt pdates.txt
sort -u -o ads.txt ads.txt
echo "===========sort ended=============="

echo "break stared"
perl break.pl< pdates.txt > pd_temp.txt
perl break.pl< ads.txt > a_temp.txt
perl break.pl< prices.txt > p_temp.txt
perl break.pl< terms.txt > t_temp.txt
echo "===========break ended=============="

#echo "organize files"
#mv pd_temp.txt pdates.txt
#mv a_temp.txt ads.txt
#mv p_temp.txt prices.txt
#mv t_temp.txt terms.txt
#echo "===========organization ended======="

echo "create index"
db_load -c duplicates=1 -T -t hash -f a_temp.txt ad.idx
db_load -c duplicates=1 -T -t btree -f p_temp.txt pr.idx
db_load -c duplicates=1 -T -t btree -f pd_temp.txt da.idx
db_load -c duplicates=1 -T -t btree -f t_temp.txt te.idx
echo "===========building ended==========="
