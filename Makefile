.PHONY: all clean distclean

DPI_100=768
DPI_50=384
DPI_39=300
DPI_25=192
DPI_15=115

DEPS=generate.py names.toml
FILES=\
	output_s100_q90_d$(DPI_100).pdf \
	output_s50_q90_d$(DPI_50).pdf \
	output_s39_q90_d$(DPI_39).pdf \
	output_s25_q90_d$(DPI_25).pdf \
	output_s15_q20_d$(DPI_15).pdf

all: $(FILES)

distclean: clean
	rm -f $(FILES)

output_s100_q90_d$(DPI_100).pdf: $(patsubst ../pages/%.jpg,pages/s100_q90_%.jpg,$(wildcard ../pages/*.jpg)) $(DEPS)
	pipenv run ./generate.py 100 90 $(DPI_100)

output_s50_q90_d$(DPI_50).pdf: $(patsubst ../pages/%.jpg,pages/s50_q90_%.jpg,$(wildcard ../pages/*.jpg)) $(DEPS)
	pipenv run ./generate.py 50 90 $(DPI_50)

output_s39_q90_d$(DPI_39).pdf: $(patsubst ../pages/%.jpg,pages/s39_q90_%.jpg,$(wildcard ../pages/*.jpg)) $(DEPS)
	pipenv run ./generate.py 39 90 $(DPI_39)

output_s25_q90_d$(DPI_25).pdf: $(patsubst ../pages/%.jpg,pages/s25_q90_%.jpg,$(wildcard ../pages/*.jpg)) $(DEPS)
	pipenv run ./generate.py 25 90 $(DPI_25)

output_s15_q20_d$(DPI_15).pdf: $(patsubst ../pages/%.jpg,pages/s15_q20_%.jpg,$(wildcard ../pages/*.jpg)) $(DEPS)
	pipenv run ./generate.py 15 20 $(DPI_15)

pages:
	mkdir -p pages

pages/s100_q90_%.jpg: ../pages/%.jpg | pages
	convert -quality 90 -resize 100% $< $@

pages/s50_q90_%.jpg: ../pages/%.jpg | pages
	convert -quality 90 -resize 50% $< $@

pages/s39_q90_%.jpg: ../pages/%.jpg | pages
	convert -quality 90 -resize 39% $< $@

pages/s25_q90_%.jpg: ../pages/%.jpg | pages
	convert -quality 90 -resize 25% $< $@

pages/s15_q20_%.jpg: ../pages/%.jpg | pages
	convert -quality 20 -resize 15% $< $@

clean:
	rm -f pages/s*_q*_*.jpg
