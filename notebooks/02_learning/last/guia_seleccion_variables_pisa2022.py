"""
═══════════════════════════════════════════════════════════════════════════════
    GUÍA COMPLETA: CÓMO SELECCIONAR VARIABLES EN PISA 2022
    Según tu Objetivo de Investigación
═══════════════════════════════════════════════════════════════════════════════
"""

import pandas as pd
import numpy as np

# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║ CONCEPTOS FUNDAMENTALES                                                    ║
# ╚═══════════════════════════════════════════════════════════════════════════╝

print("""
┌─────────────────────────────────────────────────────────────────────────────┐
│ 🎯 REGLA DE ORO:                                                            │
│                                                                             │
│ Las variables que agrupes deben medir aspectos RELACIONADOS del mismo      │
│ constructo o concepto. Si mezclas peras con manzanas, obtendrás factores   │
│ sin sentido.                                                               │
└─────────────────────────────────────────────────────────────────────────────┘
""")

# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║ ESTRUCTURA DE CÓDIGOS EN PISA 2022                                        ║
# ╚═══════════════════════════════════════════════════════════════════════════╝

def entender_codigos_pisa():
    """
    Explicación de cómo están codificadas las variables en PISA
    """
    print("""
    ╔═════════════════════════════════════════════════════════════════════════╗
    ║ 📚 ESTRUCTURA DE CÓDIGOS EN PISA 2022                                   ║
    ╚═════════════════════════════════════════════════════════════════════════╝
    
    Los códigos siguen un patrón:
    
    ST###Q##XX
    ││ │  │  └─> Parte de la pregunta (TA, TB, TC...)
    ││ │  └────> Número de ítem dentro de la pregunta
    ││ └───────> Q = Question (pregunta)
    │└─────────> Número de la escala/constructo (034 = ansiedad matemática)
    └──────────> ST = Student (estudiante), SC = School, TC = Teacher
    
    EJEMPLOS:
    • ST034Q01TA = Student, Escala 034 (ansiedad), Pregunta 01, parte A
    • ST183Q01HA = Student, Escala 183 (bullying), Pregunta 01, parte A
    • ESCS = Index of Economic, Social and Cultural Status
    """)

# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║ CASO 1: INVESTIGAR ANSIEDAD Y ACTITUDES HACIA LAS MATEMÁTICAS            ║
# ╚═══════════════════════════════════════════════════════════════════════════╝

def caso1_ansiedad_matematica():
    """
    Variables para investigar ansiedad matemática
    """
    print("""
    ╔═════════════════════════════════════════════════════════════════════════╗
    ║ CASO 1: ANSIEDAD Y ACTITUDES HACIA LAS MATEMÁTICAS                      ║
    ╚═════════════════════════════════════════════════════════════════════════╝
    
    🎯 OBJETIVO: Entender los factores emocionales relacionados con matemáticas
    
    📊 VARIABLES A SELECCIONAR:
    """)
    
    variables = {
        'ANSIEDAD MATEMÁTICA (ST034)': {
            'ST034Q01TA': 'Me preocupo porque tendré dificultades en clases de matemáticas',
            'ST034Q02TA': 'Me pongo muy tenso cuando tengo que hacer tareas de matemáticas',
            'ST034Q03TA': 'Me pongo muy nervioso al hacer problemas de matemáticas',
            'ST034Q04TA': 'Me siento indefenso al hacer un problema de matemáticas',
            'ST034Q05TA': 'Me preocupo por obtener malas notas en matemáticas',
            'ST034Q06TA': 'Me siento ansioso cuando pienso en matemáticas'
        },
        
        'AUTOEFICACIA MATEMÁTICA (ST035)': {
            'ST035Q01TA': 'Puedo resolver ecuaciones lineales',
            'ST035Q02TA': 'Puedo calcular el área de figuras',
            'ST035Q03TA': 'Puedo resolver problemas con fracciones',
            'ST035Q04TA': 'Puedo interpretar gráficos',
            'ST035Q05TA': 'Puedo resolver problemas de proporcionalidad'
        },
        
        'MOTIVACIÓN MATEMÁTICA (ST182)': {
            'ST182Q03HA': 'Disfruto leyendo sobre matemáticas',
            'ST182Q04HA': 'Espero con entusiasmo mis clases de matemáticas',
            'ST182Q05HA': 'Hago matemáticas porque me gusta',
            'ST182Q06HA': 'Me interesan las cosas que aprendo en matemáticas'
        }
    }
    
    # Mostrar las variables organizadas
    for constructo, items in variables.items():
        print(f"\n{'='*70}")
        print(f"📐 {constructo}")
        print(f"{'='*70}")
        for codigo, descripcion in items.items():
            print(f"   {codigo}: {descripcion}")
    
    print("""
    
    💡 RESULTADOS ESPERADOS DEL EFA:
    • Factor 1: "Ansiedad Matemática" (items ST034)
    • Factor 2: "Autoeficacia Matemática" (items ST035)  
    • Factor 3: "Motivación Intrínseca" (items ST182)
    
    📊 NÚMERO DE VARIABLES: 15 variables totales
    """)
    
    # Crear lista para análisis
    todas_variables = []
    for items in variables.values():
        todas_variables.extend(items.keys())
    
    return todas_variables

# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║ CASO 2: INVESTIGAR BIENESTAR Y CLIMA ESCOLAR                             ║
# ╚═══════════════════════════════════════════════════════════════════════════╝

def caso2_bienestar_escolar():
    """
    Variables para investigar bienestar y clima escolar
    """
    print("""
    ╔═════════════════════════════════════════════════════════════════════════╗
    ║ CASO 2: BIENESTAR Y CLIMA ESCOLAR                                       ║
    ╚═════════════════════════════════════════════════════════════════════════╝
    
    🎯 OBJETIVO: Entender factores de bienestar estudiantil y ambiente escolar
    
    📊 VARIABLES A SELECCIONAR:
    """)
    
    variables = {
        'SENTIDO DE PERTENENCIA (ST033)': {
            'ST033Q01TA': 'Me siento como un extraño en la escuela',
            'ST033Q02TA': 'Hago amigos fácilmente en la escuela',
            'ST033Q03TA': 'Siento que pertenezco a la escuela',
            'ST033Q04TA': 'Me siento incómodo y fuera de lugar',
            'ST033Q05TA': 'Parece que le caigo bien a otros estudiantes',
            'ST033Q06TA': 'Me siento solo en la escuela'
        },
        
        'EXPERIENCIAS DE BULLYING (ST183)': {
            'ST183Q01HA': 'Otros estudiantes me dejaron fuera a propósito',
            'ST183Q02HA': 'Otros estudiantes se burlaron de mí',
            'ST183Q03HA': 'Fui amenazado por otros estudiantes',
            'ST183Q04HA': 'Otros estudiantes me quitaron o destruyeron mis cosas',
            'ST183Q05HA': 'Fui golpeado o empujado por otros estudiantes',
            'ST183Q06HA': 'Otros estudiantes esparcieron rumores desagradables sobre mí'
        },
        
        'APOYO DEL PROFESOR (ST100)': {
            'ST100Q01TA': 'El profesor muestra interés en el aprendizaje de cada estudiante',
            'ST100Q02TA': 'El profesor da ayuda extra cuando los estudiantes la necesitan',
            'ST100Q03TA': 'El profesor ayuda a los estudiantes con su aprendizaje',
            'ST100Q04TA': 'El profesor continúa enseñando hasta que los estudiantes entienden'
        },
        
        'SATISFACCIÓN CON LA VIDA (ST016Q01NA)': {
            'ST016Q01NA': 'Satisfacción general con la vida actual (escala 0-10)'
        }
    }
    
    for constructo, items in variables.items():
        print(f"\n{'='*70}")
        print(f"🏫 {constructo}")
        print(f"{'='*70}")
        for codigo, descripcion in items.items():
            print(f"   {codigo}: {descripcion}")
    
    print("""
    
    💡 RESULTADOS ESPERADOS DEL EFA:
    • Factor 1: "Pertenencia Escolar" (items ST033 positivos)
    • Factor 2: "Aislamiento Social" (items ST033 negativos + ST183)
    • Factor 3: "Apoyo Docente" (items ST100)
    • Factor 4: "Bienestar General" (ST016 + items positivos)
    
    📊 NÚMERO DE VARIABLES: 17 variables totales
    """)
    
    todas_variables = []
    for items in variables.values():
        todas_variables.extend(items.keys())
    
    return todas_variables

# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║ CASO 3: INVESTIGAR USO DE TECNOLOGÍA Y APRENDIZAJE DIGITAL               ║
# ╚═══════════════════════════════════════════════════════════════════════════╝

def caso3_tecnologia_aprendizaje():
    """
    Variables para investigar tecnología y aprendizaje digital
    """
    print("""
    ╔═════════════════════════════════════════════════════════════════════════╗
    ║ CASO 3: USO DE TECNOLOGÍA Y APRENDIZAJE DIGITAL                         ║
    ╚═════════════════════════════════════════════════════════════════════════╝
    
    🎯 OBJETIVO: Entender patrones de uso tecnológico y su relación con aprendizaje
    
    📊 VARIABLES A SELECCIONAR:
    """)
    
    variables = {
        'RECURSOS TIC EN CASA (ST011)': {
            'ST011Q01TA': 'Escritorio para estudiar',
            'ST011Q02TA': 'Habitación propia',
            'ST011Q03TA': 'Lugar tranquilo para estudiar',
            'ST011Q04TA': 'Computadora para trabajo escolar',
            'ST011Q05TA': 'Software educativo',
            'ST011Q06TA': 'Conexión a Internet',
            'ST011Q07TA': 'Libros de literatura clásica',
            'ST011Q08TA': 'Libros de poesía',
            'ST011Q09TA': 'Obras de arte',
            'ST011Q10TA': 'Libros para ayudar con tareas',
            'ST011Q11TA': 'Libros de referencia técnica',
            'ST011Q12TA': 'Diccionario',
            'ST011Q16NA': 'Libros sobre arte, música o diseño',
            'ST011Q17TA': 'Más de 100 libros en casa'
        },
        
        'FRECUENCIA DE USO DE TIC (ST176)': {
            'ST176Q01HA': 'Uso de dispositivos digitales fuera de la escuela entre semana',
            'ST176Q02HA': 'Uso de dispositivos digitales fuera de la escuela los fines de semana',
            'ST176Q03HA': 'Uso de dispositivos digitales en la escuela'
        },
        
        'ACTIVIDADES DIGITALES PARA APRENDIZAJE (ST177)': {
            'ST177Q01HA': 'Buscar información para tareas',
            'ST177Q02HA': 'Navegar por Internet para trabajo escolar',
            'ST177Q03HA': 'Usar email para comunicación escolar',
            'ST177Q04HA': 'Descargar material del sitio web de la escuela',
            'ST177Q05HA': 'Subir tareas al sitio web de la escuela'
        }
    }
    
    for constructo, items in variables.items():
        print(f"\n{'='*70}")
        print(f"💻 {constructo}")
        print(f"{'='*70}")
        for codigo, descripcion in items.items():
            print(f"   {codigo}: {descripcion}")
    
    print("""
    
    💡 RESULTADOS ESPERADOS DEL EFA:
    • Factor 1: "Recursos Digitales" (items ST011 relacionados con TIC)
    • Factor 2: "Recursos Culturales" (items ST011 de libros y arte)
    • Factor 3: "Intensidad de Uso Digital" (items ST176)
    • Factor 4: "Uso Académico de TIC" (items ST177)
    
    📊 NÚMERO DE VARIABLES: 22 variables totales
    """)
    
    todas_variables = []
    for items in variables.values():
        todas_variables.extend(items.keys())
    
    return todas_variables

# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║ CASO 4: INVESTIGAR FACTORES SOCIOECONÓMICOS                              ║
# ╚═══════════════════════════════════════════════════════════════════════════╝

def caso4_factores_socioeconomicos():
    """
    Variables para investigar factores socioeconómicos
    """
    print("""
    ╔═════════════════════════════════════════════════════════════════════════╗
    ║ CASO 4: FACTORES SOCIOECONÓMICOS Y RECURSOS FAMILIARES                  ║
    ╚═════════════════════════════════════════════════════════════════════════╝
    
    🎯 OBJETIVO: Entender la estructura del capital económico, social y cultural
    
    📊 VARIABLES A SELECCIONAR:
    """)
    
    variables = {
        'ÍNDICES SOCIOECONÓMICOS PRINCIPALES': {
            'ESCS': 'Índice de Estatus Económico, Social y Cultural',
            'WEALTH': 'Índice de Riqueza Familiar',
            'CULTPOSS': 'Posesiones Culturales',
            'HEDRES': 'Recursos Educativos del Hogar',
            'HOMEPOS': 'Posesiones del Hogar'
        },
        
        'EDUCACIÓN DE LOS PADRES': {
            'MISCED': 'Educación de la madre (ISCED)',
            'FISCED': 'Educación del padre (ISCED)',
            'HISCED': 'Educación más alta de los padres',
            'PARED': 'Índice de educación parental en años'
        },
        
        'OCUPACIÓN DE LOS PADRES': {
            'BMMJ1': 'Ocupación de la madre',
            'BFMJ2': 'Ocupación del padre',
            'HISEI': 'Estatus ocupacional más alto de los padres',
            'ISEI': 'Índice socioeconómico internacional de estatus ocupacional'
        }
    }
    
    for constructo, items in variables.items():
        print(f"\n{'='*70}")
        print(f"💰 {constructo}")
        print(f"{'='*70}")
        for codigo, descripcion in items.items():
            print(f"   {codigo}: {descripcion}")
    
    print("""
    
    💡 RESULTADOS ESPERADOS DEL EFA:
    • Factor 1: "Capital Económico" (WEALTH, HOMEPOS)
    • Factor 2: "Capital Cultural" (CULTPOSS, educación padres)
    • Factor 3: "Capital Social" (ocupación padres, HISEI)
    • Factor 4: "Recursos Educativos" (HEDRES, apoyo familiar)
    
    📊 NÚMERO DE VARIABLES: 13 variables totales
    
    ⚠️ NOTA: Estos índices ya son resultado de análisis factoriales previos,
    así que hacer EFA sobre ellos busca factores de segundo orden.
    """)
    
    todas_variables = []
    for items in variables.values():
        todas_variables.extend(items.keys())
    
    return todas_variables

# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║ CASO 5: INVESTIGAR ESTRATEGIAS DE APRENDIZAJE Y METACOGNICIÓN            ║
# ╚═══════════════════════════════════════════════════════════════════════════╝

def caso5_estrategias_aprendizaje():
    """
    Variables para investigar estrategias de aprendizaje
    """
    print("""
    ╔═════════════════════════════════════════════════════════════════════════╗
    ║ CASO 5: ESTRATEGIAS DE APRENDIZAJE Y METACOGNICIÓN                      ║
    ╚═════════════════════════════════════════════════════════════════════════╝
    
    🎯 OBJETIVO: Identificar patrones en estrategias de estudio y metacognición
    
    📊 VARIABLES A SELECCIONAR:
    """)
    
    variables = {
        'ESTRATEGIAS DE MEMORIZACIÓN': {
            'MEMOR': 'Índice de estrategias de memorización',
            'ST097Q01TA': 'Memorizo todo lo que tengo que aprender',
            'ST097Q02TA': 'Leo el material varias veces',
            'ST097Q03TA': 'Leo el texto tantas veces que puedo recitarlo',
            'ST097Q04TA': 'Leo una y otra vez el texto'
        },
        
        'ESTRATEGIAS DE ELABORACIÓN': {
            'ELAB': 'Índice de estrategias de elaboración',
            'ST097Q05TA': 'Trato de relacionar el material nuevo con lo que ya sé',
            'ST097Q06TA': 'Relaciono el material con otras asignaturas',
            'ST097Q07TA': 'Pienso cómo la información podría ser útil fuera de la escuela',
            'ST097Q08TA': 'Trato de entender mejor relacionando con mis experiencias'
        },
        
        'ESTRATEGIAS DE CONTROL': {
            'CSTRAT': 'Índice de estrategias de control',
            'ST097Q09TA': 'Verifico si entiendo lo que he leído',
            'ST097Q10TA': 'Trato de identificar los conceptos que no entiendo bien',
            'ST097Q11TA': 'Me aseguro de recordar los puntos más importantes',
            'ST097Q12TA': 'Cuando no entiendo algo, busco información adicional'
        }
    }
    
    for constructo, items in variables.items():
        print(f"\n{'='*70}")
        print(f"📚 {constructo}")
        print(f"{'='*70}")
        for codigo, descripcion in items.items():
            print(f"   {codigo}: {descripcion}")
    
    print("""
    
    💡 RESULTADOS ESPERADOS DEL EFA:
    • Factor 1: "Aprendizaje Superficial" (estrategias de memorización)
    • Factor 2: "Aprendizaje Profundo" (estrategias de elaboración)
    • Factor 3: "Autorregulación" (estrategias de control)
    
    📊 NÚMERO DE VARIABLES: 15 variables totales
    """)
    
    todas_variables = []
    for items in variables.values():
        todas_variables.extend(items.keys())
    
    return todas_variables

# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║ FUNCIÓN PARA PREPARAR ANÁLISIS PERSONALIZADO                              ║
# ╚═══════════════════════════════════════════════════════════════════════════╝

def preparar_analisis_personalizado(df, caso_elegido):
    """
    Prepara el dataset para EFA según el caso elegido
    """
    print("""
    ╔═════════════════════════════════════════════════════════════════════════╗
    ║ PREPARACIÓN DEL ANÁLISIS PERSONALIZADO                                   ║
    ╚═════════════════════════════════════════════════════════════════════════╝
    """)
    
    # Obtener variables según el caso
    if caso_elegido == 1:
        variables = caso1_ansiedad_matematica()
    elif caso_elegido == 2:
        variables = caso2_bienestar_escolar()
    elif caso_elegido == 3:
        variables = caso3_tecnologia_aprendizaje()
    elif caso_elegido == 4:
        variables = caso4_factores_socioeconomicos()
    elif caso_elegido == 5:
        variables = caso5_estrategias_aprendizaje()
    else:
        print("❌ Caso no válido. Elige entre 1-5")
        return None
    
    # Verificar qué variables existen en el dataset
    variables_existentes = [v for v in variables if v in df.columns]
    variables_faltantes = [v for v in variables if v not in df.columns]
    
    print(f"\n📊 VERIFICACIÓN DE VARIABLES:")
    print(f"   ✅ Variables encontradas: {len(variables_existentes)}/{len(variables)}")
    print(f"   ❌ Variables faltantes: {len(variables_faltantes)}")
    
    if variables_faltantes:
        print(f"\n   Variables que no están en tu dataset:")
        for v in variables_faltantes[:10]:  # Mostrar máximo 10
            print(f"      • {v}")
    
    if len(variables_existentes) < 3:
        print(f"\n⚠️ ADVERTENCIA: Solo se encontraron {len(variables_existentes)} variables.")
        print("   Se necesitan al menos 3 variables para hacer EFA.")
        print("   Verifica que tu dataset tiene las variables correctas.")
        return None
    
    # Crear subset con las variables existentes
    datos_para_efa = df[variables_existentes].copy()
    
    # Información sobre datos faltantes
    n_completos = datos_para_efa.dropna().shape[0]
    n_total = len(datos_para_efa)
    porcentaje_completos = (n_completos / n_total) * 100
    
    print(f"\n📈 CALIDAD DE DATOS:")
    print(f"   • Casos totales: {n_total:,}")
    print(f"   • Casos completos: {n_completos:,} ({porcentaje_completos:.1f}%)")
    
    if porcentaje_completos < 50:
        print(f"   ⚠️ Muchos datos faltantes. Considera imputación.")
    
    # Generar código para el análisis
    print(f"\n💻 CÓDIGO PARA TU ANÁLISIS:")
    print("="*70)
    print(f"""
# Cargar tu dataset
import pandas as pd
from factor_analyzer import FactorAnalyzer

# Leer datos
df = pd.read_csv('tu_dataset_pisa2022.csv')

# Variables para tu análisis (Caso {caso_elegido})
variables = {variables_existentes[:5]}  # ... y más

# Preparar datos
datos_efa = df[variables].dropna()

# Realizar EFA
fa = FactorAnalyzer(n_factors=3, rotation='varimax')
fa.fit(datos_efa)

# Ver resultados
print(fa.loadings_)
    """)
    
    return datos_para_efa, variables_existentes

# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║ RECOMENDACIONES FINALES                                                    ║
# ╚═══════════════════════════════════════════════════════════════════════════╝

def mostrar_recomendaciones():
    """
    Muestra recomendaciones finales para selección de variables
    """
    print("""
    ╔═════════════════════════════════════════════════════════════════════════╗
    ║ 📚 RECOMENDACIONES FINALES PARA SELECCIONAR VARIABLES                    ║
    ╚═════════════════════════════════════════════════════════════════════════╝
    
    ✅ MEJORES PRÁCTICAS:
    
    1. COHERENCIA CONCEPTUAL es lo más importante
       • Las variables deben medir aspectos relacionados
       • No mezcles conceptos muy diferentes
    
    2. CONOCE TUS VARIABLES
       • Lee el cuestionario original de PISA
       • Entiende qué pregunta exactamente cada ítem
       • Revisa el manual técnico de PISA
    
    3. TAMAÑO APROPIADO
       • Entre 5-20 variables es ideal para empezar
       • Con menos de 3 no puedes hacer EFA
       • Con más de 30 se vuelve difícil de interpretar
    
    4. CALIDAD DE DATOS
       • Verifica valores faltantes (<30% es aceptable)
       • Revisa la distribución de respuestas
       • Elimina variables con poca variabilidad
    
    5. VALIDACIÓN
       • Los factores resultantes deben tener sentido teórico
       • Compara con estudios previos de PISA
       • Valida con expertos en educación si es posible
    
    ❌ ERRORES COMUNES A EVITAR:
    
    1. Mezclar variables de diferentes niveles
       • No combines variables del estudiante con variables de la escuela
    
    2. Incluir variables demográficas en el EFA
       • Género, edad, país NO van en el EFA
       • Úsalas después para comparar grupos
    
    3. Incluir variables de resultado
       • Los puntajes (PV1MATH, etc.) son resultados, no predictores
       • Analízalos por separado o como variable dependiente
    
    4. Ignorar la teoría
       • No hagas EFA "a ciegas" con todas las variables
       • Siempre ten una hipótesis sobre qué factores esperas
    
    💡 RECURSOS ÚTILES:
    
    • Manual Técnico PISA 2022: 
      https://www.oecd.org/pisa/data/pisa2022technicalreport/
    
    • Cuestionarios PISA 2022:
      https://www.oecd.org/pisa/data/2022database/
    
    • Diccionario de Variables (Codebook):
      Busca el archivo "PISA2022_CODEBOOK.xlsx" en los datos descargados
    
    📊 PRÓXIMOS PASOS:
    
    1. Elige tu caso de estudio (1-5) o define el tuyo propio
    2. Verifica que tienes las variables necesarias
    3. Ejecuta el EFA con el tutorial principal
    4. Interpreta los factores basándote en la teoría
    5. Usa los factores para análisis posteriores (LCA, regresión, etc.)
    """)

# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║ EJEMPLO DE USO COMPLETO                                                    ║
# ╚═══════════════════════════════════════════════════════════════════════════╝

if __name__ == "__main__":
    print("""
    ╔═════════════════════════════════════════════════════════════════════════╗
    ║ 🎯 GUÍA DE SELECCIÓN DE VARIABLES PARA EFA EN PISA 2022                ║
    ╚═════════════════════════════════════════════════════════════════════════╝
    
    Esta guía te muestra 5 casos típicos de investigación con PISA:
    
    1️⃣ Ansiedad y Actitudes hacia las Matemáticas
    2️⃣ Bienestar y Clima Escolar
    3️⃣ Uso de Tecnología y Aprendizaje Digital
    4️⃣ Factores Socioeconómicos
    5️⃣ Estrategias de Aprendizaje y Metacognición
    
    Para usar esta guía:
    
    >>> from guia_seleccion_variables_pisa2022 import *
    
    # Ver un caso específico:
    >>> caso1_ansiedad_matematica()
    
    # Preparar tu análisis:
    >>> import pandas as pd
    >>> df = pd.read_csv('tu_dataset_pisa2022.csv')
    >>> datos, variables = preparar_analisis_personalizado(df, caso=1)
    
    # Ver recomendaciones:
    >>> mostrar_recomendaciones()
    
    ¡Elige tu objetivo de investigación y selecciona las variables apropiadas!
    """)
    
    # Mostrar todos los casos
    print("\n" + "="*80)
    entender_codigos_pisa()
    print("\n" + "="*80)
    mostrar_recomendaciones()
