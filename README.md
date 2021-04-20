# SociaGrow

This Repo gives the insturctions to recreate the SociaGrow App. 
## The App is no longer being maintained due to changes to Instagram Policies. 
-----

## Description

Many people and bussineses join Instagram in the hopes of gathering many followers so that they could gather loyal costumers, increase their credibility and reduce their advertisement cost by posting their ads directly to their accounts. 

This is obviously not an easy task to do, and various methods are used to reach potential followers. One of the most effective methods is collaborating or following people that are in the same niche as you are. But finding these people is not an easy task and requires alot of time searching through Instagram. That's where the SociaGrow App comes in! 

After signing up for the app you can add ten different people that are in the same niche as you are and then you are done. Everyday in the homepage of the App new users are suggested to you and the type of interactions you need to do with them (Follow, Like, comment or shared posting). Follow the suggested actions and you will be growing your account in no time!

---

## How it works 

There are many different components in play to get the information from instagram, processed and then displayed on the App. Follow the instructions in each folder to see more explanation about that component and also so that you could rebuild the app for yourself:

1- DataBase builder : Before anything else is done we need to create a SQL database so that the data could be gathered and used for the different parts of the pipeline

2- Scraper Scripts: These scripts scrape Instagram (Public and business profiles only! For privacy private accouunts profiles are skipped by the scrapers) and gather information such as Bio, Number of Posts, Number of followings and Number of followers and sends them to the database. Also to find new people, the followings of people that are in the same niche as ours are scraped and added to database.

