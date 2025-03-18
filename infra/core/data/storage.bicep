param storageAccountName string
param location string = resourceGroup().location
param storageAccountType string = 'Standard_LRS'

resource storageAccount 'Microsoft.Storage/storageAccounts@2022-05-01' = {
  name: storageAccountName
  location: location
  sku: {
    name: storageAccountType
  }
  kind: 'Storage'
  properties: {
    supportsHttpsTrafficOnly: true
    defaultToOAuthAuthentication: true
  }
}

output storageAccountName string = storageAccount.name
output storageAccountUrl string = storageAccount.properties.primaryEndpoints.blob
output storageAccountId string = storageAccount.id
