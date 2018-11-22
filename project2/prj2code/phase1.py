import re
import sys

def writeterm(key,text,file,name,option):
    term = re.compile('<'+name+'>.*</'+name+'>')
    term = term.findall(text)
    if len(term) == 0:
        return
    term = term[0].split('<'+name+'>')
    ln = len(name)+3
    newterm = []
    for i in term:
        if len(i)>=ln:
            newterm.append(i[:-ln])
    term = []
    for each in newterm: 
        new = ''
        for i in each:
            if re.match('\w',i):
                new += i
            else:
                new +=' '
        term.append(new.lower())
    for each in term:
        each = each.split()
        for i in each:
            if len(i)>2:
                file.write(option+i+':'+key+'\n')

def terms(key,text,file):
    
    writeterm(key,text,file,'title','t-')
    writeterm(key,text,file,'journal','o-')
    writeterm(key,text,file,'booktitle','o-')
    writeterm(key,text,file,'publisher','o-')
    writeterm(key,text,file,'author','a-')
    
def years(key,text,file):
    
    year = re.compile('<year>.*</year>')
    year = year.findall(text)
    if len(year) == 0:
        return
    file.write(year[0][6:-7]+':'+key+'\n')
    
def recs(key,text,file):
    if "\\" in text:
        new = ''
        for i in text:
            if i == '\\':
                i = '&92;'
            new += i
        text = new
    file.write(key+':'+text)
    
def goin(term,text,termsfile,yearsfile,recsfile):
    
    key = re.compile(term+'.*"')
    key = key.findall(text)[0].split('"')[1]
    terms(key,text,termsfile)
    years(key,text,yearsfile)
    recs(key,text,recsfile)
    
def main():
    inputfile = sys.argv[1]
    text = []
    file = open(inputfile,'r')
    termsfile = open('terms.txt','w')
    yearsfile = open('years.txt','w')
    recsfile = open('recs.txt','w')
    
    for eachline in file:
        if re.match('\A<article key.*',eachline):
            goin('\A<article key="',eachline,termsfile,yearsfile,recsfile)
        elif re.match('\A<inproceedings key.*',eachline):
            goin('\A<inproceedings key="',eachline,termsfile,yearsfile,recsfile)
            
    file.close()
    termsfile.close()
    yearsfile.close()
    recsfile.close()
    
if __name__ == "__main__":
    main()