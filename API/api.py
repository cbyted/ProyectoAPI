import pandas
from sodapy import Socrata
from sys import exit

# Data base identifyer
database = "gt2j-8ykr"
domain = "www.datos.gov.co"

# Connect to the API
def connect_to_api():
    try:
        client = Socrata(domain, None)
        return client
    
    except Exception as e:
        exit()

# fetch request
def consult_data(client, location, registers=10):
    try:    
        results = client.get(database, departamento_nom=location, limit=registers)
        if not results:
            return None

        return results
    
    except Exception as e:
        exit()

# Convert results to pandas DataFrame
def converto_to_dataframe(results):
    try:
        results_df = pandas.DataFrame.from_records(results)
        print(results_df)
        return results_df

    except Exception as e:
        exit()

# parse interesting fields
def parse_results_fields(resutls_df):
    try: 
        new_df = resutls_df[["departamento_nom", "ciudad_municipio_nom", "ubicacion", "edad", "estado", "tipo_recuperacion"]]  
        return new_df
    
    except Exception as e:
        exit()
