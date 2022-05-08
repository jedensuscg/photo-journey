import piexif
from PIL import Image


image = Image.open('images/amelia1.jpg')
exif_dict = piexif.load(image.info["exif"])
gps_ifd = {
        piexif.GPSIFD.GPSLatitudeRef: "N",
        piexif.GPSIFD.GPSLatitude: ((36,1),(51,1),(28,1000)),
        piexif.GPSIFD.GPSLongitudeRef: "W",
        piexif.GPSIFD.GPSLongitude: ((76,1),(12,1),(1,12000)),
        piexif.GPSIFD.GPSAltitudeRef: 1,
        piexif.GPSIFD.GPSAltitude: (76,1),
    }
#add TRY block

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
