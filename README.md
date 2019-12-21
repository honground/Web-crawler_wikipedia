# Web-crawler_wikipedia
Python codes to crawl Wikipedia articles in the network format

***

Description
-----------
This code 1)takes the title of seed Wikipedia page of interest and the time period of interest; 2)crawls the Wikipedia articles linked with the seed page; and 3)generates the network with the collected page

The following figure shows the architecture of the network.

![image](./wiki.png)

Usage
-------------
As an input, the user can input the title of seed page of interest, time period of interest, and the number of steps to crawl.
For instance, you can crawl the Wikipedia articles directly linked with the seed page (Set 1 pages), the articles directly linked with the Set 1 pages (Set 2 pages), and so on.


  1. Example of the output ("Ajax(Programming language)" as the seed page) is presented
  2. The network drawn with the Gephi is also presented

Prerequisites
-------------
1. Python (the codes in this repository are developed using Python verison 3.6.6)
2. You need several external packages, and they are mentioned in the python file.



