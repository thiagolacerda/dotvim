TOP := $(shell pwd)

all:
	@test -e vimrc\
		|| echo "Cannot find vimrc. Did you run ./configure.sh?"

install:
	@ln -s ~+/vimrc ~/.vimrc\
		&& echo "dotvim successfully installed"\
		|| echo "can't install dotvim"

uninstall:
	@test -L ~/.vimrc\
		&& rm ~/.vimrc\
		&& echo "~/.vimrc successfully removed"\
		|| echo "Can't remove ~/.vimrc (the only installed file)"
