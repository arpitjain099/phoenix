setup_asdf:
	echo "Setting up asdf"
	asdf plugin list | grep -q helm || asdf plugin add helm
	asdf plugin list | grep -q tilt || asdf plugin add tilt
	asdf plugin list | grep -q nodejs || asdf plugin add nodejs
	asdf plugin list | grep -q kubectl || asdf plugin-add kubectl https://github.com/asdf-community/asdf-kubectl.git
	asdf install
	asdf reshim

up:
	tilt up

clean:
	tilt down
	@echo "Deleting all pvc in mircok8s cluster default namespace."
	kubectl delete pvc --all -n default --context microk8s

local_auth_up:
	if [ -f clusters/local_with_auth/secrets.yaml ]; then \
		tilt up -f Tiltfile.local_with_auth; \
	else \
		echo "File clusters/local_with_auth/secrets.yaml does not exist."; \
		echo "Copying the example file"; \
		cp charts/main/example_secrets.yaml clusters/local_with_auth/secrets.yaml; \
		echo "Please fill in the clusters/local/secrets.yaml file and run 'make up' again"; \
	fi

local_auth_clean:
	tilt down -f Tiltfile.local_with_auth;
	@echo "Deleting all pvc in mircok8s cluster default namespace."
	kubectl delete pvc --all -n default --context microk8s

dev_up:
	if [ -f clusters/dev/secrets.yaml ]; then \
		echo "Starting tilt with dev context"; \
		tilt up -f Tiltfile.dev; \
	else \
		echo "File clusters/dev/secrets.yaml does not exist."; \
		echo "Copying the example file"; \
		cp charts/main/example_secrets.yaml clusters/dev/secrets.yaml; \
		echo "Please fill in the clusters/dev/secrets.yaml file and run 'make dev_up' again"; \
	fi

dev_clean:
	tilt down -f Tiltfile.dev
	@echo "Deleting all pvc in ${KUBE_DEV_CONTEXT} cluster ${DEV_NAMESPACE} namespace."

	kubectl delete pvc --all -n ${DEV_NAMESPACE} --context ${KUBE_DEV_CONTEXT}
