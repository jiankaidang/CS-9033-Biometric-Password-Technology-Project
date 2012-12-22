Mobile Application Programming

CS 9033 FALL 2012

SignPass

Maneli Kadkhodazadeh

Changpeng Li

Jiankai Dang (Team Leader)

Yang Li

With our application, we seek to re-create the benefits of the in-person signature to replace complex and insecure username/password combinations. The application will allow users to login easily to their bank accounts simply and quickly using a touch-signature or touch-phrase.

Our system has three major components: iOS Application, Back-End Server, and Bank Services.


iOS Application

 Training of user’s signature

 Sign and Tap Login

 Access bank account through signature


Back-End Server

 Save the training signature data from iOS App to server database

 Recognize and match signature data between iOS App and server database

 Observe and handle the login event from bank service

 Return the user authentication results to bank server


Bank Services

 Provide login interface for user

 Dispatch login event to Back-End Server

 Receive the user authentication results from Back-End server and inform user about it

System Software Architecture

 iOS Application (Client Side) -- Objective-C

 Back-End Software Program (Server Side) -- Python, Django, SQL

 Bank Services (third-party software, including Bank website and Bank Server software program) -- Python, HTML, JavaScript, CSS
