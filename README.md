# LiveByte
An open-source light-based indoor positioning solution

# What is LiveByte?

LiveByte turns your smart bulbs like Philip Hue or LIFX to your indoor GPS satellites. Like GPS's method that infers device's location from the beacon signal of the GPS sattelites it can communicate, LiveByte infers location of your smart devices (mobiles, wearables) from the light-beacon broadcasted by your smart bulbs. To deploy LiveByte, you only need a small and cheap server like Raspherry Pi to host LiveByte server application to control your smart bulb, and LiveByte client application installed in your phone to communicate with your smart bulb via your device's camera and get your location. 

# How does it work?

With your phone in your palm, LightByte uses phone camera to detect the bulbs' ID and the distance to the bulbs. By leverage Visble Light Communication (VLC) technologies, each bulb's ID is encoded in form of light colors or light intensive that is invisible with human eye but be recognized by CMOS sensor of camera. The distance between bulbs and phone is estimated using the anger of arrival, the ratio between the size of ojects in the picture and the real size of objects.

-----------	  (wifi)  -------------------
[Pi server] <-------> [Phillip Hue Bulbs]
-----------			  -------------------
^^                          ^^
||                          ||
||(wifi)                    ||(Visible light communication) 
||                          ||
VV                          VV
[ phone/wearables with camera ]

This is a demo I made for the Raspherry Pi contest. 

[![ScreenShot](https://raw.github.com/GabLeRoux/WebMole/master/ressources/WebMole_Youtube_Video.png)](https://www.youtube.com/watch?v=WG8qRy8FAHE)

#Why do we use light bulb?

We believe light-based approach is the solution for three core challenges of indoor postitioning, namely, accuracy, robustness and ubiqutous distribution. Unlike wifi-based approach which is suffered with accuracy and robustness caused by the unreliability of wifi signal strength and unlike bluetooth-based approach which requires additional bluetooth broadcasters pre-deployed in the building resulting in huge cost of deploying and maintaining. Light-based approach uses computer vision to provide sub-meter accuracy without suffering from the inconsistence of wifi signal and, as light bulbs are the vital part of any building, it can also be considered as the most ubiquitous solution for indoor localization context.   

#Who we are?

This project is started by me and currently run by me only.


