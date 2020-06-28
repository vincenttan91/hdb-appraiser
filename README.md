# Project Title: Singapore Public Housing (HDB) Resale Price Prediction Model

### Problem Statement
Singapore has always had one of the most expensive housing market in the world, so it becomes crucial for the locals to make sure every dollar they spent are worthwhile. However, most of the housing price are still benchmarked manually by experienced appraiser today. Hence, it would really be helpful for home buyer if there is a predictive model available to find out any undervalued property listing and maximise their savings.

---

### Executive Summary
According to Forbes rich list in 2018, out of the 22 billionaires in Singapore, 16 of them are real-estate tycoons. The total fortune came up to a staggering $43.7 billion, which grew up to nearly 10 percent from the previous year (Channel News Asia, 2018). We cannot deny that all the successful real-estate investors have had either natural talent or decade-trained experience in them to tell a good or bad property listing or development project apart. Nevertheless, it would be fascinating if we could unravel and quantify the investors' - or ordinary home-buyer - judgement with the help of Data Science. So we set out a journey to create a machine learning model that could benchmark a property pricing based on its attributes.

In this project, we will develop a predictive model on HDB unit resale price using several machine learning techniques of different classes. We believe that a model like this would be very valuable for any real state agent or home-buyer to set a benchmark pricing to judge whether a property listing is over or under-valued.

One thing worth noting is that HDB-developed flats are in a highly controlled environment by the Government to avoid market speculation on housing price. In fact, investment in these flats is technically prohibited as one could only own a maximum of one HDB flat. However, this situation does not render our study and model useless, simply because of the fact that this project still serve as a window to look into home buyer's psychology and how premium is justifiable by numerical features or attributes. So the same methodology could still be applied to Condominium sales in Singapore or real estates in City States that resembles Singapore where some of the key features could still be applicable and worth researching.

The data dictionary below described that final data that were cleaned and selected from the data collection via various API calls and web-scraping from multiple sources:

|     Column Name     | Data Type |                                      Description                                     |
|:-------------------:|:---------:|:------------------------------------------------------------------------------------:|
|         town        |   object  |                HDB township where the flat is situated, eg. Queenstown               |
|      flat_type      |   object  |                  Type of the resale flat unit, eg. 3-room, Executive                 |
|     storey_range    |  integer  |                          Floor level of the resale flat unit                         |
|    floor_area_sqm   |  integer  |                  Floor area of the resale flat unit in square meter                  |
|      flat_model     |   object  |                HDB-model of the resale flat, eg. Standard, Mansionette               |
| lease_commence_date |  integer  |                   Commencement year of the flat unit 99-year lease                   |
|   remaining_lease   |  integer  |        Remaining lease of the flat unit in year as of the date of transaction        |
|     resale_price    |  integer  |           Resale Price recorded for the resale flat unit (Target Variable)           |
|      sold_year      |  integer  |                           Year of resale flat unit is sold                           |
|      sold_month     |  integer  |                           Month of resale flat unit is sold                          |
|       address       |   object  |                             Full Address of the flat unit                            |
|       latitude      |   float   |                               Latitude of the flat unit                              |
|      longitude      |   float   |                              Longitude of the flat unit                              |
|  raffles_place_dist |   float   |   Commuting time from flat unit to Raffles Place MRT in minutes by Public Transport  |
|    one_north_dist   |   float   |     Commuting time from flat unit to one-north MRT in minutes by Public Transport    |
|   jurong_east_dist  |   float   |    Commuting time from flat unit to Jurong East MRT in minutes by Public Transport   |
|     orchard_dist    |   float   |      Commuting time from flat unit to Orchard MRT in minutes by Public Transport     |
|     changi_dist     |   float   |  Commuting time from flat unit to Changi Airport MRT in minutes by Public Transport  |
| raffles_place_drive |   float   |       Commuting time from flat unit to Raffles Place MRT in minutes by Driving       |
|   one_north_drive   |   float   |         Commuting time from flat unit to one-north MRT in minutes by Driving         |
|  jurong_east_drive  |   float   |        Commuting time from flat unit to Jurong East MRT in minutes by Driving        |
|    orchard_drive    |   float   |          Commuting time from flat unit to Orchard MRT in minutes by Driving          |
|     changi_drive    |   float   |       Commuting time from flat unit to Changi Airport MRT in minutes by Driving      |
|       mrt_dist      |  integer  |                  Distance from flat unit to the nearest MRT in meter                 |
|     mrt_station     |   object  |                            Name of the nearest MRT Station                           |
|     near_bus_itc    |   binary  |       Whether there is a bus interchange within 500m radius from the flat unit       |
|     near_mrt_itc    |   binary  |       Whether there is a MRT interchange within 500m radius from the flat unit       |
|      bus_u300m      |  integer  |               Number of bus stops within 300m radius from the flat unit              |
|       bus_dist      |  integer  |               Distance from flat unit to the nearest bus stop in meter               |
|      mall_u1km      |  integer  |             Number of shopping malls within 1km radius from the flat unit            |
|      mall_dist      |  integer  |             Distance from flat unit to the nearest shopping mall in meter            |
|       pri_u1km      |  integer  |             Number of primary school within 1km radius from the flat unit            |
|       pri_u2km      |  integer  |             Number of primary school within 2km radius from the flat unit            |
|     pri_aff_u1km    |  integer  |    Number of primary school with affiliation within 1km radius from the flat unit    |
|     pri_aff_u2km    |  integer  |    Number of primary school with affiliation within 2km radius from the flat unit    |
|    pri_elite_u1km   |  integer  |         Number of top 20 primary school within 1km radius from the flat unit         |
|    pri_elite_u2km   |  integer  |         Number of top 20 primary school within 2km radius from the flat unit         |
|       sec_u1km      |  integer  |            Number of secondary school within 1km radius from the flat unit           |
|       sec_u2km      |  integer  |            Number of secondary school within 2km radius from the flat unit           |
|     sec_aff_u1km    |  integer  |   Number of secondary school with affiliation within 1km radius from the flat unit   |
|     sec_aff_u2km    |  integer  |   Number of secondary school with affiliation within 2km radius from the flat unit   |
|    sec_elite_u1km   |  integer  |        Number of top 20 secondary school within 1km radius from the flat unit        |
|    sec_elite_u2km   |  integer  |        Number of top 20 secondary school within 2km radius from the flat unit        |
|   dist_to_highway   |  integer  |            Nearest distance from flat unit to the closest highway in meter           |
|    dist_to_exits    |  integer  |      Nearest distance from flat unit to the closest highway exits/ramp in meter      |

Feature selection were carried out throughout the Exploratory Data Analysis (EDA) process as part of the strategy to eliminate visibly unnecessary or non-correlated features before the modelling attempt. The strategy aimed to clear out white noises when plotting a correlation heatmap to further amputate any collinear features from the dataset.

As for the predictive modelling, there are 3 major techniques that were used in the project: (1) **Linear Regression**, (2) **Tree-based Regressor** and (3) **Neural Network**. After the models have been optimised and assessed, a best model was chosen to be exported for the deployment of a web application.

---

### Conclusion/Recommendation

In all, we have successfully developed and deployed a machine learning model to predict the pricing of resale HDB flats in Singapore. The accuracy was even up to 95% with the use of Random Forest Regressor. We have also found that the key indicators for price prediction are actually Floor Area, Remaining Year Lease, Storey Range and the Township where the property is situated. However, if we were to take away the effect of Township, we would still be able to explain some of its variance with the help of commuting time from the CBD, one-north and Changi airport.

There are several property that cost more than 600,000 SGD were being undervalued significantly with the prediction from the final model. There are definitely limitation to the final model as resale flat might come in different furnishing level, or condition of the house might vary across a wide range too. There is no way to find out about the house condition during the transaction and thus it is unable to capture one of the most critical factor in property pricing. Nevertheless, for most part, the model is extremely accurate, up to 23,012 SGD as inferred by the Mean Absolute Error of the final deployable model.

Although HDB-developed flats are in a highly controlled environment where investment would only yield unexciting profit, this project still serve as a window to look into home buyer's psychology and how premium is justifiable by numerical features or attributes. Hence the same methodology could still be applied to Condominium sales in Singapore or real estates in City States that resembles Singapore where some of the key features could still be applicable and worth researching.

To access the web application that was developed using the final model we created through the project, please visit https://hdb-appraiser.herokuapp.com.
