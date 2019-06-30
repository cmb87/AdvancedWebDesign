from flask import Blueprint, request, session, redirect, url_for, render_template
import os
import datetime
import pandas as pd
from src.common.flask_redirect import redirect_url
from src.models.users.decorators import requires_login
from src.models.users.user import User
from src.models.data.data_item import DataItem
from src.common.utils import Utils

data_blueprint = Blueprint('data', __name__)

uploaddir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
            os.path.normpath('../../../../uploaded'))

logger = Utils.get_logger(__name__)

@data_blueprint.route('/upload', methods=['POST'])
@requires_login
def handle_upload():

    ### Get file descriptions from form ###
    description = "NA" #request.form.get('dataUploadTextArea')


    ### Get user id ###
    userid = User.find_by_email(session["email"])._id

    ### Create data folder ###
    datadir = os.path.join(uploaddir,os.path.normpath("{}/".format(userid)))

    if not os.path.exists(datadir):
        os.mkdir(datadir)

    ### upload data ###
    h5_output_file = os.path.join(datadir,os.path.normpath("userdata.h5"))

    ### Store compress data has hd5
    with pd.HDFStore(h5_output_file, mode='a', complevel=9) as store:

        for key, f in request.files.items():
            if key.startswith('file'):
                
                ### data to server ###
                file = os.path.join(datadir, f.filename)
                f.save(file)

                ### Store csvfile in h5 format ###
                df = DataItem.import_csv(file)
                dataname = DataItem.get_dataset_name(file)
                columnsstring = ','.join(list(df.columns))
                filesize = os.path.getsize(file)

                ctr,dataname0 = 0,dataname
                while '/'+dataname in store.keys():
                    logger.warning("Dataset exists! Changing name in DB.")
                    dataname=dataname0+"_"+str(ctr)
                    ctr+=1

                store.put(dataname, df)                

                ### Create data object ###
                dataItem = DataItem(dataname, h5_output_file, userid, columnsstring, filesize, description=description).save_to_db()

                ### Delete csv file ###
                try:
                    os.remove(file)
                except:
                    logger.warning("Couldn't delete file: {}".format(file))

    return '', 204


@data_blueprint.route('/form', methods=['POST'])
def handle_form():
    description = request.form.get('dataUploadTextArea')
    return 'file uploaded and form submit<br>title: %s<br> description: %s' % ("title", description)


@data_blueprint.route('/explorer')
@requires_login
def explorer():
    return render_template("data/databrowser.html", dataItems=DataItem.getDataItems())
    

@data_blueprint.route('/remove')
@requires_login
def remove():

    
    item = DataItem.find_by_id(request.args.get('dataid'))
    
    if not item is None: 
        item.h5filepath
        item.dataname

        with pd.HDFStore(item.h5filepath) as store:
            store.remove(item.dataname)

        item.remove_from_DB()
        del item;
        return "DataItem deleted successfully!"


    return "Couldn't delete DataItem"