import pandas as pd
import collections
import datetime
import functions as func

DOC_TXT = 'layout_censup_auto.txt'
DOC_DOCENTE_VINCULO_CSV = 'test.csv'
DOC_DOCENTE_DADOS_CSV = 'test1.csv'
DOC_CURSOS_TXT = 'cursos.txt'
DOC_AUX_TXT = 'temp/auxiliar.txt'
DOC_DOCENTE_CURSO_TXT = 'temp/docentes_cursos.txt'

df_dados_pessoais = ''
df_dados_vinculos = ''

def clearTXT(doc):
    with open('docs/output/'+doc,'w') as file:
        pass

def escreveTXT(texto,doc):
    with open('docs/output/'+doc,'a+') as f:
        f.write(texto+'\n')
        
def searchTXT(text, doc):
    with open('docs/output/'+doc, 'r', encoding='utf8') as f:
        encontrou = ''
        for line in f:
            if str(text) in str(line):
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
    
def captureMatricula(file_input, file_output):
    clearTXT(file_output)

    with open('docs/output/'+file_input, 'r') as r:
        for line in r:
            with open('docs/output/'+file_output,'a+') as f:
                profs = line.split('|')[1]
                cod_curso = line.split('|')[2]
                mat = profs.split(' (')[1].replace(')','')
    
                if func.docenteExterno(matricula=mat) :
                    pass #print( 'matricula==cpf '+profs )
                else:
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
    clearTXT(DOC_TXT)
    f = open('docs/output/'+DOC_AUX_TXT,'r')
    ls = f.readlines()
    
    for l in ls:
        if str(l)[0:3] == '31|':
            encontrou_docente_dados_pessoais = ''
            mat = str(l).split('|')[1]
            df_dados_pessoais = pd.read_excel('docs/input/docente_dados_pessoais_tudo.xls')
            df_dados_pessoais[['MATRICULA','SERVIDOR','CPF','NASCIMENTO DATA','DEFICIENCIA','RACA','NASCIMENTO MUNICIPIO','TITULACAO','SITUACAO','JORNADA TRABALHO','FUNCAO DISPLAY']].to_csv('docs/output/temp/'+DOC_DOCENTE_DADOS_CSV,index=False,header=False)
            df_dados_pessoais = df_dados_pessoais.reset_index()
            #cpf = ''
            for index, row in df_dados_pessoais.iterrows():
                prof = str(row['MATRICULA'])
                if prof == mat:
                    encontrou_docente_dados_pessoais = prof
                    break
            if encontrou_docente_dados_pessoais == '':
                print( 'ALERTA. Nao encontrou docente Matricula: '+mat+' na planilha de dados pessoais!' )
            else:#if cpf != '':
                str_dados_docente = str(l)[:-1].replace('__'+str(3)+'__',str(row['CPF']).replace('.','').replace('-',''))                
                # documento estrangeiro / opcional
                str_dados_docente = str_dados_docente.replace('__'+str(4)+'__','')                
                # data nascimento
                str_dados_docente = str_dados_docente.replace('__'+str(5)+'__',str(row['NASCIMENTO DATA']).replace('/',''))                
                # cor/raça
                str_dados_docente = str_dados_docente.replace('__'+str(6)+'__',func.corRaca(str(row['RACA'])))                
                # nacionalidade
                str_dados_docente = str_dados_docente.replace('__'+str(7)+'__',func.nacionalidade(str(row['NASCIMENTO MUNICIPIO'])))                
                # pais de origem
                str_dados_docente = str_dados_docente.replace('__'+str(8)+'__',func.paisOrigem(str(row['NASCIMENTO MUNICIPIO'])))                
                # UF de nascimento / opcional
                str_dados_docente = str_dados_docente.replace('__'+str(9)+'__','')                
                # municipio de nascimento / opcional
                str_dados_docente = str_dados_docente.replace('__'+str(10)+'__','')                

                # deficiencia
                str_dados_docente = str_dados_docente.replace('__'+str(11)+'__',func.deficiencia(str(row['DEFICIENCIA'])))                
                # deficiencia item 1
                str_dados_docente = str_dados_docente.replace('__'+str(12)+'__',func.deficiencia(str(row['DEFICIENCIA'])))                
                # deficiencia item 2
                str_dados_docente = str_dados_docente.replace('__'+str(13)+'__',func.deficiencia(str(row['DEFICIENCIA'])))                
                # deficiencia item 3
                str_dados_docente = str_dados_docente.replace('__'+str(14)+'__',func.deficiencia(str(row['DEFICIENCIA'])))                
                # deficiencia item 4
                str_dados_docente = str_dados_docente.replace('__'+str(15)+'__',func.deficiencia(str(row['DEFICIENCIA'])))                
                # deficiencia item 5
                str_dados_docente = str_dados_docente.replace('__'+str(16)+'__',func.deficiencia(str(row['DEFICIENCIA'])))                
                # deficiencia item 6
                str_dados_docente = str_dados_docente.replace('__'+str(17)+'__',func.deficiencia(str(row['DEFICIENCIA'])))                
                # deficiencia item 7
                str_dados_docente = str_dados_docente.replace('__'+str(18)+'__',func.deficiencia(str(row['DEFICIENCIA'])))                
                # deficiencia item 8
                str_dados_docente = str_dados_docente.replace('__'+str(19)+'__',func.deficiencia(str(row['DEFICIENCIA'])))                
                # deficiencia item 9
                str_dados_docente = str_dados_docente.replace('__'+str(20)+'__',func.deficiencia(str(row['DEFICIENCIA'])))                

                # escolaridade/titulacao
                str_dados_docente = str_dados_docente.replace('__'+str(21)+'__',func.escolaridade(str(row['TITULACAO'])))                

                # situacao do docente
                str_dados_docente = str_dados_docente.replace('__'+str(22)+'__',func.situacaoDocente(str(row['SITUACAO'])))                
                # docente em exercicio 31/12
                str_dados_docente = str_dados_docente.replace('__'+str(23)+'__',func.docenteEmExercicio31_12(str(row['SITUACAO'])))                
                # regime de trabalho
                str_dados_docente = str_dados_docente.replace('__'+str(24)+'__',func.regimeTrabalho(str(row['JORNADA TRABALHO'])))                
                # docente substituto
                str_dados_docente = str_dados_docente.replace('__'+str(25)+'__',func.docenteSubstituto(str(row['SITUACAO'])))                
                # docente visitante
                str_dados_docente = str_dados_docente.replace('__'+str(26)+'__',func.docenteVisitante(str(row['SITUACAO'])))                
                # vinculo docente visitante
                str_dados_docente = str_dados_docente.replace('__'+str(27)+'__',func.vinculoDocenteVisitante(str(row['SITUACAO'])))                
                # docente curso sequencial
                str_dados_docente = str_dados_docente.replace('__'+str(28)+'__',func.docenteCursoSequencial(str(row['SITUACAO'])))                
                # docente graduacao presencial
                str_dados_docente = str_dados_docente.replace('__'+str(29)+'__',func.docenteCursoPresencial(str(row['SITUACAO'])))                
                # docente graduacao a distancia
                str_dados_docente = str_dados_docente.replace('__'+str(30)+'__',func.docenteCursoEaD( mat, df_dados_vinculos ))                
                # docente strictu presencial
                str_dados_docente = str_dados_docente.replace('__'+str(31)+'__',func.docenteCursoStrictuPresencial( mat, df_dados_vinculos ))                
                # docente strictu a distancia
                str_dados_docente = str_dados_docente.replace('__'+str(32)+'__',func.docenteCursoStrictuEaD( mat, df_dados_vinculos ))                

                # atuacao docente pesquisa
                str_dados_docente = str_dados_docente.replace('__'+str(33)+'__',func.atuacaoDocentePesquisa( mat ))                
                # atuacao docente extensao
                str_dados_docente = str_dados_docente.replace('__'+str(34)+'__',func.atuacaoDocenteExtensao( mat ))                

                # docente em gestao
                str_dados_docente = str_dados_docente.replace('__'+str(35)+'__',func.docenteGestao(str(row['FUNCAO DISPLAY'])))                

                # bolsa pesquisa
                str_dados_docente = str_dados_docente.replace('__'+str(36)+'__',func.docenteBolsaPesquisa( mat ))                

                escreveTXT(  str_dados_docente ,DOC_TXT )


        elif str(l)[0:3] == '30|' or str(l)[0:3] == '32|':
            escreveTXT( str(l)[:-1] ,DOC_TXT )
    f.close()

print('\n\n### SYNC_SUAP_CENSUP ###')
inicio = datetime.datetime.now()

df_dados_vinculos = pd.read_excel('docs/input/docente_vinculos.xls')
df_dados_vinculos[['Professores','Diretoria','Período Letivo']].to_csv('docs/output/temp/'+DOC_DOCENTE_VINCULO_CSV,index=False,header=False)
clearTXT(DOC_TXT)
df_dados_vinculos = df_dados_vinculos.reset_index()
for index, row in df_dados_vinculos.iterrows():
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

fim = datetime.datetime.now()
print('\nFim do processamento.\n'+str( int((fim - inicio).total_seconds()) )+' segundos.')