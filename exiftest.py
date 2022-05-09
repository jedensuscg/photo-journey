import piexif
from PIL import Image
import math
from fractions import Fraction

coord_to_test = [36.857912892884606, -76.20338127791958]

def decimalCoordToRational(coords, altitude = 100):
    #Initialize lists and references
    latRef = 'N'
    longRef = 'E'
    altRef = 1
    hours = []
    minutes = []
    seconds = []

    #iterate through lat and long and separate into each into a tuple of rational numbers for D, M, S
    for i in range(2):
        hours.append(math.modf(coords[i]))
        minutes.append(math.modf(abs(hours[i][0] * 60)))
        seconds.append(minutes[i][0] * 60)

    #Convert Seconds and altitude into fraction.
    latSecondsFraction = Fraction(seconds[0]).limit_denominator()
    longSecondsFraction = Fraction(seconds[1]).limit_denominator()
    altitudeFraction = Fraction(altitude).limit_denominator()

    #Build the tuple that holds the full lat and long
    rationalLat = ((abs(int(hours[0][1])), 1),(int(minutes[0][1]), 1),(latSecondsFraction.numerator, latSecondsFraction.denominator))
    rationalLong =  ((abs(int(hours[1][1])), 1),(int(minutes[1][1]), 1),(longSecondsFraction.numerator, longSecondsFraction.denominator))

    #Determine N/S and E/W reference of coordinate based on it's sign.
    if hours[0][1] < 0:
        latRef = "S"
    if hours[1][1] < 0:
        longRef = "W"

    #Determine altitude reference (0 or below sea level, 1 for above)
    if altitude < 0:
        altRef = 0

    #build altitude tuple
    rationalAltitude = (altitudeFraction.numerator, altitudeFraction.denominator)

    # print(hours)
    # print(minutes)
    # for i in seconds:
    #     print(Fraction(i).limit_denominator())

    # print(f'Lat: {latRef}{int(hours[0][1])}:{int(minutes[0][1])}:{round(seconds[0], 4)}')
    # print(f'Long: {longRef}{abs(int(hours[1][1]))}:{int(minutes[1][1])}:{round(seconds[1], 4)}')



    print(rationalLat)
    print(rationalLong)
    #build entire GPS IFD
    gps_ifd = (latRef,rationalLat,longRef,rationalLong,altRef,rationalAltitude)
    return gps_ifd


testData = decimalCoordToRational(coord_to_test)

image = Image.open('images/amelia1.jpg')
exif_dict = piexif.load(image.info["exif"])
gps_ifd = {
        piexif.GPSIFD.GPSLatitudeRef: testData[0],
        piexif.GPSIFD.GPSLatitude: testData[1],
        piexif.GPSIFD.GPSLongitudeRef: testData[2],
        piexif.GPSIFD.GPSLongitude: testData[3],
        piexif.GPSIFD.GPSAltitudeRef: testData[4],
        piexif.GPSIFD.GPSAltitude: testData[5],
    }

exif_dict["GPS"] = gps_ifd 

try:
    exif_bytes = piexif.dump(exif_dict)
except:
    del exif_dict["1st"]
    del exif_dict["thumbnail"]
    exif_bytes = piexif.dump(exif_dict)


exif_dict["GPS"] = gps_ifd 
exif_dict


image.save('images/ameliaGPS.jpg', "jpeg",exif=exif_bytes)
