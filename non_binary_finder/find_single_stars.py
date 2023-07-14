#Import the necessary modules
from astropy import units as u
from astropy.coordinates import SkyCoord, Angle
from astropy.wcs import WCS
import warnings
import numpy as np
# warnings.filterwarnings('ignore')
from astroquery.vizier import Vizier
from astroquery.simbad import Simbad
# %matplotlib inline
import matplotlib.pyplot as plt
from IPython.display import Image
from IPython.core.display import HTML
import pandas as pd
import re

def determine_coord_units(incoords):
    ok_chars = r'[^0-9\s+-.]'  # re filter any non-numericals; keeping spaces, decimal pts, +/-
    found_chars_not_ok = re.findall(ok_chars, incoords)
    print(found_chars_not_ok)
    if (type(incoords) == list) or (type(incoords) == tuple):
        if len(incoords) > 1:
            raise TypeError("Pls remove unecessary brackets; only separate RA/Dec with spaces.")
    if type(incoords) != str:
        raise TypeError("Please input RA/Dec pair as a string.")
    if ":" in  incoords:
        raise ValueError("Please separate HMS values by spaces only.")
    if len(found_chars_not_ok) > 0:
        raise ValueError("Invalid character(s)! Please separate by spaces only and no brackets.")
    deconstruct_coords_string = incoords.split()
    if len(deconstruct_coords_string) > 2:
        print('Recognized input coordinate in HMS format.')
        coord_units = (u.degree, u.degree)
    else:
        print('Recognized input coordinate in degree format.')
        coord_units = (u.hourangle, u.degree)
    return coord_units


def query_the_gaia(objloc,conerad,catalognamelist=["I/350/gaiaedr3","B/wds"],RUWE=True,maghigh=3,maglow=10):
    """

    This function will query the input list of catalogs using the Astropy Vizier API.

    Args:
        - objloc (string): RA/Dec coordinate pair to pass into Vizier.query_region().
        Ex. "11 02 24.8763629208 -77 33 35.667131796"

        - conerad (float): Cone radius in degrees.

        - catalognamelist (list): List of catalog name strings as shown on Vizier. [optional]
        Ex. "I/350/gaiaedr3"

        - RUWE (bool): Toggle RUWE filtering metric (refer to README for theory) [optional]

        - maghigh (float): Brightness limit for queried objects. [optional]

        - maglow (float): Faintness limit for queried objects. [optional]

    Returns:
        pd.DataFrame: CSV saved to disk in the directory where this script is located.

    """ 
    ## change row limit to none; else default to 50 
    Vizier.ROW_LIMIT = -1
    input_coord_units = determine_coord_units(objloc)
    obj_coord = SkyCoord(objloc,unit=(input_coord_units), frame='icrs')
    # if len(objloc) == 2:
    #      obj_coord=SkyCoord(objloc[0],objloc[1],unit=input_coord_units), frame='icrs')
    # else:
    #     obj_coord=SkyCoord(objloc,unit=input_coord_units, frame='icrs')
    
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
    sorted_df.to_csv("bright_single_stars_catalog.csv", sep= " ",header=False)

    return sorted_df


# print(query_the_gaia(objloc=("11 02 24.8763629208 -77 33 35.667131796"),
#                conerad=0.5,
#                ))
# print(query_the_gaia(objloc=("165.520318183 -77.5599075361"),
#                conerad=0.5,
#                ))
