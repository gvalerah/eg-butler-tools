GIT=/home/gvalera/GIT
AUTO=$(GIT)/EG-Suite-Tools/Butler/code/auto/views
SRC=$(GIT)//EG-Butler-Tools/code/src
BUTLER=$(GIT)/EG-Butler
CORE=$(SRC)/core

core:	$(SRC)/butler-core.py $(CORE)/*.py
	@cp -rf $(SRC)/butler-core.py ${BUTLER}/butler-core.py
	@cp -rf $(CORE)/*.py ${BUTLER}/core
	@ls -lh $(BUTLER)/butler-core.py
	@ls -lh $(BUTLER)/core
	@echo
	@echo Butler CORE completed.
	@echo 
