# source: code/src/include/models/flask_users_methods.py
# Required for Load_Table Function
import  pandas      as      pandas
from    pathlib     import  Path
# imports orm_model as local definitions for DB popuplation
import  emtec.butler.orm_models   as      orm_model
       
def Load_Table(self,class_name,filename,separator=','):
    my_file = Path(filename)
    if my_file.is_file():
        # file exists
        # Gets type of recodr class by name
        table_class=getattr(orm_model,class_name)
        # reads data from CSV (separator can be specified to change format
        # if needed, no default NaN values will be used
        df=pandas.read_csv(filename,sep=separator,keep_default_na=False)
        # iterate over rows with iterrows()
        for index, row in df.iterrows():
            instance=table_class()
            # access data using column names
            for column in list(df.columns.values):
                value = None if pandas.isnull(row[column]) else row[column]
                setattr(instance, column, value)
                try:
                    self.session.add(instance)
                except Exception as e:
                    print("Load_table: Could not add instance of %s: %s %s"%(instance,class_name,e))
                    return False
        try:
            self.session.commit()
        except Exception as e:
            #print("Load_table: Could not commit session: %s %s"%(self.session,e))
            print("Load_table: Could not commit session: %s %s"%(self.session,'e'))
            self.session.rollback()
            return False
        return True
    else:
        return False
