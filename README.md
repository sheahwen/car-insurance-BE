# Pay-per-km Insurance App
Deployed on: 
https://insur-km.netlify.app/ (Frontend)
https://km-insur-heroku.herokuapp.com/ (Backend)


## Idea
Pay-per-km Insurance App is a platform for users to sign up for pay-per-km car insurance contracts. It is based on a relatively new auto insurance model where the insurance premium is calculated based on real time data and driving habits, thus bringing more fairness to customers. For example customers pay $30 fixed monthly fee + $0.03/km variable fee. 

## Features and Technologies
#### Stack - PDRN (Postgresql, Django, React, NodeJs)

#### Mini calculator
This app features a mini calculator with slider for visitors' quick computation. 

#### Singpass Integration
**OAuth2.0** is implemented to retrieve data from mock Singpass API and pre-fill user sign up form (as shown in the clip below). However, this feature is not available on live site currently.

https://user-images.githubusercontent.com/25454526/154534377-36f3830a-b854-4847-89d5-f34b40ccd390.mp4

#### User Authentication
User authentication for this app is handled by **Django SimpleJWT**. 

#### User dashboard
Upon successful log in, users will have access to dashboard that shows outstanding balance to be paid, month-to-date distance travelled and estimated premium for current month. For more visual insights, it includes **charts created by Rechart.js** on distance travelled aggregated daily or monthly.

#### Admin Approval
An admin dashboard is created via Django admin site to allow admin to oversee contract applications and approve. A demo of the site is available at https://km-insur-heroku.herokuapp.com/admin/ (email: admin@projectfour.com | password: example) 

#### Scheduler
To simulate generation and record of actual distance travelled, **advanced python scheduler** is used to generate random mileage for all active contracts at 12am everyday. 

## Database Design
![drawSQL-export-2022-02-18_01_35](https://user-images.githubusercontent.com/25454526/154538594-d9ac5624-d274-4e17-b0c1-263de12328ce.png)
