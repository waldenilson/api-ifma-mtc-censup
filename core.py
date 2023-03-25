import pandas as pd
import collections

DOC_TXT = 'test.txt'
DOC_CSV = 'test.csv'
DOC_AUX_TXT = 'test_aux.txt'

def clearTXT(doc):
    with open('docs/output/'+doc,'w') as file:
        pass

def escreveTXT(texto,doc):
    with open('docs/output/'+doc,'a+') as f:
        f.write(texto+'\n')
        
def searchTXT(text, doc):
    with open('docs/output/'+doc) as f:
        if text in f.read():
            return True
        else:
            return False

def sortedTXT(file_input,file_output):
    with open('docs/output/'+file_input, 'r') as r:
        for line in sorted(r):
            with open('docs/output/'+file_output,'a+') as f:
                f.write(line)

def copyFile(file_input, file_output):
    with open('docs/output/'+file_input, 'r') as r:
        for line in r:
            with open('docs/output/'+file_output,'a+') as f:
                f.write( line )
    
def duplicateLineQTDTXT(file_input, file_output):
    copyFile(file_input,file_output)
    clearTXT(file_input)

    with open('docs/output/'+file_output, 'r') as f:
        counts = collections.Counter(l.strip() for l in f)
        for line, count in counts.most_common():
            with open('docs/output/'+file_input,'a+') as f:
                f.write( line+'=='+str(count)+'\n' )
    clearTXT(DOC_AUX_TXT)

def captureMatricula(file_input, file_output):
    clearTXT(file_output)

    #with open('docs/output/'+file_output,'a+') as f:
    #    f.write( '30|600'+'\n' )

    with open('docs/output/'+file_input, 'r') as r:
        for line in r:
            with open('docs/output/'+file_output,'a+') as f:
                mat = line[3:].split(' (')[1].replace(')','')
                f.write( '31|'+mat[:-1]+'|'+str(line[3:]).split(' (')[0]+'\n' )
    clearTXT(DOC_AUX_TXT)
    duplicateLineQTDTXT(DOC_TXT,DOC_AUX_TXT)

def linhasVinculosDiarios(file_input, file_output):
    copyFile(file_input,file_output)
    clearTXT(file_input)

    with open('docs/output/'+file_output, 'r') as r:
        for line in r:
            with open('docs/output/'+file_input,'a+') as f:
                f.write( line.split('==')[0]+'\n' )
                for x in range(int(line.split('==')[1])):
                    f.write( '32|COD_CURSO'+'\n' )
    clearTXT(DOC_AUX_TXT)

print('### SYNC_SUAP_CENSUP ###')

df = pd.read_excel('docs/input/docente_vinculos.xls')
df[['Professores','Diretoria']].to_csv('docs/output/'+DOC_CSV,index=False,header=False)
clearTXT(DOC_TXT)

df = df.reset_index()
for index, row in df.iterrows():
    prof = str(row['Professores']).upper()
    diretoria = str( row['Diretoria'] )
    if prof != 'NAN' and diretoria == 'SUP':
        if prof.__contains__(','):
            aux = prof.split(',')
            for s in aux:
                if s[0] == ' ':
                    #if not searchTXT( s[1:],DOC_TXT ):
                    escreveTXT( '31|'+s[1:],DOC_TXT )
                else:#if not searchTXT( s,DOC_TXT ):
                    escreveTXT( '31|'+s,DOC_TXT )
        else:
            #if not searchTXT( prof,DOC_TXT ):
            escreveTXT( '31|'+prof,DOC_TXT )

clearTXT(DOC_AUX_TXT)
sortedTXT(DOC_TXT,DOC_AUX_TXT)
captureMatricula(DOC_AUX_TXT,DOC_TXT)
linhasVinculosDiarios(DOC_TXT,DOC_AUX_TXT)

print('Finalizou processamento.')