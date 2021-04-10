all:	install

eg-butler-api:	eg-butler-api.py
	@echo
	@echo Compiling eg-butler-api ...
	pyinstaller --onefile eg-butler-api.py
	@echo

eg-butler-core:	eg-butler-core.py
	@echo
	@echo Compiling eg-butler-core ...
	pyinstaller --onefile eg-butler-core.py
	@echo

install:	eg-butler-api eg-butler-core
	@echo
	@echo Copying butler executables to butler ...
	sshpass -p butler scp dist/eg-butler* butler@butler:~/.
	sshpass -p butler ssh butler@butler ls -l
	@echo

