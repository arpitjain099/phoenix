setup_asdf:
	echo "Setting up asdf"
	asdf plugin list | grep -q helm || asdf plugin add helm
	asdf plugin list | grep -q tilt || asdf plugin add tilt
	asdf plugin list | grep -q nodejs || asdf plugin add nodejs
	asdf plugin list | grep -q kubectl || asdf plugin-add kubectl https://github.com/asdf-community/asdf-kubectl.git
	asdf install
	asdf reshim

up:
	if [ -f clusters/local/secret.yaml ]; then \
		kubectl apply -f clusters/local/secret.yaml; \
		tilt up; \
	else \
		echo "File clusters/local/secret.yaml does not exist."; \
		echo "Copying the example file"; \
		cp clusters/local/.example_secrets.yaml clusters/local/secret.yaml; \
		echo "Please fill in the clusters/local/secret.yaml file and run 'make up' again"; \
	fi
