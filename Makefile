all: \
	s50_q90_output.pdf \
	s40_q90_output.pdf \
	s33_q90_output.pdf \
	s25_q90_output.pdf \
	s15_q20_output.pdf

DEPS=generate.py dimensions.toml names.toml

s50_q90_output.pdf: $(patsubst ../pages/%.jpg,pages/s50_q90_%.jpg,$(wildcard ../pages/*.jpg)) $(DEPS)
	pipenv run ./generate.py 50 90

s40_q90_output.pdf: $(patsubst ../pages/%.jpg,pages/s40_q90_%.jpg,$(wildcard ../pages/*.jpg)) $(DEPS)
	pipenv run ./generate.py 40 90

s33_q90_output.pdf: $(patsubst ../pages/%.jpg,pages/s33_q90_%.jpg,$(wildcard ../pages/*.jpg)) $(DEPS)
	pipenv run ./generate.py 33 90

s25_q90_output.pdf: $(patsubst ../pages/%.jpg,pages/s25_q90_%.jpg,$(wildcard ../pages/*.jpg)) $(DEPS)
	pipenv run ./generate.py 25 90

s15_q20_output.pdf: $(patsubst ../pages/%.jpg,pages/s15_q20_%.jpg,$(wildcard ../pages/*.jpg)) $(DEPS)
	pipenv run ./generate.py 15 20

pages:
	mkdir -p pages

pages/s50_q90_%.jpg: ../pages/%.jpg | pages
	convert -quality 90 -resize 50% $< $@

pages/s40_q90_%.jpg: ../pages/%.jpg | pages
	convert -quality 90 -resize 40% $< $@

pages/s33_q90_%.jpg: ../pages/%.jpg | pages
	convert -quality 90 -resize 33% $< $@

pages/s25_q90_%.jpg: ../pages/%.jpg | pages
	convert -quality 90 -resize 25% $< $@

pages/s15_q20_%.jpg: ../pages/%.jpg | pages
	convert -quality 20 -resize 15% $< $@
