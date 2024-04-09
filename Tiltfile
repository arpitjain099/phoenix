# Tilefile for phoenix
print("Phoenix TiltFile is being evaluated")

# Apply the secrets
k8s_yaml('./clusters/local/secrets.yaml')

k8s_yaml(helm(
  './charts/main/',
  name='phoenixchartmain',
  values='./clusters/local/values.yaml',
))
