import pandas as pd
import collections

DOC_TXT = 'test.txt'
DOC_CSV = 'test.csv'
DOC_AUX_TXT = 'test_aux.txt'
DOC_CURSOS_TXT = 'cursos.txt'
DOC_DOCENTE_CURSO_TXT = 'docentes_cursos.txt'

def clearTXT(doc):
    with open('docs/output/'+doc,'w') as file:
        pass

def escreveTXT(texto,doc):
    with open('docs/output/'+doc,'a+') as f:
        f.write(texto+'\n')
        
def searchTXT(text, doc):
    with open('docs/output/'+doc, 'r') as f:
        encontrou = ''
        for line in f:
            if text in str(line):
                encontrou = str(line)
                break
        return encontrou
    
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
                f.write( line+'\n' )
    clearTXT(DOC_AUX_TXT)

def captureMatricula(file_input, file_output):
    clearTXT(file_output)

    #with open('docs/output/'+file_output,'a+') as f:
    #    f.write( '30|600'+'\n' )

    with open('docs/output/'+file_input, 'r') as r:
        for line in r:
            with open('docs/output/'+file_output,'a+') as f:
                profs = line.split('|')[1]
                cod_curso = line.split('|')[2]
                mat = profs.split(' (')[1].replace(')','')
                f.write( '31|'+mat[:-1]+'|'+str(line[3:]).split(' (')[0]+'|'+cod_curso )
    clearTXT(DOC_AUX_TXT)
    duplicateLineQTDTXT(DOC_TXT,DOC_AUX_TXT)

def linhasVinculosDiarios(file_input, file_output):
    copyFile(file_input,file_output)
    clearTXT(file_input)
#31|matricula|nome_docente|cod_curso
    with open('docs/output/'+file_output, 'r') as r:
        for line in r:
            with open('docs/output/'+file_input,'a+') as f:
                f.write( line.split('|')[0]+'|'+line.split('|')[1]+'|'+line.split('|')[2]+'\n' )
                #for x in range(int(line.split('|')[3])):
                    #f.write( '32|COD_CURSO'+'\n' )
    clearTXT(DOC_AUX_TXT)

print('### SYNC_SUAP_CENSUP ###')

df = pd.read_excel('docs/input/docente_vinculos.xls')
df[['Professores','Diretoria','Período Letivo']].to_csv('docs/output/'+DOC_CSV,index=False,header=False)
clearTXT(DOC_TXT)

df = df.reset_index()
for index, row in df.iterrows():
    prof = str(row['Professores']).upper()
    diretoria = str( row['Diretoria'] )
    curso_nome = str( row['Período Letivo'] )
    if prof != 'NAN' and diretoria == 'SUP':
        if prof.__contains__(','):
            aux = prof.split(',')
            for s in aux:
                if s[0] == ' ':
                    #if not searchTXT( s[1:],DOC_TXT ):
                    cod_curso = searchTXT( curso_nome, DOC_CURSOS_TXT ).split('|')[1]
                    escreveTXT( '31|'+s[1:]+'|'+cod_curso,DOC_TXT )
                else:#if not searchTXT( s,DOC_TXT ):
                    cod_curso = searchTXT( curso_nome, DOC_CURSOS_TXT ).split('|')[1]
                    escreveTXT( '31|'+s+'|'+cod_curso,DOC_TXT )
        else:
            #if not searchTXT( prof,DOC_TXT ):
            cod_curso = searchTXT( curso_nome, DOC_CURSOS_TXT ).split('|')[1]
            escreveTXT( '31|'+prof+'|'+cod_curso,DOC_TXT )

clearTXT(DOC_AUX_TXT)
sortedTXT(DOC_TXT,DOC_AUX_TXT)
captureMatricula(DOC_AUX_TXT,DOC_TXT)
#linhasVinculosDiarios(DOC_TXT,DOC_AUX_TXT)

print('Finalizou processamento.')