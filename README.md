# code-astro-proj

# Instructions for use

- 

The need for a single, bright star for calibrations arises for many astronomers interested in high-resolution imaging. The purpose of this package is to return a catalog of bright, likely single stars by filtering out multiple star systems.

By default, this package does this by cross-matching the Gaia DR3 catalog with the Washington Double-Star Catalog (WDS) which exists to flag visual binaries. Other catalogs may be passed-in as arguments for additional functionality, though positive cross-match results means those objects will be excluded from the final CSV catalog. It also features user-set options for Renormalized Unit Weight Error (RUWE) and magnitude range to suit the user's needs.

From the Gaia docs:

"The RUWE is expected to be around 1.0 for sources where the single-star model provides a good fit to the astrometric observations. A value significantly greater than 1.0 (say, >1.4) could indicate that the source is non-single or otherwise problematic for the astrometric solution."

By default, the RUWE threshold is set to >1.2.

Specifically, the cross-matching is done by additionally querying the SIMBAD (Set of Identifications, Measurements and Bibliography for Astronomical Data) astronomical database and checking the known identifiers for each object (i.e., if a star has a WDS identifier on SIMBAD, it is rejected). 

The final catalog of filtered objects is output in Comma-Seperated Value (CSV) format in the directory the program is located. ([TODO] is this what we want? Should we code in a specified directory?) 

The catalog columns include SIMBAD object name, Gaia identifier, RA, Dec, (V or SDSS i or Gaia G) magnitude, RUWE. The objects are sorted by decreasing brightness with increasing row number (i.e., first row contains the brightest star).

Future plans for this project include creating a SQL database to populate with multiple star systems as some of these objects will undoubtedly get through this process. For instance, the resolution capabilities of the instruments used to populate the WDS or the Gaia space telescope are often superceded by larger, ground-based telescopes meaning that unresolved multiple star systems are often serendipitously resolved for ground-based diffraction-limited imaging. For these cases, the object will be input into the database to exclude from future query results leading to increased accuracy over time.



[TODO] Change repository name to be more unique/descriptive, but how does this change git behavior?
[TODO] make more general by defining more (all?) object identifiers in SIMBAD for additional catalog inputs on command line. This way we only ever need to query Gaia and SIMBAD once, and adding additional catalogs will not slow down the code.
[TODO] add test function(s). E.g., negative coordinates, 0 search radius, too big/small search radius, too high/low magnitude limits, int vs. float for coords and search radius, degrees + hour angle argument compatibility
[TODO] use pytest framework and get it to pass.
[TODO] complete package setup and upload PyPI.
