setup_asdf:
	echo "Setting up asdf"
	asdf plugin list | grep -q helm || asdf plugin add helm
	asdf plugin list | grep -q tilt || asdf plugin add tilt
	asdf plugin list | grep -q nodejs || asdf plugin add nodejs
	asdf plugin list | grep -q kubectl || asdf plugin-add kubectl https://github.com/asdf-community/asdf-kubectl.git
	asdf install
	asdf reshim

up:
	if [ -f clusters/local/secrets.yaml ]; then \
		tilt up; \
	else \
		echo "File clusters/local/secrets.yaml does not exist."; \
		echo "Copying the example file"; \
		cp clusters/.example_secrets.yaml clusters/local/secrets.yaml; \
		echo "Please fill in the clusters/local/secrets.yaml file and run 'make up' again"; \
	fi
