for ligne in open("corpus-kab.txt",encoding='utf-8'):
     text=ligne.replace("\ufeff","")
     a=text.split(" ")
     for i in a:
        j=i.split("/")
        try:
         if j[1] in [ "VPPP","VPAIP","VPAIN","VPA","VPPN"]:
            print (ligne)
        except:
            print("error",ligne)
            exit()