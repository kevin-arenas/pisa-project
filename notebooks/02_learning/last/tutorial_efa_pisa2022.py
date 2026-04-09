"""
═══════════════════════════════════════════════════════════════════════════════
    TUTORIAL COMPLETO: ANÁLISIS FACTORIAL EXPLORATORIO (EFA) EN PISA 2022
    Aprendiendo desde Cero - Paso a Paso
═══════════════════════════════════════════════════════════════════════════════
"""

# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║ PARTE 0: CONFIGURACIÓN INICIAL Y CONCEPTOS BÁSICOS                         ║
# ╚═══════════════════════════════════════════════════════════════════════════╝

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from factor_analyzer import FactorAnalyzer
from factor_analyzer.factor_analyzer import calculate_bartlett_sphericity, calculate_kmo
import warnings
warnings.filterwarnings('ignore')

# Configuración visual
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

print("""
╔═══════════════════════════════════════════════════════════════════════════════╗
║ 📚 CONCEPTOS FUNDAMENTALES DEL ANÁLISIS FACTORIAL                              ║
╚═══════════════════════════════════════════════════════════════════════════════╝

🎯 ¿QUÉ ES UN FACTOR?
Un factor es una variable NO OBSERVABLE (latente) que explica la correlación entre 
varias variables observables.

📊 EJEMPLO SIMPLE:
Si un estudiante es bueno en:
- Álgebra
- Geometría  
- Cálculo
- Estadística

Probablemente todas están influenciadas por un FACTOR común: "Habilidad Matemática"

🔍 ¿PARA QUÉ SIRVE EL EFA?
1. REDUCIR complejidad: De 100 variables a 5-10 factores
2. DESCUBRIR estructuras ocultas en los datos
3. ELIMINAR redundancia (variables que miden lo mismo)
4. PREPARAR datos para otros análisis (LCA, clustering, etc.)
""")

# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║ PARTE 1: CARGA Y EXPLORACIÓN INICIAL DE DATOS                              ║
# ╚═══════════════════════════════════════════════════════════════════════════╝

def cargar_y_explorar_datos(ruta_archivo):
    """
    Carga el dataset PISA 2022 y realiza exploración inicial
    """
    print("\n" + "="*80)
    print("PASO 1: CARGANDO Y EXPLORANDO TUS DATOS PISA 2022")
    print("="*80)
    
    # Cargar datos
    df = pd.read_csv(ruta_archivo)
    print(f"\n📊 Dataset cargado: {df.shape[0]:,} estudiantes × {df.shape[1]:,} variables")
    
    # Mostrar primeras columnas
    print("\n📋 Primeras 20 variables en tu dataset:")
    for i, col in enumerate(df.columns[:20], 1):
        print(f"   {i:2d}. {col}")
    
    # Tipos de datos
    print(f"\n📈 Tipos de variables:")
    print(df.dtypes.value_counts())
    
    return df

# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║ PARTE 2: SELECCIÓN DE VARIABLES PARA EFA                                  ║
# ╚═══════════════════════════════════════════════════════════════════════════╝

def seleccionar_variables_para_efa(df):
    """
    Selección inteligente de variables para el análisis factorial
    """
    print("\n" + "="*80)
    print("PASO 2: SELECCIÓN DE VARIABLES PARA EFA")
    print("="*80)
    
    print("""
    🎯 CRITERIOS PARA SELECCIONAR VARIABLES:
    
    1. TIPO DE VARIABLE:
       ✅ Variables numéricas continuas o ordinales (escalas Likert)
       ❌ Variables categóricas nominales (país, género)
       ❌ Variables de identificación (ID estudiante)
    
    2. CONCEPTUALMENTE RELACIONADAS:
       ✅ Variables que midan aspectos similares
       Ejemplos en PISA:
       - Items de una misma escala (ej: ST034Q01-Q06 sobre ansiedad matemática)
       - Preguntas sobre actitudes hacia la escuela
       - Items sobre recursos en casa
    
    3. VARIABILIDAD:
       ✅ Variables con suficiente variación
       ❌ Variables con poca variación (casi todos responden igual)
    """)
    
    # Identificar tipos de variables en PISA
    variables_pisa = {
        'cognitivas': [],      # PV1MATH, PV1READ, PV1SCIE
        'actitudinales': [],   # ST (Student questionnaire)
        'contextuales': [],    # ESCS, recursos en casa
        'escolares': []        # SC (School questionnaire)
    }
    
    # Buscar patrones típicos de PISA
    for col in df.columns:
        if col.startswith('PV') and any(x in col for x in ['MATH', 'READ', 'SCIE']):
            variables_pisa['cognitivas'].append(col)
        elif col.startswith('ST') and df[col].dtype in ['float64', 'int64']:
            variables_pisa['actitudinales'].append(col)
        elif col in ['ESCS', 'WEALTH', 'CULTPOSS', 'HEDRES']:
            variables_pisa['contextuales'].append(col)
        elif col.startswith('SC') and df[col].dtype in ['float64', 'int64']:
            variables_pisa['escolares'].append(col)
    
    print("\n📊 Variables identificadas en tu dataset PISA:")
    for tipo, vars in variables_pisa.items():
        if vars:
            print(f"\n{tipo.upper()} ({len(vars)} variables):")
            print(f"   Ejemplos: {', '.join(vars[:5])}")
    
    return variables_pisa

# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║ PARTE 3: EJEMPLO PRÁCTICO - ANÁLISIS DE ACTITUDES MATEMÁTICAS              ║
# ╚═══════════════════════════════════════════════════════════════════════════╝

def ejemplo_efa_actitudes_matematicas(df):
    """
    Ejemplo completo de EFA con variables de actitudes hacia las matemáticas
    """
    print("\n" + "="*80)
    print("EJEMPLO PRÁCTICO: EFA DE ACTITUDES HACIA LAS MATEMÁTICAS")
    print("="*80)
    
    # Seleccionar variables típicas de actitudes (ejemplo)
    # Estas son variables comunes en PISA sobre actitudes matemáticas
    variables_actitudes = [
        'ST034Q01TA',  # Me preocupo por obtener malas notas en matemáticas
        'ST034Q02TA',  # Me pongo nervioso al resolver problemas de matemáticas
        'ST034Q03TA',  # Me siento indefenso al hacer matemáticas
        'ST034Q04TA',  # Me preocupa que las clases de matemáticas sean difíciles
        'ST034Q05TA',  # Me pongo tenso cuando tengo tarea de matemáticas
        'ST034Q06TA',  # Me siento nervioso al pensar en matemáticas
    ]
    
    # Verificar cuáles existen en el dataset
    variables_disponibles = [v for v in variables_actitudes if v in df.columns]
    
    if len(variables_disponibles) < 3:
        print("\n⚠️ No se encontraron suficientes variables de actitudes.")
        print("Buscando alternativas...")
        
        # Buscar cualquier variable ST que sea numérica
        variables_st = [col for col in df.columns 
                       if col.startswith('ST') and df[col].dtype in ['float64', 'int64']]
        
        if len(variables_st) >= 6:
            variables_disponibles = variables_st[:10]  # Tomar las primeras 10
            print(f"✅ Usando {len(variables_disponibles)} variables ST alternativas")
        else:
            # Usar variables numéricas disponibles
            numericas = df.select_dtypes(include=[np.number]).columns
            variables_disponibles = list(numericas[:10])
            print(f"✅ Usando {len(variables_disponibles)} variables numéricas disponibles")
    
    # Crear subset de datos
    datos_efa = df[variables_disponibles].dropna()
    
    print(f"\n📊 Dataset para EFA:")
    print(f"   • Variables seleccionadas: {len(variables_disponibles)}")
    print(f"   • Estudiantes con datos completos: {len(datos_efa):,}")
    print(f"   • Variables: {', '.join(variables_disponibles[:5])}...")
    
    return datos_efa, variables_disponibles

# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║ PARTE 4: VERIFICACIÓN DE SUPUESTOS PARA EFA                               ║
# ╚═══════════════════════════════════════════════════════════════════════════╝

def verificar_supuestos_efa(datos_efa):
    """
    Verifica si los datos son apropiados para EFA
    """
    print("\n" + "="*80)
    print("PASO 3: VERIFICACIÓN DE SUPUESTOS PARA EFA")
    print("="*80)
    
    print("""
    📐 SUPUESTOS PRINCIPALES DEL EFA:
    
    1️⃣ TAMAÑO DE MUESTRA ADECUADO
       • Mínimo absoluto: 100 observaciones
       • Recomendado: 5-10 observaciones por variable
       • Ideal: >300 observaciones
    
    2️⃣ CORRELACIONES ENTRE VARIABLES
       • Las variables deben estar correlacionadas
       • Si no hay correlación, no hay factores comunes
    
    3️⃣ PRUEBA KMO (Kaiser-Meyer-Olkin)
       • Mide qué tan apropiados son los datos para EFA
       • Valores:
         - KMO < 0.5: Inaceptable ❌
         - 0.5 ≤ KMO < 0.6: Pobre ⚠️
         - 0.6 ≤ KMO < 0.7: Mediocre 😐
         - 0.7 ≤ KMO < 0.8: Aceptable ✓
         - 0.8 ≤ KMO < 0.9: Bueno ✅
         - KMO ≥ 0.9: Excelente 🌟
    
    4️⃣ PRUEBA DE ESFERICIDAD DE BARTLETT
       • H₀: La matriz de correlación es una matriz identidad
       • Si p < 0.05: Rechazamos H₀ → ✅ Hay correlaciones significativas
    """)
    
    # 1. Verificar tamaño de muestra
    n_obs = len(datos_efa)
    n_vars = datos_efa.shape[1]
    ratio = n_obs / n_vars
    
    print(f"\n1️⃣ TAMAÑO DE MUESTRA:")
    print(f"   • Observaciones: {n_obs:,}")
    print(f"   • Variables: {n_vars}")
    print(f"   • Ratio obs/var: {ratio:.1f}")
    
    if ratio >= 10:
        print(f"   ✅ Excelente! Ratio = {ratio:.1f} (>10)")
    elif ratio >= 5:
        print(f"   ✓ Bueno. Ratio = {ratio:.1f} (5-10)")
    else:
        print(f"   ⚠️ Bajo. Ratio = {ratio:.1f} (<5)")
    
    # 2. Matriz de correlación
    corr_matrix = datos_efa.corr()
    
    print(f"\n2️⃣ ANÁLISIS DE CORRELACIONES:")
    corr_values = corr_matrix.values[np.triu_indices_from(corr_matrix.values, k=1)]
    print(f"   • Correlación media: {np.mean(np.abs(corr_values)):.3f}")
    print(f"   • Correlación máxima: {np.max(np.abs(corr_values)):.3f}")
    print(f"   • Correlación mínima: {np.min(np.abs(corr_values)):.3f}")
    
    # Visualizar matriz de correlación
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0,
                square=True, linewidths=1, cbar_kws={"shrink": 0.8})
    plt.title('Matriz de Correlación entre Variables', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig('/mnt/user-data/outputs/matriz_correlacion.png', dpi=150, bbox_inches='tight')
    plt.show()
    
    # 3. Prueba KMO
    try:
        kmo_all, kmo_model = calculate_kmo(datos_efa)
        print(f"\n3️⃣ PRUEBA KMO (Kaiser-Meyer-Olkin):")
        print(f"   • KMO Global: {kmo_model:.3f}")
        
        if kmo_model >= 0.9:
            print(f"   🌟 EXCELENTE para EFA!")
        elif kmo_model >= 0.8:
            print(f"   ✅ MUY BUENO para EFA")
        elif kmo_model >= 0.7:
            print(f"   ✓ ACEPTABLE para EFA")
        elif kmo_model >= 0.6:
            print(f"   😐 MEDIOCRE - Proceder con cautela")
        else:
            print(f"   ❌ NO RECOMENDADO para EFA")
        
        # KMO por variable
        print("\n   KMO por variable:")
        for i, var in enumerate(datos_efa.columns):
            print(f"      • {var}: {kmo_all[i]:.3f}")
    except:
        print("\n   ⚠️ No se pudo calcular KMO (posible problema de datos)")
    
    # 4. Prueba de Bartlett
    try:
        chi_square, p_value = calculate_bartlett_sphericity(datos_efa)
        print(f"\n4️⃣ PRUEBA DE ESFERICIDAD DE BARTLETT:")
        print(f"   • Chi-cuadrado: {chi_square:.2f}")
        print(f"   • p-valor: {p_value:.2e}")
        
        if p_value < 0.001:
            print(f"   ✅ p < 0.001 → Las correlaciones son significativas")
            print(f"   → Los datos son APROPIADOS para EFA")
        else:
            print(f"   ❌ p ≥ 0.05 → No hay correlaciones significativas")
            print(f"   → Los datos NO son apropiados para EFA")
    except:
        print("\n   ⚠️ No se pudo calcular la prueba de Bartlett")
    
    return corr_matrix

# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║ PARTE 5: DETERMINACIÓN DEL NÚMERO DE FACTORES                              ║
# ╚═══════════════════════════════════════════════════════════════════════════╝

def determinar_numero_factores(datos_efa):
    """
    Determina el número óptimo de factores usando múltiples criterios
    """
    print("\n" + "="*80)
    print("PASO 4: DETERMINACIÓN DEL NÚMERO ÓPTIMO DE FACTORES")
    print("="*80)
    
    print("""
    🎯 MÉTODOS PARA DETERMINAR EL NÚMERO DE FACTORES:
    
    1️⃣ CRITERIO DE KAISER (Eigenvalores > 1)
       • Un factor debe explicar al menos tanta varianza como una variable original
       • Si eigenvalor > 1 → El factor es importante
    
    2️⃣ SCREE PLOT (Gráfico de sedimentación)
       • Buscar el "codo" donde la curva se aplana
       • Los factores antes del codo son importantes
    
    3️⃣ VARIANZA EXPLICADA ACUMULADA
       • Retener factores hasta alcanzar 60-70% de varianza
       • En ciencias sociales, 50-60% puede ser aceptable
    
    4️⃣ ANÁLISIS PARALELO (Más robusto)
       • Compara eigenvalores con datos aleatorios
       • Si eigenvalor real > aleatorio → Retener factor
    """)
    
    # Crear objeto FactorAnalyzer para exploración
    fa = FactorAnalyzer(n_factors=min(len(datos_efa.columns), 10), rotation=None)
    fa.fit(datos_efa)
    
    # Obtener eigenvalores
    eigenvalores = fa.get_eigenvalues()[0]
    
    # 1. Criterio de Kaiser
    n_kaiser = sum(eigenvalores > 1)
    print(f"\n1️⃣ CRITERIO DE KAISER:")
    print(f"   Eigenvalores:")
    for i, eigen in enumerate(eigenvalores[:10], 1):
        simbolo = "✅" if eigen > 1 else "❌"
        print(f"   Factor {i}: {eigen:.3f} {simbolo}")
    print(f"\n   → Número de factores según Kaiser: {n_kaiser}")
    
    # 2. Scree Plot
    plt.figure(figsize=(12, 5))
    
    plt.subplot(1, 2, 1)
    plt.plot(range(1, len(eigenvalores)+1), eigenvalores, 'bo-', linewidth=2)
    plt.axhline(y=1, color='r', linestyle='--', label='Eigenvalor = 1')
    plt.xlabel('Número de Factor', fontsize=12)
    plt.ylabel('Eigenvalor', fontsize=12)
    plt.title('Scree Plot - Gráfico de Sedimentación', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    # Marcar el codo
    if len(eigenvalores) > 2:
        diferencias = np.diff(eigenvalores)
        codo = np.argmax(diferencias[:-1] - diferencias[1:]) + 2
        plt.axvline(x=codo, color='g', linestyle=':', label=f'Posible codo (Factor {codo})')
        plt.legend()
    
    # 3. Varianza explicada
    varianza_explicada = eigenvalores / sum(eigenvalores) * 100
    varianza_acumulada = np.cumsum(varianza_explicada)
    
    plt.subplot(1, 2, 2)
    x = range(1, min(11, len(eigenvalores)+1))
    plt.bar(x, varianza_explicada[:10], alpha=0.6, label='Varianza Individual')
    plt.plot(x, varianza_acumulada[:10], 'ro-', linewidth=2, label='Varianza Acumulada')
    plt.axhline(y=60, color='g', linestyle='--', alpha=0.7, label='60% varianza')
    plt.xlabel('Número de Factor', fontsize=12)
    plt.ylabel('Varianza Explicada (%)', fontsize=12)
    plt.title('Varianza Explicada por Factor', fontsize=14, fontweight='bold')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('/mnt/user-data/outputs/determinacion_factores.png', dpi=150, bbox_inches='tight')
    plt.show()
    
    # Encontrar número de factores para 60% varianza
    n_var60 = np.argmax(varianza_acumulada >= 60) + 1
    
    print(f"\n3️⃣ VARIANZA EXPLICADA:")
    for i in range(min(10, len(eigenvalores))):
        print(f"   Factor {i+1}: {varianza_explicada[i]:.1f}% (Acum: {varianza_acumulada[i]:.1f}%)")
    print(f"\n   → Factores para 60% varianza: {n_var60}")
    
    # Recomendación final
    print(f"\n" + "="*50)
    print(f"📊 RECOMENDACIÓN FINAL:")
    print(f"   • Criterio Kaiser sugiere: {n_kaiser} factores")
    print(f"   • Para 60% varianza: {n_var60} factores")
    
    n_factores_optimo = min(n_kaiser, n_var60)
    print(f"\n   ✅ NÚMERO RECOMENDADO: {n_factores_optimo} factores")
    
    return n_factores_optimo, eigenvalores, varianza_acumulada

# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║ PARTE 6: EXTRACCIÓN Y ROTACIÓN DE FACTORES                                ║
# ╚═══════════════════════════════════════════════════════════════════════════╝

def extraer_y_rotar_factores(datos_efa, n_factores):
    """
    Realiza la extracción de factores con rotación Varimax
    """
    print("\n" + "="*80)
    print("PASO 5: EXTRACCIÓN Y ROTACIÓN DE FACTORES")
    print("="*80)
    
    print("""
    🔄 ROTACIÓN DE FACTORES - ¿Por qué rotar?
    
    PROBLEMA: Los factores iniciales son difíciles de interpretar
    SOLUCIÓN: La rotación redistribuye la varianza para hacer los factores más claros
    
    TIPOS DE ROTACIÓN:
    • VARIMAX (Ortogonal): Factores independientes entre sí
      → Maximiza la varianza de las cargas al cuadrado
      → Más fácil de interpretar
      → Cada variable carga alto en UN factor
    
    • PROMAX (Oblicua): Permite correlación entre factores
      → Más realista en ciencias sociales
      → Factores pueden estar relacionados
    
    📊 CARGAS FACTORIALES:
    • Correlación entre variable y factor
    • Rango: -1 a +1
    • Interpretación:
      - |carga| ≥ 0.7: Excelente
      - |carga| ≥ 0.5: Buena
      - |carga| ≥ 0.4: Aceptable
      - |carga| < 0.4: Débil
    """)
    
    # Realizar análisis factorial con rotación Varimax
    fa = FactorAnalyzer(n_factors=n_factores, rotation='varimax', method='minres')
    fa.fit(datos_efa)
    
    # Obtener cargas factoriales
    cargas = pd.DataFrame(
        fa.loadings_,
        index=datos_efa.columns,
        columns=[f'Factor_{i+1}' for i in range(n_factores)]
    )
    
    print(f"\n📊 CARGAS FACTORIALES (Rotación Varimax):")
    print("="*60)
    
    # Mostrar cargas con formato condicional
    for var in cargas.index:
        print(f"\n{var}:")
        for factor in cargas.columns:
            carga = cargas.loc[var, factor]
            if abs(carga) >= 0.5:
                print(f"   {factor}: {carga:+.3f} ✅")
            elif abs(carga) >= 0.4:
                print(f"   {factor}: {carga:+.3f} ✓")
            else:
                print(f"   {factor}: {carga:+.3f}")
    
    # Visualizar matriz de cargas
    plt.figure(figsize=(10, 8))
    sns.heatmap(cargas, annot=True, cmap='RdBu_r', center=0,
                vmin=-1, vmax=1, square=True, linewidths=1,
                cbar_kws={"shrink": 0.8, "label": "Carga Factorial"})
    plt.title('Matriz de Cargas Factoriales (Rotación Varimax)', 
              fontsize=14, fontweight='bold')
    plt.xlabel('Factores', fontsize=12)
    plt.ylabel('Variables', fontsize=12)
    plt.tight_layout()
    plt.savefig('/mnt/user-data/outputs/cargas_factoriales.png', dpi=150, bbox_inches='tight')
    plt.show()
    
    # Comunalidades
    comunalidades = pd.DataFrame({
        'Variable': datos_efa.columns,
        'Comunalidad': fa.get_communalities()
    }).sort_values('Comunalidad', ascending=False)
    
    print(f"\n📊 COMUNALIDADES (Varianza explicada por variable):")
    print("="*60)
    for _, row in comunalidades.iterrows():
        porcentaje = row['Comunalidad'] * 100
        if porcentaje >= 50:
            simbolo = "✅"
        elif porcentaje >= 30:
            simbolo = "✓"
        else:
            simbolo = "⚠️"
        print(f"   {row['Variable']}: {porcentaje:.1f}% {simbolo}")
    
    # Varianza explicada por factor
    varianza_factor = fa.get_factor_variance()
    df_varianza = pd.DataFrame({
        'Factor': [f'Factor_{i+1}' for i in range(n_factores)],
        'Varianza': varianza_factor[0],
        'Proporción': varianza_factor[1],
        'Acumulada': varianza_factor[2]
    })
    
    print(f"\n📊 VARIANZA EXPLICADA POR FACTOR:")
    print("="*60)
    for _, row in df_varianza.iterrows():
        print(f"   {row['Factor']}: {row['Proporción']*100:.1f}% (Acum: {row['Acumulada']*100:.1f}%)")
    
    return fa, cargas, comunalidades

# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║ PARTE 7: INTERPRETACIÓN Y NOMBRADO DE FACTORES                            ║
# ╚═══════════════════════════════════════════════════════════════════════════╝

def interpretar_factores(cargas, umbral=0.4):
    """
    Ayuda a interpretar y nombrar los factores
    """
    print("\n" + "="*80)
    print("PASO 6: INTERPRETACIÓN Y NOMBRADO DE FACTORES")
    print("="*80)
    
    print("""
    🎯 CÓMO INTERPRETAR LOS FACTORES:
    
    1. Identificar variables con cargas altas (≥0.4) en cada factor
    2. Buscar el tema común entre esas variables
    3. Asignar un nombre descriptivo al factor
    
    EJEMPLO:
    Si Factor_1 tiene cargas altas en:
    - "Me preocupo por las matemáticas" (0.75)
    - "Me pongo nervioso con matemáticas" (0.82)
    - "Las matemáticas me estresan" (0.69)
    → Nombre sugerido: "ANSIEDAD MATEMÁTICA"
    """)
    
    interpretaciones = {}
    
    for factor in cargas.columns:
        print(f"\n{'='*60}")
        print(f"📊 {factor.upper()}")
        print(f"{'='*60}")
        
        # Variables con cargas significativas
        cargas_factor = cargas[factor].abs().sort_values(ascending=False)
        variables_importantes = cargas_factor[cargas_factor >= umbral]
        
        if len(variables_importantes) > 0:
            print(f"\nVariables con cargas ≥ {umbral}:")
            for var, carga_abs in variables_importantes.items():
                carga_real = cargas.loc[var, factor]
                direccion = "+" if carga_real > 0 else "-"
                print(f"   {direccion} {var}: {abs(carga_real):.3f}")
            
            # Análisis de patrones
            print(f"\n🔍 ANÁLISIS DEL PATRÓN:")
            
            # Sugerencias basadas en nombres de variables PISA
            sugerencias = []
            vars_str = ' '.join(variables_importantes.index).upper()
            
            if 'MATH' in vars_str:
                sugerencias.append("Relacionado con MATEMÁTICAS")
            if 'READ' in vars_str:
                sugerencias.append("Relacionado con LECTURA")
            if 'SCIE' in vars_str:
                sugerencias.append("Relacionado con CIENCIAS")
            if 'ST034' in vars_str or 'ANXMAT' in vars_str:
                sugerencias.append("Posible ANSIEDAD MATEMÁTICA")
            if 'ESCS' in vars_str or 'WEALTH' in vars_str:
                sugerencias.append("Posible ESTATUS SOCIOECONÓMICO")
            if 'MOTIV' in vars_str or 'INTMAT' in vars_str:
                sugerencias.append("Posible MOTIVACIÓN")
            if 'BELONG' in vars_str:
                sugerencias.append("Posible SENTIDO DE PERTENENCIA")
            
            if sugerencias:
                print("   Temas detectados:")
                for sug in sugerencias:
                    print(f"      • {sug}")
            
            # Solicitar nombre al usuario (simulado)
            print(f"\n💡 SUGERENCIA DE NOMBRE:")
            if 'ANSIEDAD' in ' '.join(sugerencias):
                nombre_sugerido = "Ansiedad Matemática"
            elif 'SOCIOECONÓMICO' in ' '.join(sugerencias):
                nombre_sugerido = "Estatus Socioeconómico"
            elif 'MOTIVACIÓN' in ' '.join(sugerencias):
                nombre_sugerido = "Motivación Académica"
            else:
                nombre_sugerido = f"Factor_{factor.split('_')[1]}_Latente"
            
            print(f"   → {nombre_sugerido}")
            interpretaciones[factor] = nombre_sugerido
        else:
            print(f"   ⚠️ No hay variables con cargas ≥ {umbral}")
            interpretaciones[factor] = f"Factor_{factor.split('_')[1]}_NoInterpretable"
    
    return interpretaciones

# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║ PARTE 8: CÁLCULO DE PUNTUACIONES FACTORIALES                              ║
# ╚═══════════════════════════════════════════════════════════════════════════╝

def calcular_puntuaciones_factoriales(datos_efa, fa, interpretaciones):
    """
    Calcula las puntuaciones factoriales para cada estudiante
    """
    print("\n" + "="*80)
    print("PASO 7: CÁLCULO DE PUNTUACIONES FACTORIALES")
    print("="*80)
    
    print("""
    📊 PUNTUACIONES FACTORIALES:
    
    • Cada estudiante obtiene una puntuación en cada factor
    • Representa qué tan alto/bajo está el estudiante en ese factor latente
    • Puntuaciones estandarizadas (media=0, desv=1)
    
    INTERPRETACIÓN:
    • Puntuación > 0: Por encima del promedio en ese factor
    • Puntuación < 0: Por debajo del promedio en ese factor
    • |Puntuación| > 2: Valor extremo (muy alto o muy bajo)
    
    USO POSTERIOR:
    • Estas puntuaciones se pueden usar para:
      - Análisis de Clases Latentes (LCA)
      - Clustering
      - Regresiones
      - Análisis predictivos
    """)
    
    # Calcular puntuaciones
    puntuaciones = fa.transform(datos_efa)
    
    # Crear DataFrame con puntuaciones
    columnas_puntuaciones = []
    for i, (factor_orig, nombre) in enumerate(interpretaciones.items()):
        nombre_limpio = nombre.replace(' ', '_').replace('-', '_')
        columnas_puntuaciones.append(f"Score_{nombre_limpio}")
    
    df_puntuaciones = pd.DataFrame(
        puntuaciones,
        columns=columnas_puntuaciones,
        index=datos_efa.index
    )
    
    # Estadísticas descriptivas
    print(f"\n📈 ESTADÍSTICAS DE LAS PUNTUACIONES:")
    print("="*60)
    for col in df_puntuaciones.columns:
        stats = df_puntuaciones[col].describe()
        print(f"\n{col}:")
        print(f"   Media: {stats['mean']:.3f}")
        print(f"   Desv. Est.: {stats['std']:.3f}")
        print(f"   Mín: {stats['min']:.3f}")
        print(f"   Q1: {stats['25%']:.3f}")
        print(f"   Mediana: {stats['50%']:.3f}")
        print(f"   Q3: {stats['75%']:.3f}")
        print(f"   Máx: {stats['max']:.3f}")
    
    # Visualizar distribuciones
    n_factores = len(df_puntuaciones.columns)
    fig, axes = plt.subplots(1, min(n_factores, 4), figsize=(15, 4))
    
    if n_factores == 1:
        axes = [axes]
    
    for i, col in enumerate(df_puntuaciones.columns[:4]):
        ax = axes[i] if n_factores > 1 else axes[0]
        df_puntuaciones[col].hist(bins=30, ax=ax, edgecolor='black', alpha=0.7)
        ax.axvline(x=0, color='r', linestyle='--', alpha=0.5)
        ax.set_title(col.replace('Score_', ''), fontsize=10)
        ax.set_xlabel('Puntuación', fontsize=9)
        ax.set_ylabel('Frecuencia', fontsize=9)
        ax.grid(True, alpha=0.3)
    
    plt.suptitle('Distribución de Puntuaciones Factoriales', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig('/mnt/user-data/outputs/distribucion_puntuaciones.png', dpi=150, bbox_inches='tight')
    plt.show()
    
    return df_puntuaciones

# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║ PARTE 9: PREPARACIÓN PARA ANÁLISIS POSTERIORES (LCA, IRT)                 ║
# ╚═══════════════════════════════════════════════════════════════════════════╝

def preparar_para_analisis_posteriores(df_original, df_puntuaciones, cargas, comunalidades):
    """
    Prepara los datos para LCA e IRT
    """
    print("\n" + "="*80)
    print("PASO 8: PREPARACIÓN PARA ANÁLISIS POSTERIORES")
    print("="*80)
    
    print("""
    🎯 OPCIONES PARA ANÁLISIS POSTERIORES:
    
    1️⃣ ANÁLISIS DE CLASES LATENTES (LCA):
       • Opción A: Usar puntuaciones factoriales (RECOMENDADO)
         → Reduce dimensionalidad
         → Elimina colinealidad
         → Captura estructura latente
       
       • Opción B: Usar variables con alta comunalidad
         → Variables bien explicadas por los factores
         → Mantiene interpretabilidad original
    
    2️⃣ TEORÍA DE RESPUESTA AL ÍTEM (IRT):
       • Usar ítems originales agrupados por factor
       • Verificar unidimensionalidad por escala
       • Cada factor puede analizarse por separado
    """)
    
    # 1. Preparación para LCA
    print(f"\n📊 PREPARACIÓN PARA LCA:")
    print("="*60)
    
    # Opción 1: Puntuaciones factoriales
    print(f"\n✅ Opción 1 - Puntuaciones Factoriales:")
    print(f"   • Variables disponibles: {list(df_puntuaciones.columns)}")
    print(f"   • Ventaja: Máxima reducción de dimensionalidad")
    print(f"   • Desventaja: Pérdida de interpretabilidad directa")
    
    # Opción 2: Variables con alta comunalidad
    variables_alta_comunalidad = comunalidades[comunalidades['Comunalidad'] > 0.5]['Variable'].tolist()
    print(f"\n✅ Opción 2 - Variables con Alta Comunalidad (>0.5):")
    print(f"   • Número de variables: {len(variables_alta_comunalidad)}")
    if variables_alta_comunalidad:
        print(f"   • Variables: {', '.join(variables_alta_comunalidad[:5])}...")
    
    # Opción 3: Variables representativas por factor
    variables_representativas = []
    for factor in cargas.columns:
        # Variable con mayor carga en cada factor
        var_max = cargas[factor].abs().idxmax()
        if abs(cargas.loc[var_max, factor]) > 0.5:
            variables_representativas.append(var_max)
    
    print(f"\n✅ Opción 3 - Variables Representativas por Factor:")
    print(f"   • Una variable por factor")
    print(f"   • Variables: {variables_representativas}")
    
    # 2. Preparación para IRT
    print(f"\n📊 PREPARACIÓN PARA IRT:")
    print("="*60)
    
    # Agrupar ítems por factor dominante
    items_por_factor = {}
    for var in cargas.index:
        factor_dominante = cargas.loc[var].abs().idxmax()
        if factor_dominante not in items_por_factor:
            items_por_factor[factor_dominante] = []
        items_por_factor[factor_dominante].append(var)
    
    print(f"\nÍtems agrupados por factor dominante:")
    for factor, items in items_por_factor.items():
        print(f"\n   {factor}:")
        print(f"      • Número de ítems: {len(items)}")
        print(f"      • Ítems: {', '.join(items[:3])}...")
    
    # Crear datasets de salida
    # Dataset con puntuaciones factoriales añadidas
    df_con_factores = df_original.copy()
    for col in df_puntuaciones.columns:
        df_con_factores[col] = np.nan
        df_con_factores.loc[df_puntuaciones.index, col] = df_puntuaciones[col]
    
    # Guardar resultados
    print(f"\n💾 GUARDANDO RESULTADOS:")
    print("="*60)
    
    # 1. Dataset con factores
    df_con_factores.to_csv('/mnt/user-data/outputs/dataset_con_factores.csv', index=False)
    print(f"   ✅ dataset_con_factores.csv guardado")
    
    # 2. Cargas factoriales
    cargas.to_csv('/mnt/user-data/outputs/cargas_factoriales.csv')
    print(f"   ✅ cargas_factoriales.csv guardado")
    
    # 3. Comunalidades
    comunalidades.to_csv('/mnt/user-data/outputs/comunalidades.csv', index=False)
    print(f"   ✅ comunalidades.csv guardado")
    
    # 4. Variables para LCA
    with open('/mnt/user-data/outputs/variables_lca.txt', 'w') as f:
        f.write("OPCIONES PARA LCA:\n")
        f.write("==================\n\n")
        f.write("Opción 1 - Puntuaciones Factoriales:\n")
        for col in df_puntuaciones.columns:
            f.write(f"  - {col}\n")
        f.write("\nOpción 2 - Variables Alta Comunalidad:\n")
        for var in variables_alta_comunalidad:
            f.write(f"  - {var}\n")
        f.write("\nOpción 3 - Variables Representativas:\n")
        for var in variables_representativas:
            f.write(f"  - {var}\n")
    print(f"   ✅ variables_lca.txt guardado")
    
    # 5. Metadata
    metadata = {
        'fecha_analisis': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S'),
        'n_observaciones': len(df_puntuaciones),
        'n_variables_originales': cargas.shape[0],
        'n_factores_extraidos': cargas.shape[1],
        'varianza_total_explicada': float(df_puntuaciones.var().sum()),
        'metodo_extraccion': 'minres',
        'rotacion': 'varimax',
        'variables_alta_comunalidad': variables_alta_comunalidad,
        'variables_representativas': variables_representativas,
        'items_por_factor': {k: v for k, v in items_por_factor.items()}
    }
    
    import json
    with open('/mnt/user-data/outputs/metadata_efa.json', 'w') as f:
        json.dump(metadata, f, indent=2, default=str)
    print(f"   ✅ metadata_efa.json guardado")
    
    return df_con_factores

# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║ PARTE 10: CÓDIGO PLANTILLA PARA LCA                                        ║
# ╚═══════════════════════════════════════════════════════════════════════════╝

def generar_codigo_lca():
    """
    Genera código plantilla para el siguiente análisis LCA
    """
    codigo_lca = '''"""
PLANTILLA DE CÓDIGO PARA ANÁLISIS DE CLASES LATENTES (LCA)
Usando los resultados del EFA
"""

import pandas as pd
import numpy as np
from sklearn.mixture import GaussianMixture
from sklearn.metrics import silhouette_score, davies_bouldin_score
import matplotlib.pyplot as plt
import seaborn as sns

# 1. CARGAR DATOS CON FACTORES
df = pd.read_csv('dataset_con_factores.csv')

# 2. SELECCIONAR VARIABLES PARA LCA
# Opción A: Usar puntuaciones factoriales
variables_lca = [col for col in df.columns if col.startswith('Score_')]

# Opción B: Usar variables originales con alta comunalidad
# variables_lca = ['var1', 'var2', 'var3']  # Reemplazar con tus variables

# 3. PREPARAR DATOS
X = df[variables_lca].dropna()

# 4. DETERMINAR NÚMERO ÓPTIMO DE CLASES
resultados_lca = []
rango_clases = range(2, 8)

for n_clases in rango_clases:
    # Ajustar modelo
    gmm = GaussianMixture(n_components=n_clases, random_state=42)
    gmm.fit(X)
    
    # Predicciones
    labels = gmm.predict(X)
    
    # Métricas
    bic = gmm.bic(X)
    aic = gmm.aic(X)
    silhouette = silhouette_score(X, labels)
    
    resultados_lca.append({
        'n_clases': n_clases,
        'BIC': bic,
        'AIC': aic,
        'Silhouette': silhouette
    })
    
    print(f"Clases: {n_clases} | BIC: {bic:.2f} | AIC: {aic:.2f} | Silhouette: {silhouette:.3f}")

# 5. SELECCIONAR MEJOR MODELO
df_resultados = pd.DataFrame(resultados_lca)
n_optimo = df_resultados.loc[df_resultados['BIC'].idxmin(), 'n_clases']

print(f"\\nNúmero óptimo de clases: {n_optimo}")

# 6. AJUSTAR MODELO FINAL
modelo_final = GaussianMixture(n_components=n_optimo, random_state=42)
modelo_final.fit(X)
df['clase_latente'] = modelo_final.predict(X)

# 7. CARACTERIZAR CLASES
print("\\nCaracterización de clases:")
for clase in range(n_optimo):
    print(f"\\nClase {clase} (n={sum(df['clase_latente']==clase)}):")
    subset = X[df['clase_latente']==clase]
    print(subset.mean())

# 8. VISUALIZACIÓN
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Gráfico de métricas
axes[0].plot(df_resultados['n_clases'], df_resultados['BIC'], 'o-', label='BIC')
axes[0].plot(df_resultados['n_clases'], df_resultados['AIC'], 's-', label='AIC')
axes[0].set_xlabel('Número de Clases')
axes[0].set_ylabel('Criterio de Información')
axes[0].legend()
axes[0].grid(True)

# Distribución de clases
axes[1].bar(range(n_optimo), df['clase_latente'].value_counts().sort_index())
axes[1].set_xlabel('Clase Latente')
axes[1].set_ylabel('Número de Estudiantes')
axes[1].set_title(f'Distribución de {n_optimo} Clases Latentes')

plt.tight_layout()
plt.savefig('resultados_lca.png')
plt.show()

print("\\n✅ Análisis LCA completado!")
print(f"   • Dataset con clases: dataset_con_clases.csv")

# Guardar resultados
df.to_csv('dataset_con_clases.csv', index=False)
'''
    
    with open('/mnt/user-data/outputs/codigo_plantilla_lca.py', 'w') as f:
        f.write(codigo_lca)
    
    print("\n✅ Código plantilla para LCA guardado en: codigo_plantilla_lca.py")

# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║ FUNCIÓN PRINCIPAL - EJECUTAR TODO EL ANÁLISIS                              ║
# ╚═══════════════════════════════════════════════════════════════════════════╝

def ejecutar_analisis_completo(ruta_archivo):
    """
    Ejecuta todo el pipeline de análisis factorial exploratorio
    """
    print("""
    ╔════════════════════════════════════════════════════════════════════╗
    ║   ANÁLISIS FACTORIAL EXPLORATORIO COMPLETO - PISA 2022            ║
    ║   Tutorial Paso a Paso para Principiantes                         ║
    ╚════════════════════════════════════════════════════════════════════╝
    """)
    
    try:
        # Paso 1: Cargar datos
        df = cargar_y_explorar_datos(ruta_archivo)
        
        # Paso 2: Seleccionar variables
        variables_pisa = seleccionar_variables_para_efa(df)
        
        # Paso 3: Ejemplo práctico
        datos_efa, variables_seleccionadas = ejemplo_efa_actitudes_matematicas(df)
        
        # Paso 4: Verificar supuestos
        corr_matrix = verificar_supuestos_efa(datos_efa)
        
        # Paso 5: Determinar número de factores
        n_factores, eigenvalores, varianza_acum = determinar_numero_factores(datos_efa)
        
        # Paso 6: Extraer y rotar factores
        fa, cargas, comunalidades = extraer_y_rotar_factores(datos_efa, n_factores)
        
        # Paso 7: Interpretar factores
        interpretaciones = interpretar_factores(cargas)
        
        # Paso 8: Calcular puntuaciones
        df_puntuaciones = calcular_puntuaciones_factoriales(datos_efa, fa, interpretaciones)
        
        # Paso 9: Preparar para análisis posteriores
        df_final = preparar_para_analisis_posteriores(df, df_puntuaciones, cargas, comunalidades)
        
        # Paso 10: Generar código LCA
        generar_codigo_lca()
        
        print("""
        ╔════════════════════════════════════════════════════════════════════╗
        ║   ✅ ANÁLISIS COMPLETADO CON ÉXITO                                  ║
        ╚════════════════════════════════════════════════════════════════════╝
        
        📁 ARCHIVOS GENERADOS:
        • dataset_con_factores.csv - Dataset original + puntuaciones factoriales
        • cargas_factoriales.csv - Matriz de cargas factoriales
        • comunalidades.csv - Comunalidades de cada variable
        • variables_lca.txt - Variables recomendadas para LCA
        • metadata_efa.json - Metadata del análisis
        • codigo_plantilla_lca.py - Código para siguiente paso (LCA)
        
        📊 VISUALIZACIONES:
        • matriz_correlacion.png
        • determinacion_factores.png
        • cargas_factoriales.png
        • distribucion_puntuaciones.png
        
        🎯 SIGUIENTES PASOS:
        1. Revisar la interpretación de los factores
        2. Validar que los factores tengan sentido conceptual
        3. Ejecutar el código LCA con las puntuaciones factoriales
        4. Considerar análisis IRT si tienes escalas específicas
        
        💡 RECOMENDACIONES:
        • Los factores extraídos capturan la estructura latente de tus datos
        • Usa las puntuaciones factoriales para reducir dimensionalidad
        • Valida los resultados con conocimiento del dominio PISA
        """)
        
        return df_final
        
    except Exception as e:
        print(f"\n❌ Error durante el análisis: {str(e)}")
        print("\n💡 Sugerencias:")
        print("   1. Verifica que el archivo existe y es accesible")
        print("   2. Asegúrate de que el dataset tiene variables numéricas")
        print("   3. Revisa que hay suficientes observaciones sin valores faltantes")
        return None

# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║ EJEMPLO DE USO                                                             ║
# ╚═══════════════════════════════════════════════════════════════════════════╝

if __name__ == "__main__":
    print("""
    ╔════════════════════════════════════════════════════════════════════╗
    ║   INSTRUCCIONES DE USO                                              ║
    ╚════════════════════════════════════════════════════════════════════╗
    
    Para ejecutar este análisis con tu dataset PISA 2022:
    
    1. Asegúrate de tener tu dataset unido en formato CSV
    2. Ejecuta el siguiente código:
    
    >>> from tutorial_efa_pisa2022 import ejecutar_analisis_completo
    >>> df_resultado = ejecutar_analisis_completo('ruta/a/tu/dataset_pisa2022.csv')
    
    El análisis:
    • Te guiará paso a paso por cada concepto
    • Explicará cada decisión tomada
    • Generará visualizaciones explicativas
    • Preparará los datos para LCA e IRT
    • Creará código plantilla para siguientes análisis
    
    📚 RECURSOS ADICIONALES:
    • Factor Analysis in Python: factor-analyzer library
    • Documentación PISA 2022: www.oecd.org/pisa/
    • Teoría EFA: Hair et al. (2014) Multivariate Data Analysis
    
    ¡Buena suerte con tu análisis! 🎯
    """)
