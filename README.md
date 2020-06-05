# USPSZoneCalculator
A Python script that calculates shipping zones based on zip codes of origination/destination and parcel weight for First Class mail by scraping HTML from USPS shipping API. Input is a csv file containing column of zip codes and output is a csv file containing the zip codes and their corresponding zones and commercial rates.
# Note: 
Sometimes Excel-->csv conversion removes formatting and leading zeroes are lost. The script will automatically add 0's to zip codes containing less than 5 digits. 
