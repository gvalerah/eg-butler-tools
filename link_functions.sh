MYPWD=$(pwd)
ROOT=/home/gvalera/butler
TOOLS=/home/gvalera/GIT/EG-Butler-Tools
CODE=$TOOLS/code
SRC=$CODE/src
FUNCTIONS=$SRC/functions
FORMS=$SRC/forms
VIEWS=$SRC/views
TEMPLATES=$SRC/templates

echo Starting in $MYPWD ...
echo Changing to $FUNCTIONS ...

cd $FUNCTIONS
for dir in ls *
do
    if [ -d "$dir" ]; then
        echo function: $dir
        echo "  changing to $(pwd)/$dir"
        cd $dir
        echo "    now in $(pwd)"
        # Process templates if not empty
        if [ "$(ls -A)" ]; then
            echo "    looking for templates ..."
            for file in *.html
            do
                echo "      template :" $file
                ln -f -s $FUNCTIONS/$dir/$file $TEMPLATES/$file
            done
        else
            echo No files in $dir ...
        fi
        # Process scripts if not empty
        if [ "$(ls -A)" ]; then
            echo "    looking for python scripts ..."
            for file in *.py
            do
            #echo procesando $file
                if [[ $file == 'frm_'* ]]; then
                    echo "      form     :" $file
                    ln -f -s $FUNCTIONS/$dir/$file $FORMS/$file
                else
                    if [[ $file == 'view_'* ]]; then
                        echo "      view     :" $file                
                        ln -f -s $FUNCTIONS/$dir/$file $VIEWS/$file                
                    fi
                fi
            done
        fi
        cd ..
    fi
done
echo returning to $MYPWD ...
cd $MYPWD
