import os
from bsddb3 import db

def main():
    os.system("sort -u -o recs.txt recs.txt")
    os.system("sort -u -o terms.txt terms.txt")
    os.system("sort -u -o years.txt years.txt")
    
    os.system("perl break.pl < recs.txt > recs_temp.txt")
    os.system("perl break.pl < terms.txt > terms_temp.txt")
    os.system("perl break.pl < years.txt > years_temp.txt")
    
    os.system("mv recs_temp.txt recs.txt")
    os.system("mv terms_temp.txt terms.txt")
    os.system("mv years_temp.txt years.txt")
    
    os.system("db_load -c duplicates=1 -T -t hash -f recs.txt re.idx")
    os.system("db_load -c duplicates=1 -T -t btree -f terms.txt te.idx")
    os.system("db_load -c duplicates=1 -T -t btree -f years.txt ye.idx")
    
if __name__ == "__main__":
    main()