import os #para poder obtener la variable de entorno
from azure.identity import DefaultAzureCredential
from azure.mgmt.datafactory import DataFactoryManagementClient
from azure.mgmt.datafactory.models import LinkedServiceResource, RestServiceLinkedService

# Autenticación para Azure, cogemos la id de la suscripcion de una variable de entorno que ha sido
#previamente creada
subscription_id = os.getenv('ID_AZURE_SUSCRIPTION')
#Comprobamos que exista una variable de entorno con el id de la suscripcion
if not subscription_id:
    raise ValueError("Por favor, establece la variable de entorno ID_AZURE_SUSCRIPTION antes de ejecutar este script.")

#Punto de entrada para realizar operaciones
credential = DefaultAzureCredential()
adf_client = DataFactoryManagementClient(credential, subscription_id)

#Configuracion del servicio rest
resource_group = 'TFGInformatica'
data_factory_name = 'fabricadedatostfg'
rest_service_url = 'https://api.precioil.es/estaciones/conPrecios/localidad/'


#Creacion del servicio rest
rest_service_linked_service = RestServiceLinkedService(
    url=rest_service_url,
    authentication_type='Anonymous' #No hace falta autenticarse
)

ls_name = 'ServicioRestAPIPrecioil'
adf_client.linked_services.create_or_update(
    resource_group_name=resource_group,
    factory_name=data_factory_name,
    linked_service_name=ls_name,
    linked_service=LinkedServiceResource(properties=rest_service_linked_service)
)


#Print para asegurarnos que se ha creado la fabrica
print(f"Linked Service {ls_name} para REST creado.")
