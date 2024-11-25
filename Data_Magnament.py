import pandas as pd
import numpy as np
from faker import Faker
import random 

#region Recursos
datos = {
    'A':  [1, np.nan, 3],
    'B': [4, 5, np.nan],
    'C': [np.nan, np.nan, np.nan]
}
df_datos = pd.DataFrame(datos)

# Identificar valores faltantes
print(df_datos.isnull()) # Este método devuelve un DataFrame indicando True donde falta el valor

# Llenar valores faltantes con un valor por defecto 

df_filled = df_datos.fillna(10) # Con fillna se rellenan los huecos de valores faltantes con un valor por defeco que indicamos por parámetro en el método fillna
print(df_filled)

# Eliminar filas donde todos los elementos son NaN

df_dropped = df_datos.dropna(how='all')
print(df_dropped)

# Imputación de datos con métodos
# Imputación por la media
df_media = df_datos['A'].fillna(df_datos['A'].mean()) # Rellena los huecos faltantes de la columna A con el valor por defecto correspondiente a la media de los datos de la colummna A 
print(df_media)
df_mediaB = df_datos['B'].fillna(df_datos['B'].median()) # Rellena los huecos faltantes de la columna B con el valor por defecto correspondiente a la mediana de los datos de la colummna B
print(df_mediaB)

# Estrategia de Limpieza de Datos 

datos2 = {
    'A':  [3, np.nan, 3],
    'B':  [3, np.nan, 3],
    'C':  [3, 5, 3],
}
df_datos2 = pd.DataFrame(datos2)

# Eliminar duplicados
df_filtrado = df_datos2.drop_duplicates()
print(df_filtrado)

# Corregir inconsistencias en los nombres de las categorías 

frutas = {
    'Category': [' Apple', 'Banana ', 'CHERRY', ' orange ']
}

df_frutas = pd.DataFrame(frutas)

preparacion_datos = df_frutas['Category'].str.lower().str.strip() # Guardamos en una variable las correciones de la columna Category del DF; pasando a minúsculas todos los valores, y eliminando espacios tanto al principio como al final de la cadena.
print(preparacion_datos)

# Validar datos utilizando expresiones regulares 

df_emails = pd.DataFrame({
    'Email': ['valid.email@example.com', 'invalid-email', 'another.valid@example.com']
})


df_emails['Email'] = df_emails['Email'].where(df_emails['Email'].str.match(r"[^@]+@[^@]+\.[^@]+"), np.nan) # Con el metodo where, filtra en True aquellos valores de la clave Email que coincidan (gracias al metodo match) con la expresión regular 
# La expresion regular comienza con todos aquellos caracteres excepto @, seguido de @, seguido de nuevo de todos aquellos excepto @, seguido de un punto literal y por ultimo de nuevo seguido de todos aquellos caracteres que no sean @. Si la condición de where
# es false, los valores se rellenaran por NaN
print(df_emails)

#endregion


#region DataSet 

fake = Faker()


# Generar datos ficticios

def generate_data(rows= 1000): # Genera una función donde el parámetro de entrada serán 1000 filas 
    data = [] # Creamos una lista vacía que será el conjunto de datos 
    for _ in range(rows): # Por cada iteración en filas, 
        product_id = random.randint(1, 100) # product_id tendrá un valor aleatorio en el rango [1, 100]
        product_name = fake.word().title() # product_name tendrá un nombre ficticio gracias a faker
        price = round(random.uniform(10, 1000), 2) # El precio será un número en el rango [10, 1000] y con dos decimales máximo 
        sale_date = fake.date_between(start_date='-2y', end_date='today') # la fecha de venta será una fecha ficticia en el rango del día de hoy hasta dos años atrás
        region = random.choice(['Norte', 'Sur', 'Este', 'Oeste']) # la región será una elección aleatoria entre el rango propuesto
        quantity = random.randint(1, 100) # La cantidad de productos será un número aleatorio en el rango [1, 100]

        # Introducir errores e inconsistencias 
        if random.choice([True,False]):
            product_name = product_name.lower() # Aquí introducimos una inconsistencia en la generación aleatoria de los nombres, de manera que habrá algunos con todas las letras en minúsculas, y otros nombres que no. 
        if random.choice([True, False]): 
            sale_date = str(sale_date).replace('-', '/') # Formato incorrecto de fechas 
        if random.choice([True, False]):
            price = 'N/A' # Si price es igual a True, el valor devuelto será faltante
        if random.choice([True, False]): 
            quantity = None # Si quantity es igual a True, el valor devuelto será faltante 
        
        data.append([product_id, product_name, price, sale_date, region, quantity])

    # Duplicar algunas entradas para simular datos duplicados
    duplicates = [random.choice(data) for _ in range(int(rows*0.1))] # Guardamos en una variable, una lista de valores duplicados de la lista data, en este caso, solo un 10% del total de todas las líneas
    data.extend(duplicates) # Aquí añadimos con extend la lista duplicados a la lista data que ya contiene la lista que le añadimos con append. 

    # Creamos un DataFrame con los valores en las filas de la lista data, y con las columnas descritas en la lista columns
    columns = ['Product_ID', 'Product_Name', 'Price', 'Sale_Date', 'Region', 'Quantity'] 
    df_data_Ex = pd.DataFrame(data, columns=columns) 

    # Añadir filas con errores de consistencia en 'Region' en un 5% del total de las filas 
    for _ in range(int(rows*0.05)):
        # Estamos seleccionando una fila en el índice aleatorio generado con random.randint(0, len(df_data_Ex)-1) de la columna 'Region'; y lo estamos asignando a una seleccion aleatoria de una de las cadenas de la lista ['north', 'south ', ' east', 'west']
        df_data_Ex.loc[random.randint(0, len(df_data_Ex)-1), 'Region'] = random.choice(['north', 'south ', ' east', 'west'])

    return df_data_Ex # Nos devuelve el dataFrame 

# generar el dataset 
df_data_Ex = generate_data(1000) # Asignamos al DataFrame toda la función con las 1000 líneas que tiene por parámetro

# Guardar el dataset en un archivo CSV
df_data_Ex.to_csv('sales_data_complex.csv', index=False)

# print("Dataset generado y guardado en 'sales_data_complex.csv")
#endregion 

#region Solución escalable

# Importamos el archivo CSV y lo convertimos en un DataFrame. En este caso no es necesario especificar los separadores ya que cuando se guardó el DataSet no se especificaron. 
df_dataset = pd.read_csv('sales_data_complex.csv') # Al especificarlo aquí, me estaba generando un archivo csv, y no me mostraba el formato DataFrame como yo quería. 
# Análisis exploratorio inicial para familiarizarse con los datos 
print(df_dataset.head())

#Identificación de valores faltantes con el método isnull. Nos devuelve un DataFrame con valores True para valores faltantes y False para valores disponibles
print(df_dataset.isnull()) 

# Hemos detectado que hay valores faltantes en las columnas ['Price'] y ['Quantity']
print(df_dataset['Sale_Date'], df_dataset['Region'], df_dataset['Product_Name'])

# También detectamos que hay errores de consistencia en la columna ['Sale_Date'], df_dataset['Region'] y df_dataset['Product_Name']
# Correción de las columnas ['Price'] & ['Quantity'] con el método Fillna que rellena los huecos con valores faltantes. 
# En el caso del precio hemos rellenado los huecos con valores a partir de la media de los valores disponibles en la propia columna Price, y acotando los decimales en dos cifras.
# En el caso de Quantity hemos hecho la misma operación pero utilizando la mediana, para que escoja el valor central 
df_dataset['Price']= df_dataset['Price'].fillna(round(df_dataset['Price'].mean(), 2))
df_dataset['Quantity']= df_dataset['Quantity'].fillna(df_dataset['Quantity'].median())
print(df_dataset['Price'], df_dataset['Quantity'])

# Correción del formato de fecha en ['Sale_Date']
# Hemos utilizado el método replace para reemplazar todos los formatos strings erróneos por el correcto en la columna ['Sale_Date'].
df_dataset['Sale_Date']= df_dataset['Sale_Date'].str.replace('/', '-')
print(df_dataset['Sale_Date'])

# Correción de la columna ['Region']
# Hemos convertido todos los valores de la columna Region a minúscula y hemos eliminado los espacios tanto al principio como al final de las cadenas de string
df_dataset['Region']= df_dataset['Region'].str.strip().str.lower()
df_dataset['Region']= df_dataset['Region'].replace({'north': 'Norte', 'south': 'Sur', 'east': 'Este', 'west': 'Oeste'}, regex=True) # Hemos declarado un diccionario con claves valor para que sean reemplazadas, y además todas juntas en una única llamada gracias a regex=True
print(df_dataset['Region'])

# Correción de la columna ['Product_Name']
# Eliminación de espacios al principio y final de la cadena de los valores string, y conversión de los carácteres en mayúsculas, a minúsculas
df_dataset['Product_Name']= df_dataset['Product_Name'].str.strip().str.lower()
print(df_dataset['Product_Name'])

# Comprobamos cuantas filas duplicadas existen en el DataFrame
print(f'El DataFrame df_dataset tiene {df_dataset.duplicated().sum()} duplicados') # Nos indica cuantas filas duplicadas se han generado (al utilizar random, la cantidad de duplicados será aleatoria en cada ejecución)

# Eliminación de los datos duplicados del DataSet
df_dataset.drop_duplicates(inplace=True) # En este caso he utiizado el parámetro inplace=True para que la limpieza afecte al DataFrame original 
print(f'El DataFrame df_dataset tiene {df_dataset.duplicated().sum()} duplicados') # Volvemos a comprobar cuantos duplicados hay; siendo esta vez 0, por lo que hemos limpiado de duplicados el DataFrame al completo.

# Comprobación final de valores nulos en el DataFrame 
if df_dataset.isnull().any().any(): # Con esta condición estoy comprobando columna por columna, y fila por fila si hay algún valor nulo en el DataFrame.
    print('Hay valores nulos en el DataFrame.')
else:
    print('No hay valores nulos en el DataFrame.')

# Exportación del DataSet limpio a un nuevo archivo CSV

df_dataset.to_csv('sales_data_complex_clean.csv', index=False)
#endregion

