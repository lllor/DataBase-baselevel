from bsddb3 import db
import re
import sys

database1 = None
database2 = None
database3 = None
curs1 = None
curs2 = None
curs3 = None

def createDB():
    global database1, database2, database3
    global curs1,curs2,curs3
    
    database1= db.DB()
    database1.set_flags(db.DB_DUP)
    database1.open("re.idx",None,db.DB_HASH,db.DB_CREATE)
    curs1 = database1.cursor()
    
    database2= db.DB()
    database2.set_flags(db.DB_DUP)
    database2.open("te.idx",None,db.DB_BTREE,db.DB_CREATE)
    curs2 = database2.cursor()
    
    database3= db.DB()
    database3.set_flags(db.DB_DUP)
    database3.open("ye.idx",None,db.DB_BTREE,db.DB_CREATE)    
    curs3 = database3.cursor()

def closeDB():
    global database1, database2, database3
    global curs1,curs2,curs3
    
    curs1.close()
    database1.close()
    curs2.close()
    database2.close()
    curs3.close()
    database3.close()    

def years(name):
    global curs3    
    output = []
    option = name[0]
    name = name[1:]
    
    maxyear = curs3.last()[0].decode("utf-8")
    
    if option == ":":
        name = name.encode("utf-8")
        try:
            result = curs3.set(name)
            output.append(result[1].decode("utf-8"))
        except:
            return output
        while True:
            try:
                ne = curs3.next()
                if ne[0] != name:
                    return output
                output.append(ne[1].decode("utf-8"))
            except:
                return output
            
    if option == ">":
        name = str(int(name)+1)
        name = name.encode("utf-8")
        while True:
            try:
                result = curs3.set(name)
                output.append(result[1].decode("utf-8"))
                break
            except:
                if int(name.decode("utf-8")) > int(maxyear):
                    return output
                name = str(int(name.decode("utf-8"))+1).encode("utf-8")
        while True:
            try:
                ne = curs3.next()
                output.append(ne[1].decode("utf-8"))
            except:
                return output
            
    if option == "<":
        name = name.encode("utf-8")
        result = curs3.first()
        if result[0].decode("utf-8") > name.decode("utf-8"):
            return output
        output.append(result[1].decode("utf-8"))
        while True:
            try:
                ne = curs3.next()
                if ne[0] >= name:
                    return output                
                output.append(ne[1].decode("utf-8"))
            except:
                return output        
            
def terms(name):
    global curs2
    output = []
    name = name.encode("utf-8")
    try:
        result = curs2.set(name)
        output.append(result[1].decode("utf-8"))
    except:
        return output
    while True:
        try:
            ne = curs2.next()
            if ne[0] != name:
                return output
            output.append(ne[1].decode("utf-8"))
        except:
            return output

def recs(key,text,name):
    global curs1
    key1 = key.encode("utf-8")
 
    result = curs1.set(key1)[1].decode("utf-8")    
    pattern = re.compile('<'+name+'>.*</'+name+'>')
    cont = pattern.findall(result)
    if len(cont) == 0:
        return None
    cont = cont[0].lower().split('<'+name+'>')
    ln = len(name)+3
    newterm = []
    for i in cont:
        if len(i)>=ln:
            newterm.append(i[:-ln])    
    #newcont = []
    #for ea in newterm:
        #new = ''
        #for i in ea:
            #if re.match('\w',i):
                #new += i
            #else:
                #new += ' '
        #newcont.append(new)
    for eachnew in newterm:
        if text in eachnew:
            return key
    return None
    
    
def phrase(option,text,name):
    if not re.match("\A\w.*\w\Z",text):
        return None
    text_new = text.split()
    for i in text_new:
        for j in i:
            if re.match('\W',j):
                return None
    output = []
    ret = []
    for each in text_new:
        out = terms(option+each)
        for i in out:
            if i not in output:
                output.append(i)
    for each in output:
        result = recs(each,text,name)
        if result:
            ret.append(result)
    return ret

def search(query,full,outfile = None):
    global curs1
    count = 0
    new = ''
    for i in query:
        if i == '"':
            count += 1
        if i == ' ' and count %2 == 0:
            new += '裂'
        else:
            new += i
            
    querys = new.split('裂')
    result = {}
    final = []
    
    count = len(querys)
    for each in querys:
        output = None
        if each == "output=full":
            full = True
            count -= 1
            continue
        elif each == "output=key":
            full = False
            count -= 1
            continue
 
        elif re.match('\Ayear[:<>]\d+\Z',each):
            output = years(each[4:])
            
        elif re.match('\Atitle:\w+\Z',each):
            output = terms('t-'+each[6:])
       
        elif re.match('\Aauthor:\w+\Z',each):
            output = terms('a-'+each[7:])
            
        elif re.match('\Aother:\w+\Z',each):
            output = terms('o-'+each[6:])
        elif re.match('\A\w+\Z',each) :
            output = terms('t-'+each)
            out2 = terms('a-'+each)
            out3 = terms('o-'+each)
            for ea in out2:
                if ea not in output:
                    output.append(ea)
            for ea in out3:
                if ea not in output:
                    output.append(ea)
                    
        elif re.match('\Atitle:".*"\Z',each):
            output = phrase('t-',each[7:-1],'title')
        elif re.match('\Aauthor:".*"\Z',each):
            output = phrase('a-',each[8:-1],'author')
        elif re.match('\Aother:".*"\Z',each):
            output = phrase('o-',each[7:-1],'journal')
            out2 = phrase('o-',each[7:-1],'booktitle')
            out3 = phrase('o-',each[7:-1],'publisher')
            for eachout in out2:
                if eachout not in output:
                    output.append(eachout) 
            for eachout in out3:
                if eachout not in output:
                    output.append(eachout)            
                    
        elif re.match('\A".*"\Z',each):
            output = phrase('t-',each[1:-1],'title')
            out2 = phrase('a-',each[1:-1],'author')
            out3 = phrase('o-',each[1:-1],'journal')
            out4 = phrase('o-',each[1:-1],'booktitle')
            out5 = phrase('o-',each[1:-1],'publisher')            
            
            for eachout in out2:
                if eachout not in output:
                    output.append(eachout)
            for eachout in out3:
                if eachout not in output:
                    output.append(eachout)
            for eachout in out4:
                if eachout not in output:
                    output.append(eachout)    
            for eachout in out5:
                if eachout not in output:
                    output.append(eachout)            
          
        if output == None:
            if len(sys.argv) == 3:
                outfile.write("Your grammar is not correct\n")
            else:
                print("Your grammar is not correct")
            return
        
        for i in output:
            if i in result:
                result[i] += 1
            else:
                result[i] = 1

    for each in result:
        if result[each] == count:
            if full:
                each = curs1.set(each.encode("utf-8"))[1].decode("utf-8")
            final.append(each)
                
    if len(final) == 0 and count != 0:
        if len(sys.argv) == 3:
            outfile.write("There is no result by this query\n")
        else:
            print("There is no result by this query")
    final.sort()
    for eachfinal in final:
        if len(sys.argv)==3:
            outfile.write(eachfinal+'\n')
        else:
            print(eachfinal)    
            
    return full

def main():
    createDB()
    full = False
    if len(sys.argv)==3:
        outfile = open(sys.argv[2],'w')    
    try:
        file = open(sys.argv[1],'r')
        for eachline in file:
            if len(sys.argv) == 3:
                outfile.write('output of   '+eachline[:-1].lower()+'   is:\n')
                full = search(eachline[:-1].lower(),full,outfile)
            else:
                print('\noutput of   '+eachline[:-1].lower()+'   is:')
                full = search(eachline[:-1].lower(),full)
        file.close()
    except:
        while True:
            query = input("input: ").lower()
            if query == '':
                break
            full = search(query,full)
    if len(sys.argv)==3:
        outfile.close()    
    closeDB()
if __name__ == "__main__":
    main()
