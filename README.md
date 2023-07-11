# code-astro-proj
The need for a single, bright star for calibrations arises for many astronomers. The purpose of this package is to return a catalog of bright, likely single stars.


So we want to put in a RA Dec as command line arguments

Then this inputs into a function along with cone search radius. This function queries the Gaia catalog with certain conditionals such as star brightness as well as the RUWE metric. (TODO check what objects Gaia will output by default, is it only point sources??)

For each returned object, we reject any also present in the Washington Double Star catalog (WDS). We can do the cross match by 
