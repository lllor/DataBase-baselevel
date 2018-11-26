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
            
            #all patterns must be replaced
            p1 = r"&#[0-9]*;"
            #p4 = r"[\$%@\?~\^]"
            p5 = r"[\$%@\?~\^&,.;#<>=!\(\):\+*\|\{\}\\`]"
            p6 = r"[[]"
            p7 = r"[]]"
            p9 = r"[']"
            p10 = r'["]'
            pa = r"&apos;"
            pb = r"&quot;"
            pc = r"&amp;"
            pd = r"quot;"            
            patterns = r'|'.join((pa,pb,pc,pd,p5,p6,p7,p9,p10))
            
            #terms.txt from title
            temp_list = []
            for t in t_list:
                t = str(t).lower()
                t = re.sub(p1,"", t)
                t = re.sub(patterns,' ',t)
                #print(t)
                ts = t.split()
                for k in ts:
                    if len(k.strip()) >2 and re.match(r'[0-9a-zA-Z_-]*',k):
                        new1.write(k+":"+aid.group(1)+"\n")
                        
            #terms.txt from description
            for d in d_list:
                d = str(d).lower()
                d = re.sub(p1,"", d)
                d = re.sub(patterns,' ',d)
                
                ds = d.split()
                for k in ds:
                    if len(k.strip()) >2 and re.match(r'[0-9a-zA-Z_-]*',k):
                        new1.write(k+":"+aid.group(1)+"\n")
                    
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
