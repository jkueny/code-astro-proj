#Import the necessary modules
from astropy import units as u
from astropy.coordinates import SkyCoord, Angle
from astropy.wcs import WCS
import warnings
import numpy as np
warnings.filterwarnings('ignore')
from astroquery.vizier import Vizier
from astroquery.simbad import Simbad
#%matplotlib inline
import matplotlib.pyplot as plt
from IPython.display import Image
from IPython.core.display import HTML
import pandas as pd

## change row limit to none; else default to 50 
Vizier.ROW_LIMIT = -1

def query_the_gaia(objloc,conerad,catalognamelist=["I/350/gaiaedr3","B/wds"],RUWE=True,maghigh=3,maglow=10):
    """
    This function will query the specified catalogs using Astropy Vizier.

    Args:
        catalognamelist (list): List of catalog name strings as shown on Vizier. 
        Ex. "I/350/gaiaedr3"
        objra (float): RA coord in degrees
        objdec (float): Dec coord in degrees
        conerad (float): Cone radius in degrees

    Returns:
        _type_: _description_
    """    
    if len(objloc) == 2:
         obj_coord=SkyCoord(objloc[0],objloc[1],unit=(u.degree, u.degree), frame='icrs')
    else:
        obj_coord=SkyCoord(objloc,unit=(u.hourangle, u.degree), frame='icrs')
    result = Vizier.query_region(obj_coord,
                            radius=u.Quantity(conerad,u.deg),
                             catalog=catalognamelist )
    
    
    if RUWE:
        result=result[0][result[0]['RUWE']<1.2]

    #filtering more by G magnitude
    result=result[result['Gmag']>maghigh] 
    result=result[result['Gmag']<maglow]
        
    gaia_id_list=result['Source']

    # TODO add column headers for name, RA, DEC, RUWE, mag
    singles=[["Object_Name","RA","DEC","Mean_Gmag","RUWE"]]
    for i in gaia_id_list:
        id= "Gaia DR3"+str(i)
        info=Simbad.query_objectids(id)
        strinfo=str(info)
        if 'wds' in strinfo:
            gaia_id_list.remove(i)
        elif type(info)== None:
            gaia_id_list.remove(i)
        else:
            simbadinfo=Simbad.query_object(id)
            singles.append([simbadinfo['MAIN_ID'][0],simbadinfo['RA'][0],simbadinfo['DEC'][0],result['Gmag'][0],result[0]['RUWE']])

    df=pd.DataFrame(singles)
    df.to_csv("Non-Binary.csv", sep= " ",header=False)

    return 