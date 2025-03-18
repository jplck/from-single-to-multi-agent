param name string
param location string = resourceGroup().location
param identityName string
@description('Specifies the Cron formatted repeating schedule ("* * * * *") of a Cron Job.')
param cronExpression	string = '* * * * *'
@description('Specifies the number of parallel replicas of a Container Apps job that can run at a given time.')
param parallelism	int = 2
@description('Specifies the minimum number of successful replica completions before overall Container Apps job completion.')
param replicaCompletionCount	int = 1
@description('Specifies the maximum number of retries before failing the job.')
param replicaRetryLimit	int = 1
@description('Specifies the maximum number of seconds a Container Apps job replica is allowed to run.')
param replicaTimeout	int = 300
@description('Specifies the Required CPU in cores, e.g. 0.5 for the first Azure Container Apps Job. Specify a decimal value as a string. For example, specify 0.5 for 1/2 core.')
param cpu string = '0.25'
@description('Specifies the Required memory in gigabytes for the second Azure Container Apps Job. E.g. 1.5 Specify a decimal value as a string. For example, specify 1.5 for 1.5 GB.')
param memory string = '0.5Gi'
@description('Specifies a workload profile name to pin for container app execution.')
param workloadProfileName string = ''
param containerName string
param containerImage string
param envVariables array = []

param containerRegistryName string
param containerAppsEnvironmentName string

resource userIdentity 'Microsoft.ManagedIdentity/userAssignedIdentities@2023-01-31' existing = {
  name: identityName
}

resource containerRegistry 'Microsoft.ContainerRegistry/registries@2022-02-01-preview' existing = {
  name: containerRegistryName
}

resource containerAppsEnvironment 'Microsoft.App/managedEnvironments@2022-03-01' existing = {
  name: containerAppsEnvironmentName
}

resource ingestion_pipeline_job 'Microsoft.App/jobs@2023-04-01-preview' = {
  name: toLower(name)
  location: location
  identity: {
    type: 'UserAssigned'
    userAssignedIdentities: {
      '${userIdentity.id}': {}
    }
  }
  properties: {
    configuration: {
      scheduleTriggerConfig: {
        cronExpression: cronExpression
        replicaCompletionCount: replicaCompletionCount
        parallelism: parallelism
      }
      registries: [
        {
          server: '${containerRegistry.name}.azurecr.io'
          identity: userIdentity.id
        }
      ]
      replicaRetryLimit: replicaRetryLimit
      replicaTimeout: replicaTimeout
      triggerType: 'Schedule'
    }
    environmentId: containerAppsEnvironment.id
    template: {
      containers: [
        {
          args: []
          env: envVariables
          image: containerImage
          name: containerName
          resources: {
            cpu: json(cpu)
            memory: memory
          }
          volumeMounts: []
        }
      ]
      volumes: []
    }
    workloadProfileName: workloadProfileName
  }
}

// Outputs
output id string = ingestion_pipeline_job.id
output name string = ingestion_pipeline_job.name
