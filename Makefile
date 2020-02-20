all: coverageclean test coverage quality

coverageclean:
	rm -fr .coverage

clean: coverageclean typecoverageclean
	FILES=$$(find . -name \*.pyc); for f in $${FILES}; do rm $$f; done

test:
	ENV=test nosetests --exclude='tests/integration' --cover-package=sqla_vertica_python --with-coverage --with-xunit --cover-html --cover-xml --nocapture --cover-inclusive

citest:
	ENV=test nosetests --exclude='tests/integration' --cover-package=sqla_vertica_python --with-coverage --with-xunit --cover-html --cover-xml --nocapture --cover-inclusive --xunit-file=test-reports/junit.xml

coverage:
	python setup.py coverage_ratchet

cicoverage: coverage
	@echo "Looking for un-checked-in unit test coverage metrics..."
	@git status --porcelain metrics/coverage_high_water_mark
	@test -z "$$(git status --porcelain metrics/coverage_high_water_mark)"

flake8:
	flake8 bluelabs_joblib tests

quality-flake8:
	make QUALITY_TOOL=flake8 quality

quality-punchlist:
	make QUALITY_TOOL=punchlist quality

# to run a single item, you can do: make QUALITY_TOOL=bigfiles quality
quality:
	@quality_gem_version=$$(python -c 'import yaml; print(yaml.safe_load(open(".circleci/config.yml","r"))["quality_gem_version"])'); \
	docker run  \
	       -v "$$(pwd):/usr/app"  \
	       -v "$$(pwd)/Rakefile.quality:/usr/quality/Rakefile"  \
	       "apiology/quality:$${quality_gem_version}" ${QUALITY_TOOL}

package:
	python3 setup.py sdist bdist_wheel
