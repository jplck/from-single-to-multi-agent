param name string
param location string
param tags object = {}
@description('AI hub name')
param aiHubName string

@description('AI hub display name')
param aiHubFriendlyName string = aiHubName

@description('AI hub description')
param aiHubDescription string = 'AI hub for managing AI resources'

@description('Resource ID of the application insights resource for storing diagnostics logs')
param applicationInsightsId string

param storageAccountId string

param kind string = 'OpenAI'
// Public network access of the Azure OpenAI service
param publicNetworkAccess string = 'Enabled'
// SKU of the Azure OpenAI service
param sku object = {
  name: 'S0'
}

param customDomainName string
param deployments array

resource account 'Microsoft.CognitiveServices/accounts@2024-10-01' = {
  name: name  
  location: location
  tags: tags
  kind: kind
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    customSubDomainName: customDomainName
    publicNetworkAccess: publicNetworkAccess
  }
  sku: sku
}

// Deployments for the Azure OpenAI service
@batchSize(1)
resource deployment 'Microsoft.CognitiveServices/accounts/deployments@2024-10-01' = [for deployment in deployments: {
  parent: account
  name: deployment.name
  sku: {
    name: deployment.skuName
    capacity: deployment.capacity
  }
  properties: {
    model: deployment.model
  }
}]

resource aiHub 'Microsoft.MachineLearningServices/workspaces@2023-08-01-preview' = {
  name: aiHubName
  location: location
  tags: tags
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    // organization
    friendlyName: aiHubFriendlyName
    description: aiHubDescription

    // dependent resources
    applicationInsights: applicationInsightsId
    storageAccount: storageAccountId
  }
  kind: 'hub'

  resource aiServicesConnection 'connections@2024-01-01-preview' = {
    name: '${aiHubName}-connection-AzureOpenAI'
    properties: {
      category: 'AzureOpenAI'
      target: account.properties.endpoint
      authType: 'ApiKey'
      isSharedToAll: true
      credentials: {
        key: '${listKeys(account.id, '2021-10-01').key1}'
      }
      metadata: {
        ApiType: 'Azure'
        ResourceId: account.id
      }
    }
  }
}

output aiHubID string = aiHub.id
output openaiEndpoint string = account.properties.endpoint
output openaiKey string = listKeys(account.id, '2022-10-01').key1
output openaiName string = account.name
output location string = account.location
