# Tilefile for phoenix
print("Phoenix TiltFile is being evaluated")

# Microk8s registry
default_registry('localhost:32000')

sync_config = sync('./python/projects/phoenix_superset/config.py', '/app/phoenix_superset/config.py')
sync_phoenix = sync('./python/projects/phoenix_superset/phoenix_superset/', '/app/phoenix_superset/phoenix_superset/')
docker_build('phoenix_superset', './python/projects/phoenix_superset/', live_update=[
    sync_config,
    sync_phoenix,
])

sync_phiphi = sync('./python/projects/phiphi/phiphi/', '/app/projects/phiphi/phiphi/')
docker_build(
  'phiphi',
  './python/',
  build_args={'PROJECT': 'phiphi'},
  live_update=[
    sync_phiphi,
  ],
)

k8s_yaml(helm(
  './charts/main/',
  name='phoenix',
  values=['./clusters/local/values.yaml'],
))
