Program Description: Web Mapping - CA2
Authors: C21508813 Haroun Kassouri
Date: 23/11/2024
Website Link: booknest.cc

##################### Project Description #####################

This project is a web mapping application designed to provide a platform for users to search, view, and analyze spatial data, with a focus on book-related locations and information. The platform integrates a PostgreSQL/PostGIS database for spatial data storage and manipulation, allowing for handling of book-related geospatial information, such as bookstores and libraries. The platform integrates a PostgreSQL/PostGIS database for spatial data storage and manipulation, a Django-based backend to handle the Model-View-Controller (MVC) architecture. Mapping functionality is implemented using Leaflet JS with OpenStreetMap. The application is containerized using Docker for easy deployment and is hosted on the cloud provider DigitalOcean.


###################### Project Requirements ######################
Technologies (required)

Database: PostgreSQL with PostGIS
Middle tier(s): Django with Django REST Framework
Front-end: Progressive Web Application (PWA) and Android or iOS app developed in Cordova. You can use any framework you like for layout such as jQueryMobile, Ionic, Bootstrap etc.
Mapping: Leaflet JS with OpenStreetMap
Deployment (middle tier(s)): Any cloud provider. I suggest using Docker to create an image and deploy an instance of this. The back-end components of your app must be web-accessible or the front-end component will not work.

Technologies (optional)

Companion Django Admin website to your mobile application
Django REST Framework
Android or iOS app developed in Cordova
Client-side frameworks such as Angular, React etc.
Link to external API for additional data such as points of interest etc. OpenStreetMap's Overpass API is useful in this regard.
Cloud providers: Suggestions include but are not limited to Amazon AWS, Microsoft Azure, Digital Ocean, Okeanos.

Content

The idea is to build a full-stack application that has a location-based or mapping component. To this end, it is required to:

Create/store/manipulate spatial data, hence PostgreSQL/PostGIS
Create a middle layer based on the Model-View-Controller (MVC) pattern, hence Django.
Create a mobile application, deployable on any platform, hence PWA and, optionally, Cordova. 
Be deployed to the Cloud, hence, Docker and external provider for hosting.


###################### Sources ######################
I used many of these references to accomplish this project. Code from these sources was extremely helpful to both understanding the concept aswell as completing the project.
https://learndjango.com/tutorials/django-docker-and-postgresql-tutorial
https://docs.djangoproject.com/en/5.1/ref/models/querysets/#filter
https://docs.djangoproject.com/en/5.1/topics/pagination/
https://realpython.com/django-pagination/
https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch
https://simpleisbetterthancomplex.com/tutorial/2016/08/29/how-to-work-with-ajax-request-with-django.html
https://docs.djangoproject.com/en/5.1/ref/csrf/
