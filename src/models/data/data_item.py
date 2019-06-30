import datetime
import pandas as pd
from time import process_time
import os

from src.common.database import Database
from src.common.utils import Utils
import src.models.users.errors as UserErrors
import src.config as config
from src.common.utils import Utils


logger = Utils.get_logger(__name__)

class DataItem(object):

    def __init__(self, dataname, h5filepath, userid, columnsstring, filesize, description="", _id=None, created=None):
        self._id = _id
        self.userid = userid
        self.dataname=dataname
        self.h5filepath = h5filepath
        self.columnsstring = columnsstring
        self.filesize = filesize
        self.description = description
        self.created = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3] if created is None else created

    def __repr__(self):
        return "<DataItem Object {}>".format(self._id)

    def save_to_db(self):
        Database.insert(config.DATACOLLECTION, [self.json()])

    @classmethod
    def find_by_userid(cls, userid):
        item = Database.find(config.DATACOLLECTION, query={"userid": ["=", userid]}, one=True)
        if item is not None:
            return cls(**item)

    @classmethod
    def find_by_id(cls, dataid):
        item = Database.find(config.DATACOLLECTION, query={"_id": ["=", dataid]}, one=True)
        if item is not None:
            return cls(**item)

    def remove_from_DB(self):
        Database.remove(config.DATACOLLECTION, query={"_id": ["=", self._id]})

    def update_DB(self):
        Database.update(config.DATACOLLECTION, self.json(), query={"_id": ["=", self._id]})

    def json(self):
        return {"_id": self._id,
                "userid": self.userid,
                "dataname": self.dataname,
                "h5filepath": self.h5filepath,
                "created": self.created,
                "columnsstring": self.columnsstring,
                "filesize": self.filesize,
                "description": self.description}


    def columns(self):
    	return self.columnsstring.split(',')


    @classmethod
    def getDataItems(cls):
    	return [cls(**data) for data in Database.find(config.DATACOLLECTION)]


    ### Integrate from Clemens-Otte Workbench ###
    @staticmethod
    def import_csv(csv_file):
        t0 = process_time()

        # BDAS encodes sensor failures as -9999
        try:
            df = pd.read_csv(csv_file, parse_dates=['Time'], na_values=['ERROR', '-9999', '-9999.0'])
            df.set_index(['Time'], inplace=True, verify_integrity=True)
            for col in df.columns:
                if not df[col].dtype is np.dtype(np.float):
                    # Try to convert the individual elements of the bad column to float.
                    val = np.empty((len(df.index), ))
                    for i, x in enumerate(df[col].values):
                        try:
                            val[i] = np.float(x)
                        except ValueError:
                            val[i] = np.NaN
                            logger.warning(col + ': cannot parse "%s" as float, replaced by NaN.' % str(x))
                    df[col] = pd.Series(val, index=df.index)
            logger.info('%s: read_csv took %.2fs' % (os.path.basename(csv_file), process_time() - t0))
        except:
            logger.info('Parsing failed!')
            df = pd.read_csv(csv_file, na_values=['ERROR', '-9999', '-9999.0'])

        return df

    @staticmethod
    def get_dataset_name(filename):
        return os.path.basename(filename).replace('.csv.zip', '').replace('.', '_')