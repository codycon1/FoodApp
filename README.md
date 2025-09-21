# FoodApp
A Django web application for small independent food delivery

This document outlines the design patterns and functions used in the GunniGrub website. This document is for internal use only.

***
#Stack Design

###Website backend
Python Django

###Web Server
Google Cloud hosted VM instance - ubuntu server 
Partial LAMPP stack - Apache2, MySQL

###Integrations
Google Distance Matrix API - Distance calculation
Google Secret Manager API - API Key Management
Google Places API - Used in conjunction with Distance Matrix API
Twilio - Text notifications
Stripe - Payment processing
Sentry - Issue Tracking / Debug info

###Front end
HTML5
Bootstrap 4
Minimal Javascript

***
#Database Schema

##StandardUser - Generic user class with profile information
    Email
    Region - User’s delivery region
    Address - User’s primary address
    Address2 - User’s unit number (not used in distance calculations)
    Zipcode
    Phone
    PremiumValidDate - User’s premium subscription end date (1/1/1999 if never purchased)
    Driver - Y/N Allows access to driver panel
    Manager - Y/N Allows access to admin site

##Region - Properties for each delivery region
    Name
    Code - 3 character shorthand code (Denver = DEN, Colorado Springs = SPR)
    Zip
    Active - Allows for quick switching of an active region
    WinterStatus - Quick switching of winter delivery rates when roads are icy
    (Rates)
    baseCharge(+- [Winter], [Member]) - Delivery fee
    deliveryRadius(+- [Winter], [Member]) - Radius before mileage is applied
    deliveryRate(+- [Winter], [Member]) - Dollars / mile outside of free radius

##Restaurant - Specific restaurant info
    Name
    Website (URL)
    Menu (URL)
    Address
    Phone
    Region (Foreign Key)
    placeID - Used in conjunction with distance matrix API generated on demand with Google Places API
    Active (Y/N)

##Order - Order details
    customerID (Foreign key) - FK to customer’s DB entry
    restaurantID (Foreign key) - FK to restaurant
    Region (Foreign key) - FK to region (utility entry to avoid order->restaurant->region)
    Phone - Customer’s contact number (receipt purposes)
    datePlaced - Date order was placed
    timePlaced - Time order was placed
    dateDelivery - Pickup time
    timeDelivery - Pickup time
    Name - Restaurant name
    deliveryAddress - Customer’s address 
    specialRequests - Requests entered by customer
    Status - (pending, placed, accepted, picked up, complete)

***
