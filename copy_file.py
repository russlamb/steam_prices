from os.path import expanduser

def copy_file():
    with open(expanduser("~/data/prices.csv"),"r") as f:
        with open(expanduser("~/data/prices_new.csv"),"w") as f1:
            ## Read the first line
            line = f.readline()
            i=0
            ## If the file is not empty keep reading line one at a time
            ## till the file is empty
            while line:
                if i==0:
                    f1.write("price_date,price_value,card_name,app_name,app_id\n")
                else:
                    f1.write(line)
                i+=1
                line = f.readline()

def read_file():
    with open(expanduser("~/data/prices_new.csv"),"r") as f1:
        print(f1.readline())
        print(f1.readline())

read_file()