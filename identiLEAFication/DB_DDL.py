import pymysql
from PIL import Image
import numpy
import os
import sys

conn = pymysql.connect(host='127.0.0.1',user="Yy", passwd="20011231YYydmYHQ", db="plantvillage")
cursor=conn.cursor()

folderNamelist     =   ['Apple___Apple_scab', 
                        'Apple___Black_rot', 
                        'Apple___Cedar_apple_rust', 
                        'Apple___healthy', 
                        'Blueberry___healthy', 
                        'Cherry_(including_sour)___healthy', 
                        'Cherry_(including_sour)___Powdery_mildew', 
                        'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot', 
                        'Corn_(maize)___Common_rust_', 'Corn_(maize)___healthy', 
                        'Corn_(maize)___Northern_Leaf_Blight', 
                        'Grape___Black_rot', 
                        'Grape___Esca_(Black_Measles)', 
                        'Grape___healthy', 
                        'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)', 
                        'Orange___Haunglongbing_(Citrus_greening)', 
                        'Peach___Bacterial_spot', 
                        'Peach___healthy', 
                        'Pepper__bell___Bacterial_spot', 
                        'Pepper__bell___healthy', 
                        'Potato___Early_blight', 
                        'Potato___healthy', 
                        'Potato___Late_blight', 
                        'Raspberry___healthy', 
                        'Soybean___healthy', 
                        'Squash___Powdery_mildew', 
                        'Strawberry___healthy', 
                        'Strawberry___Leaf_scorch', 
                        'Tomato___Bacterial_spot', 
                        'Tomato___Early_blight', 
                        'Tomato___healthy', 
                        'Tomato___Late_blight', 
                        'Tomato___Leaf_Mold', 
                        'Tomato___Septoria_leaf_spot', 
                        'Tomato___Spider_mites Two-spotted_spider_mite', 
                        'Tomato___Target_Spot', 
                        'Tomato___Tomato_mosaic_virus', 
                        'Tomato___Tomato_Yellow_Leaf_Curl_Virus']

namelist =             ['Apple___Apple_scab', 
                        'Apple___Black_rot', 
                        'Apple___Cedar_apple_rust', 
                        'Apple___healthy', 
                        'Blueberry___healthy', 
                        'Cherry___healthy', 
                        'Cherry___Powdery_mildew', 
                        'Corn___Cercospora_leaf_spot_Gray_leaf_spot', 
                        'Corn___Common_rust_', 
                        'Corn___healthy', 
                        'Corn___Northern_Leaf_Blight', 
                        'Grape___Black_rot', 
                        'Grape___Esca', 
                        'Grape___healthy', 
                        'Grape___Leaf_blight', 
                        'Orange___Haunglongbing', 
                        'Peach___Bacterial_spot', 
                        'Peach___healthy', 
                        'Pepper__bell___Bacterial_spot', 
                        'Pepper__bell___healthy', 
                        'Potato___Early_blight', 
                        'Potato___healthy', 
                        'Potato___Late_blight', 
                        'Raspberry___healthy', 
                        'Soybean___healthy', 
                        'Squash___Powdery_mildew', 
                        'Strawberry___healthy', 
                        'Strawberry___Leaf_scorch', 
                        'Tomato___Bacterial_spot', 
                        'Tomato___Early_blight', 
                        'Tomato___healthy', 
                        'Tomato___Late_blight', 
                        'Tomato___Leaf_Mold', 
                        'Tomato___Septoria_leaf_spot', 
                        'Tomato___Spider_mites_Two_spotted_spider_mite', 
                        'Tomato___Target_Spot', 
                        'Tomato___Tomato_mosaic_virus', 
                        'Tomato___Tomato_Yellow_Leaf_Curl_Virus']

def insert_image(cursor, connection, ID, category, image, table):
    sql = "insert into " + table + " values(%s,%s,%s)"
    cursor.execute(sql,(ID,category,numpy.array(image)))
    connection.commit()

def normalizeMessage(imgPath):
    img = Image.open(imgPath).resize((256,256))
    pic = numpy.array(img).reshape(256*256*3)
    stringpic = ''
    for i in range(len(pic)):
        stringpic+=(str(pic[i])+',')
    stringpic = stringpic[:len(stringpic)-1]
    return stringpic

def progress_bar(curr, total):
    progress = curr/total
    print("\r", end="")
    print("Process progress: {:0.2f}% ".format(progress*100), end="")
    sys.stdout.flush()
    
def addForeignKey(conn, cursor, table1, key1, table2, key2):
    # table1 references table2
    query=('alter table '+
           table1 + 
           ' add foreign key(' +
           key1 + 
           ') REFERENCES ' + 
           table2 + 
           '('+
           key2 +
           ')')
    cursor.execute(query)
    conn.commit()
    
#==============================================================================

for i in range(38):
    # create table
    category = folderNamelist[i]
    name = namelist[i]
    query = 'create table ' + name + '''(
    ID varchar(15),
    category varchar(80),
    image MediumBlob);'''
    cursor.execute(query)
    conn.commit()
    
    # insert tuples
    for file in os.listdir('../PlantVillage/'+category):
        img = normalizeMessage('../PlantVillage/'+category+'/'+file)
        ID = file[:len(file)-4]
        insert_image(cursor, conn, ID, category, img, name)
    print(category + ' done.==========================================')

#==============================================================================    

# 纲：单子叶植物纲，双子叶植物纲================= 
CLASS = ['Monocotyledons','Dicotyledoneae']

# 纲 & 科=======================================
Monocotyledons = ['Gramineae'] #禾本科
#豆科 杜鹃花科 葫芦科 葡萄科 蔷薇科 茄科 芸香科
Dicotyledoneae = ['Fabaceae','Ericaceae','Cucurbitaceae',  #豆科 杜鹃花科 葫芦科
                  'Vitaceae','Rosaceae','Solanaceae','Rutaceae'] #葡萄科 蔷薇科 茄科 芸香科
FAMILY = [Monocotyledons,Dicotyledoneae]
claString  = ['Monocotyledons','Dicotyledoneae']

# 科 & 种=======================================
Gramineae = ['Corn'] #禾本科
Fabaceae = ['Soybean'] #豆科
Ericaceae = ['Blueberry'] #杜鹃花科
Cucurbitaceae = ['Squash'] #葫芦科
Vitaceae = ['Grape'] #葡萄科
Rosaceae = ['Strawberry','Peach','Apple','Raspberry','Cherry'] #蔷薇科
Solanaceae = ['Tomato','Pepper','Potato'] #茄科
Rutaceae = ['Orange'] #芸香科
SPECIES = [Gramineae,Fabaceae,Ericaceae,Cucurbitaceae,Vitaceae,Rosaceae,Solanaceae,Rutaceae]
famString=['Gramineae','Fabaceae','Ericaceae','Cucurbitaceae',
           'Vitaceae','Rosaceae','Solanaceae','Rutaceae']

# 种 & 病害
Corn = ['Corn___Cercospora_leaf_spot_Gray_leaf_spot',
        'Corn___healthy',
        'Corn___Northern_Leaf_Blight',
        'Corn___Common_rust_',]
Soybean = ['Soybean___healthy']
Blueberry = ['Blueberry___healthy']
Squash = ['Squash___Powdery_mildew']
Grape = ['Grape___Black_rot',
         'Grape___Esca', 
         'Grape___healthy', 
         'Grape___Leaf_blight']
Strawberry = ['Strawberry___healthy', 
              'Strawberry___Leaf_scorch']
Peach = ['Peach___Bacterial_spot', 
         'Peach___healthy']  
Apple = ['Apple___Apple_scab', 
         'Apple___Black_rot', 
         'Apple___Cedar_apple_rust', 
         'Apple___healthy']
Raspberry = ['Raspberry___healthy']
Cherry = ['Cherry___healthy', 
          'Cherry___Powdery_mildew']
Tomato = ['Tomato___Bacterial_spot', 
          'Tomato___Early_blight', 
          'Tomato___healthy', 
          'Tomato___Late_blight', 
          'Tomato___Leaf_Mold', 
          'Tomato___Septoria_leaf_spot', 
          'Tomato___Spider_mites_Two-spotted_spider_mite', 
          'Tomato___Target_Spot', 
          'Tomato___Tomato_mosaic_virus', 
          'Tomato___Tomato_Yellow_Leaf_Curl_Virus']
Pepper = ['Pepper__bell___Bacterial_spot', 
          'Pepper__bell___healthy']
Potato = ['Potato___Early_blight', 
          'Potato___healthy', 
          'Potato___Late_blight']
Orange = ['Orange___Haunglongbing']
ILLNESS = [Corn,Soybean,Blueberry,Squash,Grape,
           Strawberry,Peach,Apple,Raspberry,Cherry,Tomato,Pepper,
           Potato,Orange]
speString=['Corn','Soybean','Blueberry','Squash','Grape',
           'Strawberry','Peach','Apple','Raspberry','Cherry',
           'Tomato','Pepper','Potato','Orange']

for item in CLASS:
    query = 'create table ' + item + '''
    (family varchar(20), 
     class varchar(20),
     PRIMARY KEY(family));'''
    cursor.execute(query)
    conn.commit()
    
for item in FAMILY:
    for table in item:
        query = 'create table ' + table + '''
        (species varchar(20),
         family varchar(20),
         PRIMARY KEY(species)
         );'''
        cursor.execute(query)
        conn.commit()

for item in SPECIES:
    for table in item:
        query = 'create table ' + table + '''
        (illness varchar(80),
         species varchar(20),
         detail blob,
         solution blob,
         PRIMARY KEY(illness)
         );'''
        cursor.execute(query)
        conn.commit()

# 单子叶植物纲
query = 'insert into Monocotyledons values(%s,%s)'
cursor.execute(query,('Gramineae','Monocotyledons'))
conn.commit()
# 双子叶植物纲
query = 'insert into Dicotyledoneae values(%s,%s)'
cursor.executemany(query,[(Dicotyledoneae[0],'Dicotyledoneae'),
                          (Dicotyledoneae[1],'Dicotyledoneae'),
                          (Dicotyledoneae[2],'Dicotyledoneae'),
                          (Dicotyledoneae[3],'Dicotyledoneae'),
                          (Dicotyledoneae[4],'Dicotyledoneae'),
                          (Dicotyledoneae[5],'Dicotyledoneae'),
                          (Dicotyledoneae[6],'Dicotyledoneae')])
conn.commit()
# 禾本科
query = 'insert into Gramineae values(%s,%s)'
cursor.execute(query,(Gramineae[0],'Gramineae'))
conn.commit()
# 豆科
query = 'insert into Fabaceae values(%s,%s)'
cursor.execute(query,(Fabaceae[0],'Fabaceae'))
conn.commit()
# 杜鹃花科
query = 'insert into Ericaceae values(%s,%s)'
cursor.execute(query,(Ericaceae[0],'Ericaceae'))
conn.commit()
# 葫芦科
query = 'insert into Cucurbitaceae values(%s,%s)'
cursor.execute(query,(Cucurbitaceae[0],'Cucurbitaceae'))
conn.commit()
# 葡萄科
query = 'insert into Vitaceae values(%s,%s)'
cursor.execute(query,(Vitaceae[0],'Vitaceae'))
conn.commit()
# 蔷薇科
query = 'insert into Rosaceae values(%s,%s)'
cursor.executemany(query,[(Rosaceae[0],'Rosaceae'),
                          (Rosaceae[1],'Rosaceae'),
                          (Rosaceae[2],'Rosaceae'),
                          (Rosaceae[3],'Rosaceae'),
                          (Rosaceae[4],'Rosaceae')])
conn.commit()
# 茄科 Solanaceae
query = 'insert into Solanaceae values(%s,%s)'
cursor.executemany(query,[(Solanaceae[0],'Rosaceae'),
                          (Solanaceae[1],'Rosaceae'),
                          (Solanaceae[2],'Rosaceae')])
conn.commit()
# 芸香科
query = 'insert into Rutaceae values(%s,%s)'
cursor.execute(query,(Rutaceae[0],'Rutaceae'))
conn.commit()

# insert=======================================================================

# read detail and solution from file
fptr = open('./files/solution.txt','rt',encoding='utf-8')
info = fptr.read().splitlines() # each illness matches 2 lines, together 76 lines
detail = info[0:len(info):2]
solution = info[1:len(info):2]
fptr.close()

count = 0
for species in ILLNESS:
    index = ILLNESS.index(species)
    for situation in species:
        table = speString[index]
        query = 'insert into ' + table + ' values(%s, %s, %s, %s)'
        cursor.execute(query,(situation,table,detail[count],solution[count]))
        print(detail[count][:10])
        print('\n')
        conn.commit()
        count += 1
print('solution done')

# fk===========================================================================

# foreign keys 
# alter table tablename add constraint FK_ID foreign key(fk) REFERENCES ftable(fk)
addForeignKey(conn,cursor,famString[0],'family','Monocotyledons','family')
addForeignKey(conn,cursor,famString[1],'family','Dicotyledoneae','family')
addForeignKey(conn,cursor,famString[2],'family','Dicotyledoneae','family')
addForeignKey(conn,cursor,famString[3],'family','Dicotyledoneae','family')
addForeignKey(conn,cursor,famString[4],'family','Dicotyledoneae','family')
addForeignKey(conn,cursor,famString[5],'family','Dicotyledoneae','family')
addForeignKey(conn,cursor,famString[6],'family','Dicotyledoneae','family')
addForeignKey(conn,cursor,famString[7],'family','Dicotyledoneae','family')

addForeignKey(conn,cursor,speString[ 0],'species',famString[0],'species')
addForeignKey(conn,cursor,speString[ 1],'species',famString[1],'species')
addForeignKey(conn,cursor,speString[ 2],'species',famString[2],'species')
addForeignKey(conn,cursor,speString[ 3],'species',famString[3],'species')
addForeignKey(conn,cursor,speString[ 4],'species',famString[4],'species')
addForeignKey(conn,cursor,speString[ 5],'species',famString[5],'species')
addForeignKey(conn,cursor,speString[ 6],'species',famString[5],'species')
addForeignKey(conn,cursor,speString[ 7],'species',famString[5],'species')
addForeignKey(conn,cursor,speString[ 8],'species',famString[5],'species')
addForeignKey(conn,cursor,speString[ 9],'species',famString[5],'species')
addForeignKey(conn,cursor,speString[10],'species',famString[6],'species')
addForeignKey(conn,cursor,speString[11],'species',famString[6],'species')
addForeignKey(conn,cursor,speString[12],'species',famString[6],'species')
addForeignKey(conn,cursor,speString[13],'species',famString[7],'species')
print('fk done')

    
    
    
    
    
    
    
    
    
    
    
    