import pandas as pd

# Cargar el archivo CSV, especificando valores nulos adicionales
df = pd.read_csv("C:/Users/scarl/IAthon25_Knigths/src/data/Datasets/Cabala/at-cpt.csv", na_values=["", "--", "NA", "null"])

# Detectar valores nulos en todo el DataFrame
valores_nulos = df.isnull()

# Mostrar las filas que contienen valores nulos
filas_con_nulos = df[valores_nulos.any(axis=1)]

# Mostrar las columnas que contienen valores nulos
columnas_con_nulos = valores_nulos.any(axis=0)

# Imprimir el resumen de las filas y columnas con valores nulos
print("Filas con valores nulos:\n", filas_con_nulos)
print("\nColumnas con valores nulos:", columnas_con_nulos)

# Contar el número total de valores nulos en cada columna
conteo_nulos_por_columna = valores_nulos.sum()
print("\nConteo de valores nulos por columna:\n", conteo_nulos_por_columna)

# Alternativamente, podrías usar .info() para ver directamente el número de valores no nulos
print("\nInformación del DataFrame:")
df.info()
