import re
import sys

def main():
    filename = sys.argv[1]
    file = open(filename,"r")
    new1 = open("terms.txt","w")
    new2 = open("pdates.txt","w")
    new3 = open("prices.txt","w")
    new4 = open("ads.txt","w")

    #for each kijiji advertisement
    for line in file:
        try:
            aid = re.search(r'<aid>(.*?)</aid>',line)
        except AttributeError:
            aid = None
            
        #if aid exists    
        if aid:
            
            #terms.txt
            try:
                title = re.search(r'<ti>(.*?)</ti>',line)
            except AttributeError:
                title = None
                
            try:
                desc = re.search(r'<desc>(.*?)</desc>',line)
            except:
                desc = None
            
            
            t_list = (title.group(1)).replace('/', ' ').replace('.',' ').split(' ')
            d_list = (desc.group(1)).replace('/', ' ').replace('.',' ').split(' ')
            p1 = r"&#[0-9]*;"
            p2 = r"[,]"
            p3 = r"[;]"
            p4 = r"[$]"
            p5 = r"[#]"
            p6 = r"[[]"
            p7 = r"[]]"
            patterns = r'|'.join((p1,p2,p3,p4,p5,p6,p7))
            
            for t in t_list:
                t = str(t)
                t = re.sub(patterns,'',t)
                if len(t)>2 and re.match(r'[0-9a-zA-Z_-]*',t) and re.match('^[^.]*$',t):
                    new1.write(t.lower()+":"+aid.group(1)+"\n")
                              
            for d in d_list:
                d = str(d)
                d = re.sub(patterns,"",d)
                if len(d)>2 and re.match(r'[0-9a-zA-Z_-]*',d) and re.match('^[^.]*$',d):
                    new1.write(d.lower()+":"+aid.group(1)+"\n")
                    
                    
            #pdates.txt
            try:
                date = re.search(r'<date>(.*?)</date>',line)
            except AttributeError:
                date = None
            try:
                cat = re.search(r'<cat>(.*?)</cat>',line)
            except AttributeError:
                cat = None
            try:
                loc = re.search(r'<loc>(.*?)</loc>',line)
            except AttributeError:
                loc = None
            
            new2.write(date.group(1)+":"+aid.group(1)+","+cat.group(1)+","+loc.group(1)+"\n")
            
            
            
            #prices.txt
            try:
                pr = re.search(r'<price>(.*?)</price>',line)
            except AttributeError:
                pr = None
            s = " "*(12-len(pr.group(1)))
            new3.write(s+pr.group(1)+":"+aid.group(1)+","+cat.group(1)+","+loc.group(1)+"\n")
            
            
            
            #ads.txt
            new4.write(aid.group(1)+":"+line+"\n")
            
            
    new1.close()
    new2.close()
    new3.close()
    new4.close()
    file.close()
            
        
        


if __name__ == "__main__":
    main()
    
    
    
