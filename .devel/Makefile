# Copyleft (C) 2020-2022, Marek Gagolewski <https://www.gagolewski.com>

#VPATH="/home/gagolews/Python/genieclust"


.PHONY: all user

all: please_specify_build_target_manually

user:
	cd .. && CPPFLAGS="-fopenmp -march=native -mtune=native" \
		LDFLAGS="-fopenmp" python3 setup.py install --user
	jupyter-qtconsole-sender --silent "import importlib, genieclust; \
genieclust = importlib.reload(genieclust); \
print(\"Package 'genieclust' reloaded.\")"
