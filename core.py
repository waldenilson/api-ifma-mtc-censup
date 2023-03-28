import pandas as pd
import collections

DOC_TXT = 'layout_censup_auto.txt'
DOC_DOCENTE_VINCULO_CSV = 'test.csv'
DOC_DOCENTE_DADOS_CSV = 'test1.csv'
DOC_CURSOS_TXT = 'cursos.txt'
DOC_AUX_TXT = 'temp/auxiliar.txt'
DOC_DOCENTE_CURSO_TXT = 'temp/docentes_cursos.txt'

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
    clearTXT(file_output)
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
    #clearTXT(DOC_AUX_TXT)

def captureMatricula(file_input, file_output):
    clearTXT(file_output)

    with open('docs/output/'+file_input, 'r') as r:
        for line in r:
            with open('docs/output/'+file_output,'a+') as f:
                profs = line.split('|')[1]
                cod_curso = line.split('|')[2]
                mat = profs.split(' (')[1].replace(')','')
                f.write( '31|'+mat+'|'+str(line[3:]).split(' (')[0]+'|'+cod_curso+'|\n' )

    clearTXT(DOC_AUX_TXT)

    with open('docs/output/'+file_output, 'r') as r:
        for line in r:
            with open('docs/output/'+file_input,'a+') as f:
                f.write( line.split('|')[0]+'|'+line.split('|')[1]+'|'+line.split('|')[2]+'|\n' )



    #copyFile( DOC_TXT, DOC_AUX_TXT )
    duplicateLineQTDTXT(DOC_TXT,DOC_DOCENTE_CURSO_TXT)
    duplicateLineQTDTXT(DOC_AUX_TXT,DOC_DOCENTE_CURSO_TXT)

def linhasVinculosCursos(file_input, file_output):
    clearTXT(DOC_DOCENTE_CURSO_TXT)

    with open('docs/output/'+DOC_DOCENTE_CURSO_TXT,'a+') as f:
        f.write( '30|600'+'\n' )

    f1 = open('docs/output/'+file_output, 'r')
    l1 = f1.readlines()

    f2 = open('docs/output/'+file_input, 'r')
    l2 = f2.readlines()
    
    for line1 in l1:
        lista = []
        for line2 in l2:
            if str(line1.split('|')[1]) in str(line2):
                lista.append( line2.split('|')[3] )
        linha = line1.split('|')[0]+'|'+line1.split('|')[1]+'|'+line1.split('|')[2]
        for x in range(34):
            linha += '|__'+str(x+3)+'__'
        escreveTXT(linha, DOC_DOCENTE_CURSO_TXT)
        for l in lista:
            escreveTXT( '32|'+str(l), DOC_DOCENTE_CURSO_TXT)
    f1.close()
    f2.close()

    clearTXT(DOC_TXT)
    copyFile(DOC_DOCENTE_CURSO_TXT, DOC_TXT)
    clearTXT(DOC_DOCENTE_CURSO_TXT)
    clearTXT(DOC_AUX_TXT)

def itensLayout():
    clearTXT(DOC_AUX_TXT)
    copyFile(DOC_TXT, DOC_AUX_TXT)
    f = open('docs/output/'+DOC_AUX_TXT,'r')
    ls = f.readlines()
    for l in ls:
        print(str(l)[:-1])
        #if str(l)[0:3] == '32|':
        #    print( 'tudo:*'+str(l)[:-1]+'*' )
        #if compare in str(l) and ts in str(l):
            #l.split('|')[split]
            #escreveTXT(  str(l).replace('__'+str(split)+'__',text) ,DOC_TXT )
            #escreveTXT( str(l).replace(ts,text), DOC_TXT )
            #print( str(l).replace(ts,text)[:-1] )
            #pass
        #elif str(l)[0:3] == '32|' or str(l)[0:3] == '30|':#str('32|') in str(l) or str('30|') in str(l):
            #escreveTXT( str(l) ,DOC_TXT )
            #print( str(l)[:-1] )
            #pass

    f.close()

print('### SYNC_SUAP_CENSUP ###')

df = pd.read_excel('docs/input/docente_vinculos.xls')
df[['Professores','Diretoria','Período Letivo']].to_csv('docs/output/temp/'+DOC_DOCENTE_VINCULO_CSV,index=False,header=False)
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
                    escreveTXT( '31|'+s[1:]+'|'+cod_curso+'|',DOC_TXT )
                else:#if not searchTXT( s,DOC_TXT ):
                    cod_curso = searchTXT( curso_nome, DOC_CURSOS_TXT ).split('|')[1]
                    escreveTXT( '31|'+s+'|'+cod_curso+'|',DOC_TXT )
        else:
            #if not searchTXT( prof,DOC_TXT ):
            cod_curso = searchTXT( curso_nome, DOC_CURSOS_TXT ).split('|')[1]
            escreveTXT( '31|'+prof+'|'+cod_curso+'|',DOC_TXT )

clearTXT(DOC_AUX_TXT)
sortedTXT(DOC_TXT,DOC_AUX_TXT)
captureMatricula(DOC_AUX_TXT,DOC_TXT)
linhasVinculosCursos(DOC_TXT,DOC_AUX_TXT)

itensLayout()

'''
df = pd.read_excel('docs/input/docente_dados_pessoais.xls')
df[['MATRICULA','SERVIDOR','CPF']].to_csv('docs/output/temp/'+DOC_DOCENTE_DADOS_CSV,index=False,header=False)
#clearTXT(DOC_TXT)
df = df.reset_index()
for index, row in df.iterrows():
    prof = str(row['MATRICULA'])
    cpf = str(row['CPF']).replace('.','').replace('-','')
'''



print('Finalizou processamento.')