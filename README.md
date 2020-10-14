# web scrapper for flipkart
This full fledge project that scrapes data from Flipkart and displayes only Indian Products.

## Content
  - Overview
  - Prerequisites
  - Setting Up Your Machine
  - Creating and Activating Virtual Environment
  - Installing python packages
  - Installing Requirements
  - Starting Project
  - Screenshots
  - TO-DO
  - Extra
  
### Overview
As we all know that there is a current conflict between India and China. The majority of online stores keep an enormous quantity of Chinese products. As an Indian, we should avoid buying Chinese products. While everyone engaged in their daily hectic schedule no one has time to check the origin of the country for each product. So here we offer a unique solution to that. Our website scrapes the real-time data from Flipkart and displays only the products that have been originated from India. 

### Prerequisites 
1. Angular(FrontEnd) 
2. Python(BackEnd)
3. Selenium(WebScrapping/Crawling) 
4. Elastic Search
5. MySQL

### Setting Up Your Machine
1. Download python From [here](https://www.python.org/downloads/).
2. Elastic Search 
   1. Download elastic search from [here](https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.8.0-windows-x86_64.zip).
   2. Download Java Version 8 and above from [here](https://www.oracle.com/java/technologies/javase-jdk14-downloads.html).
   3. Configure JAVA_HOME
      - This PC -> properties -> Advanced system settings -> Enviornment variable -> System Variable -> New 
                  Name: JAVA_HOME
                  Path: C:/ProgramFiles/Java/jdk folder name

   4. Unzip elastic search file
3. Download Node from [here](https://nodejs.org/en/).
4. Angular 
   1. Download/Clone the repo. and unzip it.
   2. Open Clients Folder after that open cmd in that directory.
   3. Write the following command in cmd to install Angular 
      > npm i @angular/cli@latest
   4. To install packages simply run
      > npm i
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
   3. Go to directory:  "./made-in-india/web-scrapper-tool/source/main_scrapper.py"
      > On line no. 206 change the user name, password and database as per user   
      
### Creating and Activating Virtual Environment
- Open Command prompt and run 
  > py -m pip install --user virtualenv
- Now Create You Virtual Environment, Go to directory "./web-scrapper-tool/" and run
  > py -m venv webscrappingenv
- To Activate it run
  > .\webscrappingenv\Scripts\activate
  
### Installing python packages
- Install the Requirements file ("./web-scrapper-tool/requirement.txt") by following command based on which pip you are using:
   > pip install -r requirements.txt or pip3 install -r requirements.txt
   
### Starting Project
1. Start Elastic Search Server
   - Go to the unzipped elastic search folder
   - open elasticsearch.bat("./elasticsearch-7.8.0/bin/elasticsearch.bat")
   - To check weather it has started visit
    > http://localhost:9200/
2. Start Node Server
   - Go to the folder that that conatins the download/cloned reop where you have installed angular.
   - Open cmd in following directory : "./client/"
   - Type the following command to start node server
     > ng serve
3. Start API Service
   - Activate virtual environment and go to directory "./web-scrapper-tool/source/" and run
     > python api_controller.py
> VISIT http://localhost:4200/

### Screenshots
This Basic Search Bar:
![Search](https://user-images.githubusercontent.com/51474690/88976094-15945400-d2d9-11ea-86e7-f5451617c24f.jpeg)
This is how the Products are displayed after we have searched a product:
![product](https://user-images.githubusercontent.com/51474690/88975790-7707f300-d2d8-11ea-8260-f5f99ba08ddf.jpeg)

### TO-DO
- [ ] Scrape More Online Stores.
- [ ] Parallel Scrapping.

### Extra
- To view how we are scrapping, Go to "./web-scrapper-tool/source/main_scrapper.py" and comment line no. 207 and 208.

**If you encounter any issue and have any suggestion while using code, feel free to contact on yadavyogesh9999@gmail.com or tapan.vach025@gmail.com**
