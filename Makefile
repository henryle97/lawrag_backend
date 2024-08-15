.PHONY: format-code build-image-dev  code-score

format-code:
	bash scripts/format_code.sh

build-image-dev:
	bash scripts/build_image_dev.sh

code-score:
	bash scripts/code_score.sh
