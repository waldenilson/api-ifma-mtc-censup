import pandas as pd2

def docenteExterno(matricula):
    if len(matricula) >= 11: # matricula == cpf
        return True
    else: return False

def deficiencia(txt):
    if txt == '-':
        return '0'

def corRaca(txt):
    if str(txt).upper() == 'BRANCA': return '1'
    elif str(txt).upper() == 'PRETA': return '2'
    elif str(txt).upper() == 'PARDA': return '3'
    elif str(txt).upper() == 'AMARELA': return '4'
    elif str(txt).upper() == 'INGÍGENA': return '5'
    else:   return '0'

def nacionalidade(txt):
    return '1'

def paisOrigem(txt):
    return 'BRA'

def escolaridade(txt):
    if 'MESTRE' in str(txt).upper() or 'MESTRADO' in str(txt).upper(): return '5'
    if 'DOUTORADO' in str(txt).upper() or 'DOUTOR' in str(txt).upper(): return '6'
    if 'APERFEI' in str(txt).upper() or 'ESPECI' in str(txt).upper() or 'POS-GRAD' in str(txt).upper(): return '4'
    else:   return '3'

def situacaoDocente(txt):
    if 'APOSENT' not in str(txt).upper(): return '1'
    else: return '1'

def docenteEmExercicio31_12(txt):
    if 'APOSENT' not in str(txt).upper(): return '1'
    else: return '1'

def regimeTrabalho(txt):
    if 'DEDICACAO EXCLUSIVA' in str(txt).upper() or 'EXCLUSIVA' in str(txt).upper(): return '1'
    if '40 HORAS SEMANAIS' in str(txt).upper() or '40 HORAS' in str(txt).upper(): return '2'
    if '20 HORAS SEMANAIS' in str(txt).upper() or '20 HORAS' in str(txt).upper() or '30 HORAS' in str(txt).upper(): return '3'
    else:   return ''

def docenteSubstituto(txt):
    if 'SUBSTITUTO' in str(txt).upper() or 'SUBSTIT' in str(txt).upper(): return '1'
    else: return '0'

def docenteVisitante(txt):
    if 'VISITANTE' in str(txt).upper() or 'VISIT' in str(txt).upper(): return '1'
    else: return '0'

def vinculoDocenteVisitante(txt):
    if docenteVisitante(txt) == '0': return ''
    else: return ''

def docenteCursoSequencial(txt):
    return '0'

def docenteCursoPresencial(txt):
    return '1'

def docenteCursoEaD(mat, df_vinculos):
    encontrou = '0'
    for index, row in df_vinculos.iterrows():
        curso_nome = str( row['Período Letivo'] )
        profmat = str( row['Professores'] )
        if mat in profmat and 'EAD' in curso_nome.upper():
            encontrou = '1'
    return encontrou

def docenteCursoStrictuPresencial(mat, df_vinculos):
    encontrou = '0'
    for index, row in df_vinculos.iterrows():
        curso_nome = str( row['Período Letivo'] )
        profmat = str( row['Professores'] )
        diretoria = str( row['Diretoria'] )
        if mat in profmat and diretoria == 'POS' and ('MESTRADO' in curso_nome.upper() or 'DOUTORADO' in curso_nome.upper()):
            #print( ':: '+profmat+' '+curso_nome.upper() )
            encontrou = '1'
    return encontrou

def docenteCursoStrictuEaD(mat, df_vinculos):
    encontrou = '0'
    for index, row in df_vinculos.iterrows():
        curso_nome = str( row['Período Letivo'] )
        profmat = str( row['Professores'] )
        diretoria = str( row['Diretoria'] )
        if mat in profmat and diretoria == 'POS' and 'EAD' in curso_nome.upper() and ('MESTRADO' in curso_nome.upper() or 'DOUTORADO' in curso_nome.upper()):
            print( ':: '+profmat+' '+curso_nome.upper() )
            encontrou = '1'
    return encontrou

def atuacaoDocentePesquisa(text):
    return '0'

def atuacaoDocenteExtensao(text):
    return '0'

def docenteBolsaPesquisa(text):
    return '0'

def docenteGestao(txt):
    if 'CD' in str(txt).upper() or 'FG' in str(txt).upper() or 'FUC' in str(txt).upper(): return '1'
    else: return '0'
