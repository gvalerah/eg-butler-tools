GIT=/home/gvalera/GIT
AUTO=$(GIT)/EG-Suite-Tools/Butler/code/auto/views
SRC=$(GIT)//EG-Butler-Tools/code/src
BUTLER=$(GIT)/EG-Butler
VIEWS=$(BUTLER)/api/main/views.py
TIMESTAMP=$("shell date +%Y%m%d-%H:%M:%S")

views:	$(SRC)/views_butler_api_py_header.py $(SRC)/views_butler_api.py
	@echo "# butler-api-views.mk AG: $(TIMESTAMP)"  >  $(VIEWS)
	@cat $(SRC)/views_butler_api_py_header.py >>  $(VIEWS)
	@cat $(SRC)/views_butler_api.py           >> $(VIEWS)
	@cat $(AUTO)/*api.html.auto               >> $(VIEWS)
	@ls -lh $(VIEWS)
	@echo
	@echo Butler API Make Views completed.
	@echo 



