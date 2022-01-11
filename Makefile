# Application folders
        APP_NAME=Butler
        APP_name=butler
BUTLER_FOLDER=/home/gvalera/GIT/EG-Butler
      APP_FOLDER=${BUTLER_FOLDER}/app
  SERVICE_FOLDER=${BUTLER_FOLDER}/service
     MAIN_FOLDER=${APP_FOLDER}/main
TEMPLATES_FOLDER=${APP_FOLDER}/templates

# Suite Tools structure folders
SUITE_TOOLS_FOLDER=/home/gvalera/GIT/EG-Suite-Tools
  SUITE_APP_FOLDER=${SUITE_TOOLS_FOLDER}/${APP_NAME}
 SUITE_CODE_FOLDER=${SUITE_APP_FOLDER}/code

# Suite Auto Code Folders structure
   SUITE_AUTO_FOLDER=${SUITE_CODE_FOLDER}/auto
   SUITE_AUTO_MODELS=${SUITE_AUTO_FOLDER}/models
    SUITE_AUTO_FORMS=${SUITE_AUTO_FOLDER}/forms
    SUITE_AUTO_VIEWS=${SUITE_AUTO_FOLDER}/views
SUITE_AUTO_TEMPLATES=${SUITE_AUTO_FOLDER}/templates
 SUITE_AUTO_INCLUDES=${SUITE_AUTO_FOLDER}/includes

       BUTLER_TOOLS_FOLDER=/home/gvalera/GIT/EG-Butler-Tools
        BUTLER_CODE_FOLDER=${BUTLER_TOOLS_FOLDER}/code
           BUTLER_CODE_SRC=${BUTLER_CODE_FOLDER}/src
        BUTLER_CODE_COMMON=${BUTLER_CODE_SRC}/common
        BUTLER_CODE_OUTPUT=${BUTLER_CODE_FOLDER}/output
          BUTLER_CODE_AUTO=${BUTLER_CODE_FOLDER}/auto
#BUTLER_CODE_AUTO_TEMPLATES=${BUTLER_CODE_AUTO}/templates
#BUTLER_CODE_AUTO_TEMPLATES=${SUITE_AUTO_TEMPLATES}

# Emtec Library updates for Butler App
        LIB_EMTEC=/home/gvalera/GIT/eg-libraries/emtec/src/emtec
 LIB_EMTEC_COMMON=${LIB_EMTEC}/common
       LIB_BUTLER=${LIB_EMTEC}/butler
    LIB_BUTLER_DB=${LIB_BUTLER}/db
LIB_BUTLER_COMMON=${LIB_BUTLER}/common

#all:	${SUITE_AUTO_TEMPLATES}/base.html classes butler 
all:	base.html classes butler butler-api butler-core

show:	
	@echo
	@echo "***********************************"
	@echo "* Show Butler makefile context    *"
	@echo "***********************************"
	@echo
	@echo
	@echo "APP_NAME                      =" ${APP_NAME}
	@echo "APP_name                      =" ${APP_name}
	@echo "BUTLER_FOLDER                 =" ${BUTLER_FOLDER}
	@echo "APP_FOLDER                    =" ${APP_FOLDER}
	@echo "MAIN_FOLDER                   =" ${MAIN_FOLDER}
	@echo "TEMPLATES_FOLDER              =" ${TEMPLATES_FOLDER}
	@echo "SUITE_TOOLS_FOLDER            =" ${SUITE_TOOLS_FOLDER}
	@echo "SUITE_APP_FOLDER              =" ${SUITE_APP_FOLDER}
	@echo "SUITE_CODE_FOLDER             =" ${SUITE_CODE_FOLDER}
	@echo "SUITE_AUTO_FOLDER             =" ${SUITE_AUTO_FOLDER}
	@echo "SUITE_AUTO_MODELS             =" ${SUITE_AUTO_MODELS}
	@echo "SUITE_AUTO_FORMS              =" ${SUITE_AUTO_FORMS}
	@echo "SUITE_AUTO_VIEWS              =" ${SUITE_AUTO_VIEWS}
	@echo "SUITE_AUTO_TEMPLATES          =" ${SUITE_AUTO_TEMPLATES}
	@echo "SUITE_AUTO_INCLUDES           =" ${SUITE_AUTO_INCLUDES}
	@echo "BUTLER_TOOLS_FOLDER           =" ${BUTLER_TOOLS_FOLDER}
	@echo "BUTLER_CODE_FOLDER            =" ${BUTLER_CODE_FOLDER}
	@echo "BUTLER_CODE_SRC               =" ${BUTLER_CODE_SRC}
	@echo "BUTLER_CODE_COMMON            =" ${BUTLER_CODE_COMMON}
	@echo "BUTLER_CODE_OUTPUT            =" ${BUTLER_CODE_OUTPUT}
	@echo "BUTLER_CODE_AUTO              =" ${BUTLER_CODE_AUTO}
#	@echo "BUTLER_CODE_AUTO_TEMPLATES    =" ${BUTLER_CODE_AUTO_TEMPLATES}
	@echo "LIB_EMTEC                     =" ${LIB_EMTEC}
	@echo "LIB_EMTEC_COMMON              =" ${LIB_EMTEC_COMMON}
	@echo "LIB_BUTLER                    =" ${LIB_BUTLER}
	@echo "LIB_BUTLER_DB                 =" ${LIB_BUTLER_DB}
	@echo "LIB_BUTLER_COMMON             =" ${LIB_BUTLER_COMMON}


butler:	${BUTLER_CODE_OUTPUT}/models.py ${BUTLER_CODE_OUTPUT}/orm_model.py ${BUTLER_CODE_OUTPUT}/forms.py ${BUTLER_CODE_OUTPUT}/views.py ${BUTLER_CODE_SRC}/*.py ${SUITE_AUTO_TEMPLATES}/base.html
	@echo
	@echo "***********************************"
	@echo "* Updating Butler's  Auto Files *"
	@echo "***********************************"
	@echo
	@echo
	@echo "APP_NAME                      =" ${APP_NAME}
	@echo "APP_name                      =" ${APP_name}
	@echo "BUTLER_FOLDER              =" ${BUTLER_FOLDER}
	@echo "APP_FOLDER                    =" ${APP_FOLDER}
	@echo "MAIN_FOLDER                   =" ${MAIN_FOLDER}
	@echo "TEMPLATES_FOLDER              =" ${TEMPLATES_FOLDER}
	@echo "SUITE_TOOLS_FOLDER            =" ${SUITE_TOOLS_FOLDER}
	@echo "SUITE_APP_FOLDER              =" ${SUITE_APP_FOLDER}
	@echo "SUITE_CODE_FOLDER             =" ${SUITE_CODE_FOLDER}
	@echo "SUITE_AUTO_FOLDER             =" ${SUITE_AUTO_FOLDER}
	@echo "SUITE_AUTO_MODELS             =" ${SUITE_AUTO_MODELS}
	@echo "SUITE_AUTO_FORMS              =" ${SUITE_AUTO_FORMS}
	@echo "SUITE_AUTO_VIEWS              =" ${SUITE_AUTO_VIEWS}
	@echo "SUITE_AUTO_TEMPLATES          =" ${SUITE_AUTO_TEMPLATES}
	@echo "SUITE_AUTO_INCLUDES           =" ${SUITE_AUTO_INCLUDES}
	@echo "BUTLER_TOOLS_FOLDER        =" ${BUTLER_TOOLS_FOLDER}
	@echo "BUTLER_CODE_FOLDER         =" ${BUTLER_CODE_FOLDER}
	@echo "BUTLER_CODE_SRC            =" ${BUTLER_CODE_SRC}
	@echo "BUTLER_CODE_COMMON         =" ${BUTLER_CODE_COMMON}
	@echo "BUTLER_CODE_OUTPUT         =" ${BUTLER_CODE_OUTPUT}
	@echo "BUTLER_CODE_AUTO           =" ${BUTLER_CODE_AUTO}
#	@echo "BUTLER_CODE_AUTO_TEMPLATES =" ${BUTLER_CODE_AUTO_TEMPLATES}
	@echo "LIB_EMTEC                     =" ${LIB_EMTEC}
	@echo "LIB_EMTEC_COMMON              =" ${LIB_EMTEC_COMMON}
	@echo "LIB_BUTLER                 =" ${LIB_BUTLER}
	@echo "LIB_BUTLER_DB              =" ${LIB_BUTLER_DB}
	@echo "LIB_BUTLER_COMMON          =" ${LIB_BUTLER_COMMON}
	@echo
	@echo updating functions source files ...
	@echo
	./link_functions.sh
	@echo
	@echo updating ${LIB_BUTLER_DB}/flask_models.py ...
	@cp ${BUTLER_CODE_OUTPUT}/models.py       		${LIB_BUTLER_DB}/flask_models.py
	@echo
	@echo updating ${LIB_BUTLER_DB}/orm_model.py ...
	@cp ${BUTLER_CODE_OUTPUT}/orm_model.py       		${LIB_BUTLER_DB}/orm_model.py
	@echo
	@echo updating ${LIB_BUTLER}/forms.py ...
	@cp ${BUTLER_CODE_OUTPUT}/forms.py       		${LIB_BUTLER}/forms.py
	@echo
	@echo "updating ${MAIN_FOLDER}/views.py ..."
	@md5sum ${BUTLER_CODE_OUTPUT}/views.py
	#@md5sum ${MAIN_FOLDER}/views.py
	cp ${BUTLER_CODE_OUTPUT}/views.py       		${MAIN_FOLDER}/views.py
	#@md5sum ${BUTLER_CODE_OUTPUT}/views.py
	@md5sum ${MAIN_FOLDER}/views.py
	@echo
	@echo "updating ${TEMPLATES_FOLDER}/base.html ..."
	@echo
	@echo cp  ${SUITE_AUTO_TEMPLATES}/base.html        		${TEMPLATES_FOLDER}/base.html
	@cp  ${SUITE_AUTO_TEMPLATES}/base.html        		${TEMPLATES_FOLDER}/base.html
	@echo
	@ls -l ${SUITE_AUTO_TEMPLATES}/base.html
	@echo
	@ls -l ${TEMPLATES_FOLDER}/base.html
	@echo
	@echo "updating ${TEMPLATES_FOLDER} templates ..."
	@echo "from  ${SUITE_AUTO_TEMPLATES}/*.html templates ..."
	@echo "-------------------------------------------------------"
	@echo
	cp  ${SUITE_AUTO_TEMPLATES}/*.html     		${TEMPLATES_FOLDER}/.
	ls -l ~/butler/app/templates/navbar_template.html
	@echo
	@echo "from  ${BUTLER_CODE_SRC}/templates/*.html templates ..."
	@echo "-------------------------------------------------------"
	cp  ${BUTLER_CODE_SRC}/templates/*.html     		${TEMPLATES_FOLDER}/.
	cp  ${BUTLER_CODE_SRC}/app/templates/*.md	     	${TEMPLATES_FOLDER}/.
	ls -l ~/butler/app/templates/navbar_template.html
	@echo
	@echo "updating COMMON files to" ${LIB_BUTLER_COMMON}
	@echo
	@cp  ${BUTLER_CODE_COMMON}/butler/*.py     			${LIB_BUTLER_COMMON}/.
	@ls -l ${LIB_BUTLER_COMMON}/.
	@echo
	@echo
	@echo "updating error handlers ..."
	@echo
	cp  ${BUTLER_CODE_SRC}/errors.py			${MAIN_FOLDER}/errors.py
	@ls -l ${MAIN_FOLDER}/errors.py
	@echo
	@echo "updating application static programs ..."
	@echo
	cp  ${BUTLER_CODE_SRC}/*.py				${BUTLER_FOLDER}/.
	cp  ${BUTLER_CODE_SRC}/*.md				${BUTLER_FOLDER}/.
	cp  ${BUTLER_CODE_SRC}/app/*.py				${BUTLER_FOLDER}/app/.
	cp  ${BUTLER_CODE_SRC}/app/auth/*.py			${BUTLER_FOLDER}/app/auth/.
	cp  ${BUTLER_CODE_SRC}/app/main/*.py			${BUTLER_FOLDER}/app/main/.
	cp  ${BUTLER_CODE_SRC}/app/static/css/*.css		${BUTLER_FOLDER}/app/static/css/.
	cp  ${BUTLER_CODE_SRC}/app/static/css/*.map		${BUTLER_FOLDER}/app/static/css/.
	cp  ${BUTLER_CODE_SRC}/app/static/img/*.*		${BUTLER_FOLDER}/app/static/img/.
	cp  ${BUTLER_CODE_SRC}/app/static/js/*.js		${BUTLER_FOLDER}/app/static/js/.
	cp  ${BUTLER_CODE_SRC}/app/static/js/*.map		${BUTLER_FOLDER}/app/static/js/.
	cp  ${BUTLER_CODE_SRC}/app/templates/*.html		${BUTLER_FOLDER}/app/templates/.
	cp  ${BUTLER_CODE_SRC}/app/templates/auth/*.html	${BUTLER_FOLDER}/app/templates/auth/.
	cp  ${BUTLER_CODE_SRC}/app/templates/bootstrap/*.html	${BUTLER_FOLDER}/app/templates/bootstrap/.
	cp  ${BUTLER_CODE_SRC}/service/*.py			${BUTLER_FOLDER}/service/.
	cp  ${BUTLER_CODE_SRC}/daemons/*.py			${BUTLER_FOLDER}/daemons/.
	@echo
	@echo butler completed !!!
	@echo

classes:
	@echo
	@echo "***********************************"
	@echo "* Generating DB Clasess AUTOCODE  *"
	@echo "***********************************"
	@echo
	@echo "***********************************"
	@echo python ${SUITE_TOOLS_FOLDER}/gen_menu_2.py ${APP_NAME} ${SUITE_TOOLS_FOLDER} 
	@python ${SUITE_TOOLS_FOLDER}/gen_menu_j2.py ${APP_NAME} ${SUITE_TOOLS_FOLDER}
	@echo "***********************************"
	@touch ${BUTLER_CODE_SRC}/*.py 
	@touch ${BUTLER_CODE_SRC}/models/*.py
	@cd ${SUITE_TOOLS_FOLDER}
	python ${SUITE_TOOLS_FOLDER}/populate_dev_tables.py ${SUITE_TOOLS_FOLDER}/gen_butler.ini
	python ${SUITE_TOOLS_FOLDER}/gen_models_code.py ${SUITE_TOOLS_FOLDER}/gen_butler.ini
	@cd ${BUTLER_TOOLS_FOLDER}
	@echo
	@ls -l ${TEMPLATES_FOLDER}/base.html
	@echo

${BUTLER_CODE_OUTPUT}/models.py:	${BUTLER_CODE_SRC}/*.py ${BUTLER_CODE_SRC}/models/*.py
	@echo
	@echo "***********************************"
	@echo "* Creating models.py *"
	@echo "***********************************"
	@echo
	@cat ${BUTLER_CODE_SRC}/models_py_header.py  		>  ${BUTLER_CODE_OUTPUT}/models.py
	@cat ${BUTLER_CODE_SRC}/models_py_header_auth.py  	>> ${BUTLER_CODE_OUTPUT}/models.py
	@cat ${SUITE_AUTO_MODELS}/flask_*.py  				>> ${BUTLER_CODE_OUTPUT}/models.py
	@cat ${BUTLER_CODE_SRC}/models/*.py            		>> ${BUTLER_CODE_OUTPUT}/models.py
	@cat ${BUTLER_CODE_SRC}/models_py_User_footer.py  	>> ${BUTLER_CODE_OUTPUT}/models.py
	@ls -l ${BUTLER_CODE_OUTPUT}/models.py

${BUTLER_CODE_OUTPUT}/orm_model.py:	${BUTLER_CODE_SRC}/*.py 
	@echo
	@echo "***********************************"
	@echo "* Creating orm_model.py *"
	@echo "***********************************"
	@echo
	@cat ${BUTLER_CODE_SRC}/orm_models_py_header.py		>  	${BUTLER_CODE_OUTPUT}/orm_model.py
	@cat ${SUITE_AUTO_MODELS}/ORM_model.py  			>> 	${BUTLER_CODE_OUTPUT}/orm_model.py
	@cp  ${SUITE_AUTO_MODELS}/ORM_model_schema.py  		${BUTLER_CODE_OUTPUT}/orm_model_schema.py
	@ls -l ${BUTLER_CODE_OUTPUT}/orm_model.py

${BUTLER_CODE_OUTPUT}/forms.py:	${BUTLER_CODE_SRC}/*.py ${BUTLER_CODE_SRC}/forms/*.py
	@echo
	@echo "***********************************"
	@echo "* Creating forms.py *"
	@echo "***********************************"
	@echo
	@cat ${BUTLER_CODE_SRC}/forms_py_header.py  		>  ${BUTLER_CODE_OUTPUT}/forms.py
	@cat ${SUITE_AUTO_FORMS}/*.py  					>> ${BUTLER_CODE_OUTPUT}/forms.py
	@cat ${BUTLER_CODE_SRC}/forms/*.py            		>> ${BUTLER_CODE_OUTPUT}/forms.py
	@ls -l ${BUTLER_CODE_OUTPUT}/forms.py

${BUTLER_CODE_SRC}/forms/*.py:
	@echo
	@echo "***********************************"
	@echo "* Creating symbolic links for ${BUTLER_CODE_SRC}/forms/*.py *"
	@echo "***********************************"
	@echo
	./link_functions.sh

${BUTLER_CODE_OUTPUT}/views.py:	${BUTLER_CODE_OUTPUT}/models.py
	@echo
	@echo "***********************************"
	@echo "* Creating views.py *"
	@echo "***********************************"
	@echo
	@cat ${BUTLER_CODE_SRC}/views_py_header.py    		>  ${BUTLER_CODE_OUTPUT}/views.py
	@cat ${SUITE_AUTO_INCLUDES}/models_py_imports.py	>> ${BUTLER_CODE_OUTPUT}/views.py
	@cat ${SUITE_AUTO_VIEWS}/*.py                		>> ${BUTLER_CODE_OUTPUT}/views.py
	@cat ${BUTLER_CODE_SRC}/views/*.py            		>> ${BUTLER_CODE_OUTPUT}/views.py
	@ls -l ${BUTLER_CODE_OUTPUT}/views.py

base:
	@echo
	@echo "***********************************"
	@echo "* Generating base ...             *"
	@echo "***********************************"

base.html:
	@echo
	@echo "***********************************"
	@echo "* Generating ${SUITE_AUTO_TEMPLATES}/base.html"
	@echo "***********************************"
	@echo
	@echo "***********************************"
	@echo python ${SUITE_TOOLS_FOLDER}/gen_menu_j2.py ${APP_NAME} ${SUITE_TOOLS_FOLDER} 
	@python ${SUITE_TOOLS_FOLDER}/gen_menu_j2.py ${APP_NAME} ${SUITE_TOOLS_FOLDER}
	@echo "***********************************"
	@echo
	ls -l ${SUITE_AUTO_TEMPLATES}/base.html
	@echo
	ls -l ${TEMPLATES_FOLDER}/base.html
	@echo

clean:
	mv models/base.py models/base.py.sav
	rm models/*.py
	mv models/base.py.sav models/base.py
	rm forms/*.py
	rm views/*.py
	
	
butler-api:
	@echo
	@echo "***********************************"
	@echo "* Butler API Code Generation ...  *"
	@echo "***********************************"
	@echo
	@make -f butler-api-views.mk

butler-core:
	@echo
	@echo "***********************************"
	@echo "* Butler API Code Generation ...  *"
	@echo "***********************************"
	@echo
	@make -f butler-core.mk
	
