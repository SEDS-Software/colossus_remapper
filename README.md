# colossus_remapper

This uses the config file to remap over certain columns in the data csv given

EX: if you had data.csv and you wanted to remap all values with the header PT-N2-220 from volts to PSI with this mapping `(data - .5) * 350` PSI you would change one of the config lines to say `PT-N2-220,700,-0.5,PSI`.  

You put in each row of the config file the header, the scale, the offset applied before the scaling and then finally the unit.