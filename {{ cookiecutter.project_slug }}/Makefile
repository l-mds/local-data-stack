.PHONY: tpl-update
## Update template project
tpl-update:
	pixi run tpl-update

.PHONY: notebook
## Start jupyter lab
notebook:
	pixi run notebook

.PHONY: start-dev
## Start dagster webserver
start-dev:
	pixi run start-dev


.PHONY: cleanup-state
## cleanup  state
cleanup-state:
	pixi run cleanup-state


.PHONY: fmt 
## basic auto formatting
fmt:
	pixi run -e ci-basics fmt


.PHONY: fmt-unsafe
## enhanced auto formatting
fmt-unsafe:
	pixi run -e ci-basics fmt-unsafe


.PHONY: lint
## Ruff based flake8 style linting plus type checking via pyright
lint:
	pixi run -e ci-validation lint


.PHONY: test
## Execute tests with coverage
test:
	pixi run -e ci-validation test



.PHONY: secrets-encrypt
## encrypt secrets with SOPS and AGE
secrets-encrypt:
	pixi run secrets-encrypt


.PHONY: secrets-decrypt
## encrypt secrets with SOPS and AGE
secrets-decrypt:
	pixi run secrets-decrypt


## cleanup local non used branches
clean-local-branches:
	pixi run clean-local-branches


#################################################################################
# PROJECT RULES                                                                 #
#################################################################################
#################################################################################
# Self Documenting Commands                                                     #
#################################################################################
.DEFAULT_GOAL := help
# Inspired by <http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html>
# sed script explained:
# /^##/:
# 	* save line in hold space
# 	* purge line
# 	* Loop:
# 		* append newline + line to hold space
# 		* go to next line
# 		* if line starts with doc comment, strip comment character off and loop
# 	* remove target prerequisites
# 	* append hold space (+ newline) to line
# 	* replace newline plus comments by `---`
# 	* print line
# Separate expressions are necessary because labels cannot be delimited by
# semicolon; see <http://stackoverflow.com/a/11799865/1968>
tasks:
	pixi task

.PHONY: help
help:
	@echo "$$(tput bold)Available rules:$$(tput sgr0)"
	@echo
	@sed -n -e "/^## / { \
		h; \
		s/.*//; \
		:doc" \
		-e "H; \
		n; \
		s/^## //; \
		t doc" \
		-e "s/:.*//; \
		G; \
		s/\\n## /---/; \
		s/\\n/ /g; \
		p; \
	}" ${MAKEFILE_LIST} \
	| LC_ALL='C' sort --ignore-case \
	| awk -F '---' \
		-v ncol=$$(tput cols) \
		-v indent=19 \
		-v col_on="$$(tput setaf 6)" \
		-v col_off="$$(tput sgr0)" \
	'{ \
		printf "%s%*s%s ", col_on, -indent, $$1, col_off; \
		n = split($$2, words, " "); \
		line_length = ncol - indent; \
		for (i = 1; i <= n; i++) { \
			line_length -= length(words[i]) + 1; \
			if (line_length <= 0) { \
				line_length = ncol - indent - length(words[i]) - 1; \
				printf "\n%*s ", -indent, " "; \
			} \
			printf "%s ", words[i]; \
		} \
		printf "\n"; \
	}' \
	| more $(shell test $(shell uname) = Darwin && echo '--no-init --raw-control-chars')
