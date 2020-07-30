# made-in-india
This full fledge project that scrapes data from Flipkart and displayes only Indian Products.

## Content
  - Overview
  - Prerequisites
  - Setting Up Your Machine
  - Installing Requirements
  - Starting Project
  - Screenshots
  - TO-DO
  
### Overview
As we all know the situation between India and China we also know that majority of online stores keep Chinese products.As our hectic daily schedule we don't have time to check the origin every product.So to overcome that problem here is a solution to it we provide the scraped data has an origin of India.
### Prerequisites 
1. Angular(FrontEnd) 
2. Python(BackEnd)
3. WebScrapping/Crawling 
4. Elastic Search
5. MySQL

### Setting Up Your Machine
1. [Python](https://www.python.org/downloads/) 

2. Elastic Search 
   1. Download elastic search from [here](https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.8.0-windows-x86_64.zip) 
   2. Download Java Version 8 and above from [here](https://www.oracle.com/java/technologies/javase-jdk14-downloads.html)
   3. Configure JAVA_HOME
      - This PC -> properties -> Advanced system settings -> Enviornment variable -> 
                  new -> Name: JAVA_HOME -> path C/ProgramFiles/Java/jdk folder name
      - add this in both user variable and system variable

   4. Unzip elastic search file
3. [Node JS](https://nodejs.org/en/)
4. Angular 
   1. Download/Clone the repo. and unzip it.
   2. Open Clients Folder after that open cmd in that directory.
   3. Write the following command in cmd to install Angular 
      '''
      npm i @angular/cli@latest
      '''
5. MySql
   1. Download from [here](https://dev.mysql.com/downloads/installer/)
   2. Use "Developer Default" setting while installing setup.
   3. Set make a table that contains the following columns.
      - Product_ID
      - Product_Name
      - Product_Price
      - Product_Highlights
      - Product_Rating
      - Product_Generic_Name
      - Product_Img_Url
      - Product_Link   
   3. Go to made-in-india/web-scrapper-tool/source/main_scrapper.py
      > On line no. 206 change the user name,password and database as per user   

### Installing Requirements
1. Activate the virtual Enviroment by running cmd in directory "../made-in-india/web-scrapper-tool/" by following command
   > webscappingenv\Scripts\activate
2. Install the Requirements file by following command based on which pip you are using:
   > pip install -r requirements.txt or pip3 install -r requirements.txt

### Starting Project
1. Start Elastic Search Server
   - Go to the unzipped elastic search folder
   - Double Click On elasticsearch.bat in following directory "..elasticsearch-7.8.0/bin/elasticsearch.bat"
   - To check weather it has started visit - "http://localhost:9200/"  
2. Start Node Server
   - Go to the folder that that conatins the download/cloned reop where you have installed angular.
   - Open cmd in following directory "..made-in-india/client/"
   - Type the following command to start node server
     > ng serve
3. Start API Service

>VISIT "http://localhost:4200/"
## Screenshots
<!--
<img src="https://user-images.githubusercontent.com/51474690/88975790-7707f300-d2d8-11ea-8260-f5f99ba08ddf.jpeg" align="left" height="500" width="300" >
<img src="https://user-images.githubusercontent.com/51474690/88976094-15945400-d2d9-11ea-86e7-f5451617c24f.jpeg" align="center" height="500" width="300" >
-->
This Basic Search Bar:
![Search](https://user-images.githubusercontent.com/51474690/88976094-15945400-d2d9-11ea-86e7-f5451617c24f.jpeg)
This Is how the Products are displayed after we have searched a product:
![product](https://user-images.githubusercontent.com/51474690/88975790-7707f300-d2d8-11ea-8260-f5f99ba08ddf.jpeg)



## TO-DO
- [ ] Scrape More Online Stores.

**If you encounter any issue while using code, feel free to contact me yadavyogesh9999@gmail.com or **

### Follow instruction for setup.
