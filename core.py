import pandas as pd
from datetime import datetime

def printTime():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return str(current_time)


def clearTXT(text):
    with open('docs/output/'+text,'w') as file:
        pass

def escreveTXT(texto):
    with open('docs/output/test.txt','a+') as f:
        f.write(texto+'\n')
        
def searchTXT(text):
    with open('docs/output/test.txt') as f:
        if text in f.read():
            return True
        else:
            return False

def sortedTXT(file_input,file_output):
    with open('docs/output/'+file_input, 'r') as r:
        for line in sorted(r):
            with open('docs/output/'+file_output,'a+') as f:
                f.write(line)

print('### SYNC_SUAP_CENSUP ###')
print( printTime()+' | Iniciando processamento.')

df = pd.read_excel('docs/input/docente_vinculos.xls')
df['Professores'].to_csv('docs/output/test.csv',index=False,header=False)

df = df.reset_index()
for index, row in df.iterrows():
    prof = str(row['Professores']).upper()
    if prof != 'NAN':
        if prof.__contains__(','):
            aux = prof.split(',')
            for s in aux:
                if s[0] == ' ':
                    if not searchTXT( s[1:] ):
                        escreveTXT( '31|'+s[1:] )
                elif not searchTXT( s ):
                        escreveTXT( '31|'+s )
        else:
            if not searchTXT( prof ):
                escreveTXT( '31|'+prof )


clearTXT('test_ordering.txt')
sortedTXT('test.txt','test_ordering.txt')
print( printTime()+' | Finalizou processamento.')