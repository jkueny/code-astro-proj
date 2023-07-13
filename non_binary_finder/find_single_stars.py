#Import the necessary modules
from astropy import units as u
from astropy.coordinates import SkyCoord, Angle
from astropy.wcs import WCS
import warnings
import numpy as np
warnings.filterwarnings('ignore')
from astroquery.vizier import Vizier
from astroquery.simbad import Simbad
# %matplotlib inline
import matplotlib.pyplot as plt
from IPython.display import Image
from IPython.core.display import HTML
import pandas as pd

def query_the_gaia(objloc,conerad,catalognamelist=["I/350/gaiaedr3","B/wds"],RUWE=True,maghigh=3,maglow=10):
    """
    This function will query the input list of catalogs using the Astropy Vizier API.

    Args:
        catalognamelist (list): List of catalog name strings as shown on Vizier. 
        Ex. "I/350/gaiaedr3"
        objloc (string): RA/Dec coordinate pair to pass into Vizier.query_region().
        Ex. "11 02 24.8763629208 -77 33 35.667131796"
        conerad (float): Cone radius in degrees.

    Returns:
        Pandas DataFrame: CSV saved to disk in the directory where this script is located.
    """ 
    ## change row limit to none; else default to 50 
    Vizier.ROW_LIMIT = -1   
    if len(objloc) == 2:
         obj_coord=SkyCoord(objloc[0],objloc[1],unit=(u.degree, u.degree), frame='icrs')
    else:
        obj_coord=SkyCoord(objloc,unit=(u.hourangle, u.degree), frame='icrs')
    
    #making sure cone radius value is proper

    conerad= np.abs(conerad)

    if conerad == 0:
        raise ValueError("Search radius is 0!")

    if conerad >= 2.0:
        print("Search radius is large, will take longer to run ")    
    
    #bright magnitude messages

    if maglow-maghigh <=0:
        raise ValueError("Magnitude search range is invalid!")

    result = Vizier.query_region(obj_coord,
                            radius=u.Quantity(conerad,u.deg),
                             catalog=catalognamelist)
    
    if RUWE:
        result=result[0][result[0]['RUWE']<1.2]

    #filtering more by G magnitude
    result=result[result['Gmag']>maghigh] 
    result=result[result['Gmag']<maglow]
        
    gaia_id_list=result['Source']

    header_list = ["Object_Name","RA","DEC","Mean_Gmag","RUWE"]
    singles = []
    for each,id in enumerate(gaia_id_list):
        gaia_id= "Gaia DR3"+str(id)
        info=Simbad.query_objectids(gaia_id)
        strinfo=str(info)
        if 'wds' in strinfo:
            gaia_id_list.remove(id)
        elif type(info)== None:
            gaia_id_list.remove(id)
        else:
            simbadinfo=Simbad.query_object(gaia_id)
            singles.append([simbadinfo['MAIN_ID'][0],simbadinfo['RA'][0],simbadinfo['DEC'][0],result[each]['Gmag'],result[each]['RUWE']])

    df=pd.DataFrame(singles,columns=header_list)
    sorted_df = df.sort_values(by='Mean_Gmag', ascending=True)
    sorted_df.to_csv("Non-Binary.csv", sep= " ",header=False)

    return sorted_df


print(query_the_gaia(objloc="11 02 24.8763629208 -77 33 35.667131796",
               conerad=0.5,
               ))
