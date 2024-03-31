# Tilefile for phoenix
print("Phoenix TiltFile is being evaluated")

# Microk8s registry
default_registry('localhost:32000')

docker_build('phoenix_superset', './python/projects/phoenix_superset/')

# Apply the secrets
k8s_yaml('./clusters/local/secrets.yaml')

k8s_yaml(helm(
  './charts/main/',
  name='phoenixchartmain',
  values='./clusters/local/values.yaml',
))
