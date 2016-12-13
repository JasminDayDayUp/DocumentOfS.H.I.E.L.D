
#Classified Documents of S.H.I.E.L.D.

![1](https://cloud.githubusercontent.com/assets/15006855/21127256/926e5a46-c0bf-11e6-96c1-81d3282f89fc.png)

   I.COMSE 4111 Introduction to Database PROJECT

Contributor: Jingtao Zhu & Shengtong Zhang
A website provides an interface for S.H.I.E.L.D fans to interact with the database, making addition and queries

   II.Inspiration: 
                  
Fascinated by TV drama- Agents of S.H.I.E.L.D's magical plot and supernatural elements, we are inspired to build this application to provide Marvel fans with a brand new prospective of this TV show. 

   III. Function: 
                  
·If we ask users to input a S.H.I.E.L.D/HYDRA/Inhuman member’s name, our application will return his/her detailed profile and recommend users to view missions the character involved in/relationships with others(friends, enemies, lovers)/facilities he/she owns. 
·When users inputs name of a mission, they will get the detailed information about the mission and all the characters involved. 
·Moreover, by searching the name of "valuable items”(for example: mystery crystal),  users can get related characters and missions  information. 

   IV. Structure: 
We have seven entities including: detailed profile of members of S.H.I.E.L.D;profile of core members of HYDRA; profile of Inhumans appeared in TV show; significant events and missions; facilities which S.H.I.E.L.D members own(Queen-Jet; bio-chemistry laboratory; convertible car...) valuable items appeared(Great stone; mystery crystal… ); duties of agents of S.H.I.E.L.D. 

![1](https://cloud.githubusercontent.com/assets/15006855/21127166/df510828-c0be-11e6-80b8-57b3bf38edf6.png)

   V.Insterest & Challenges 
The inhuman and supernatural elements extracted from TV show makes this application more vivid and interesting. Due to its complex characters relationships and plots, we are to design a more intuitive and beautiful UI.


**********************************************************************************************************

The URL of the web application:
    http://40.117.35.158:8111


Implemented:
1. Users can input S.H.I.E.L.D/HYDRA/Inhuman member’s name, our application will return his/her detailed profile and recommend users to view missions the character involved in/relationships with others(friends, enemies, lovers)/facilities he/she owns.
2. When users inputs name of a mission, they will get the detailed information about the mission and all the characters involved.
3. Moreover, by searching the name of "valuable items”(for example: mystery crystal), users can get related missions information.


New Feature:
1. We add two different type of users, one is admin, the other is client.
2. We let admin add the new example of entity and relationship into our databases.
3. We let client input the query sql to get the information they want, but they could not add new tables or insert new examples.


**********************************************************************************************************

Two of the web pages that require the most interesting database operations.

1. Login.html
This page is used for admin to add new example of entity and relationship.
Inputs on the page are used as the new example’s attributes to produce databases operations that insert a new complete example. It is useful and necessary for admin to manage the databases.

2. query.html
This page is used for clients to query and search the databases. 
In query part, clients could input the sql sentence to get the result what they want. The input is sql sentence, and the databases use sql to get the result the client want. But the input could not be “CREATE …” or “INSERT …”. 
In search part, clients could input the ID or name of characters or missions or items, the system will give the users the related information. The end change the input word to sql sentence to get the information from the databases.


**********************************************************************************************************

Three interesting SQL queries over the database, with a sentence or two per query explaining what the query is supposed to compute.

(1)
w4111=> SELECT AVG(S.SAge)
w4111-> FROM SHIELDMember S, Participate1 P1, Mission M
w4111-> WHERE S.SID = P1.SID AND P1.MID = 'M01' AND M.MID = 'M01'
w4111-> \g
avg         

 32.3000000000000000
(1 row)

Output the average age of SHIELD who participated the Mission ‘MID’.

(2)
w4111=> SELECT DISTINCT F.FName
w4111-> FROM Facility F, BelongsTo B, SHIELDMember S, Participate1 P1, Mission M, Appearance A, ValuableItem V
w4111-> WHERE F.FID = B.FID AND B.SID = S.SID AND P1.SID = S.SID AND M.MID = P1.MID AND M.MID = A.MID AND A.VID = V.VID AND V.VName = 'The Terrigen Crystals'
w4111-> \g
fname                  

 The Guest House
 Incapacitating Cartridge Emitting Rifle
 Bus
 Toolbox
 The Fridge
 The Slingshot
 The Playgroud
 Lola
(8 rows)
Ouput the Facilities used by the heroes who participate the mission where ValuableItem ‘The Terrigen Crystals’ Appears.


(3)
w4111=> SELECT S.SName
w4111-> FROM Mission M, SHIELDMember S RIGHT OUTER JOIN Participate1 P1 ON S.SID = P1.SID
w4111-> WHERE P1.MID = 'M02' AND M.MID = 'M02'
w4111-> \g
sname     

 Phil Coulson
 Melinda
 Grant Ward
 Daisy Johnson
(4 rows)

Outpot SHIELD Member’s names who participated in the Mission ‘M01’.
