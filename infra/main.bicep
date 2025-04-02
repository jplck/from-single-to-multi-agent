targetScope = 'subscription'

@minLength(1)
@maxLength(64)
@description('Name of the the environment which is used to generate a short unique hash used in all resources.')
param environmentName string

@minLength(1)
@description('Primary location for all resources')
param location string
@description('Primary location for all AI resources - Might difffer from the primary location')
@allowed(['francecentral', 'swedencentral'])
param aiResourceLocation string
@description('Id of the user or app to assign application roles')
param resourceGroupName string = ''
param containerAppsEnvironmentName string = ''
param containerRegistryName string = ''
param openaiName string = ''
param storageAccountName string = ''
param applicationInsightsName string = ''
param logAnalyticsName string = ''

var abbrs = loadJsonContent('./abbreviations.json')
var resourceToken = toLower(uniqueString(subscription().id, environmentName, location))
var tags = { 'azd-env-name': environmentName, 'app': 'ai-agents', 'tracing': 'yes' }
param searchIndexName string = 'search-index'
param completionDeploymentModelName string = 'gpt-4o'
param completionModelName string = 'gpt-4o'
param completionModelVersion string = '2024-08-06'
param embeddingDeploymentModelName string = 'text-embedding-ada-002'
param embeddingModelName string = 'text-embedding-ada-002'
param embeddingModelVersion string = '2'
param openaiApiVersion string = '2024-08-01-preview'
param openaiCapacity int = 50
param voiceDeploymentModelName string = 'gpt-4o-realtime-preview'
param voiceModelName string = 'gpt-4o-realtime-preview'
param voiceModelVersion string = '2024-12-17'

param modelDeployments array = [
  {
    name: completionDeploymentModelName
    skuName: 'Standard'
    capacity: openaiCapacity
    model: {
      format: 'OpenAI'
      name: completionModelName
      version: completionModelVersion
    }
  }
  {
    name: embeddingDeploymentModelName
    skuName: 'Standard'
    capacity: openaiCapacity
    model: {
      format: 'OpenAI'
      name: embeddingModelName
      version: embeddingModelVersion
    }
  }
  {
    name: voiceDeploymentModelName
    skuName: 'GlobalStandard'
    capacity: 1
    model: {
      format: 'OpenAI'      
      name: voiceModelName
      version: voiceModelVersion
    }
  }
]

// Organize resources in a resource group
resource resourceGroup 'Microsoft.Resources/resourceGroups@2021-04-01' = {
  name: !empty(resourceGroupName) ? resourceGroupName : '${abbrs.resourcesResourceGroups}${environmentName}'
  location: location
  tags: tags
}

/*
module storage './core/data/storage.bicep' = {
  name: 'storage'
  scope: resourceGroup
  params: {
    storageAccountName: !empty(storageAccountName) ? storageAccountName : '${abbrs.storageAccounts}${resourceToken}'
  }
}

// Container apps host (including container registry)
module containerApps './core/host/container-apps.bicep' = {
  name: 'container-apps'
  scope: resourceGroup
  params: {
    name: 'app'
    containerAppsEnvironmentName: !empty(containerAppsEnvironmentName) ? containerAppsEnvironmentName : '${abbrs.appManagedEnvironments}${resourceToken}'
    containerRegistryName: !empty(containerRegistryName) ? containerRegistryName : '${abbrs.containerRegistryRegistries}${resourceToken}'
    location: location
    logAnalyticsWorkspaceName: monitoring.outputs.logAnalyticsWorkspaceName
    applicationInsightsName: monitoring.outputs.applicationInsightsName
    identityName: '${abbrs.managedIdentityUserAssignedIdentities}api-agents'
    openaiName: openai.outputs.openaiName
    searchName: search.outputs.searchName
  }
}

*/

// Azure OpenAI Model
module openai './ai/openai.bicep' = {
  name: 'openai'
  scope: resourceGroup
  params: {
    location: !empty(aiResourceLocation) ? aiResourceLocation : location
    tags: tags
    customDomainName: !empty(openaiName) ? openaiName : '${abbrs.cognitiveServicesAccounts}${resourceToken}'
    name: !empty(openaiName) ? openaiName : '${abbrs.cognitiveServicesAccounts}${resourceToken}'
    deployments: modelDeployments
  }
}

/*

module search './ai/search.bicep' = {
  name: 'search'
  scope: resourceGroup
  params: {
    location: location
    tags: tags
    name: !empty(openaiName) ? openaiName : '${abbrs.searchSearchServices}${resourceToken}'
  }
}

*/

// Monitor application with Azure Monitor
module monitoring './core/monitor/monitoring.bicep' = {
  name: 'monitoring'
  scope: resourceGroup
  params: {
    location: location
    tags: tags
    logAnalyticsName: !empty(logAnalyticsName) ? logAnalyticsName : '${abbrs.operationalInsightsWorkspaces}${resourceToken}'
    applicationInsightsName: !empty(applicationInsightsName) ? applicationInsightsName : '${abbrs.insightsComponents}${resourceToken}'
  }
}

output AZURE_LOCATION string = location
output AZURE_TENANT_ID string = tenant().tenantId
output AZURE_RESOURCE_GROUP string = resourceGroup.name
output AZURE_VOICE_COMPLETION_DEPLOYMENT_NAME string = voiceDeploymentModelName
output AZURE_VOICE_COMPLETION_MODEL string = voiceModelName
output AZURE_VOICE_COMPLETION_MODEL_VERSION string = voiceModelVersion
output AZURE_OPENAI_API_VERSION string = openaiApiVersion
output AZURE_OPENAI_API_KEY string = openai.outputs.openaiKey
output AZURE_OPENAI_ENDPOINT string = openai.outputs.openaiEndpoint
output AZURE_OPENAI_COMPLETION_MODEL string = completionModelName
output AZURE_OPENAI_COMPLETION_DEPLOYMENT_NAME string = completionDeploymentModelName
output AZURE_OPENAI_COMPLETION_MODEL_VERSION string = completionModelVersion
output AZURE_OPENAI_EMBEDDING_MODEL string = embeddingModelName
output AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME string = embeddingDeploymentModelName
output APPLICATIONINSIGHTS_CONNECTION_STRING string = monitoring.outputs.applicationInsightsConnectionString
output APPLICATIONINSIGHTS_NAME string = monitoring.outputs.applicationInsightsName
/*
output AZURE_CONTAINER_ENVIRONMENT_NAME string = containerApps.outputs.environmentName
output AZURE_CONTAINER_REGISTRY_ENDPOINT string = containerApps.outputs.registryLoginServer
output AZURE_CONTAINER_REGISTRY_NAME string = containerApps.outputs.registryName
output AZURE_AI_SEARCH_NAME string = search.outputs.searchName
output AZURE_AI_SEARCH_ENDPOINT string = search.outputs.searchEndpoint
output AZURE_AI_SEARCH_KEY string = search.outputs.searchAdminKey
output AZURE_AI_SEARCH_INDEX string = searchIndexName
output BACKEND_API_URL string = 'http://localhost:8000'
output FRONTEND_SITE_NAME string = 'http://127.0.0.1:3000'
output STORAGE_ACCOUNT_URL string = storage.outputs.storageAccountUrl
*/
