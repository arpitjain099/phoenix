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
  'phiphi-dev-image',
  './python/',
  build_args={'PROJECT': 'phiphi'},
  live_update=[
    sync_phiphi,
  ],
  match_in_env_vars=True,
)

sync_console_ui = sync('./console_ui/src/', '/app/src/')
docker_build(
  'phoenix_console',
  './console_ui/',
  dockerfile='./console_ui/Dockerfile.dev',
  live_update=[sync_console_ui]
)

k8s_yaml(helm(
  './charts/main/',
  name='phoenix',
  values=['./clusters/local/values.yaml', './clusters/local/secrets.yaml'],
))


has_prefect_server = read_yaml('./clusters/local/values.yaml').get('prefect-server')
if has_prefect_server:
  if has_prefect_server.get('enabled'):
    print("Prefect Server is enabled")
    k8s_resource(workload='prefect-server', port_forwards=4200)
