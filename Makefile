.PHONY: help
help:
	@echo "(TODO)"

.PHONY: clean
clean:
	rm -rf node_modules
	rm -rf examples/rv-react-ts-example/node_modules
	rm -rf dist
	rm -rf tmp

.PHONY: devpi-upload
devpi-upload:
	devpi upload

.PHONY: testenv
testenv:
	mkdir -p tmp
	python -m venv tmp/testenv
	tmp/testenv/bin/pip install ipython

.PHONY: devpi-install
devpi-install: testenv devpi-upload
	source tmp/testenv/bin/activate && devpi install radiant-voices

.PHONY: testenv-shell
testenv-shell: devpi-upload testenv devpi-install
	tmp/testenv/bin/ipython

.PHONY: twine-upload
twine-upload:
	twine upload dist/radiant-voices-*.tar.gz

.PHONY: npm-build
npm-build: clean
	npm install
	npm run tsc

.PHONY: genrv
genrv:
	python -m genrv.tools.generate --config genrv-config.yaml
