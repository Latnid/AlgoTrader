# Algotrader (Trader assistant tool)
This tool is created inorder to assist advanced traders with mature strategies. Which including long term trend and short term trade management. With this tool, traders can have a settle mindset and prediction of future and able to plan for the strategies. With a mature strategy, this tool can stand watch for traders. Thanks to the hard work and free data API providers, this tool can provide realtime data collection,realtime data analysis, and realtime trade signal monitoring. This tool has utilized Prophet, SVM,Logistic Regression and LTSM combined with technical indicators and cash flow as analyzing methods. Base on a local PostgreSql server, this tool have been tested runing over 24 hours non stop. Last but not least, this tool is not only support for stocks market and also fit for crypto market. Since crtpto market opens 24 hours a day, most of the realtime data realted function was test under crypto.

# features
* Realtime data collection
  
    RTstream : Realtime API, get realtime stock bar from alpaca.

    RTdata : pull data from local PostgreSql realtime database, and return clean dataframe.

    RTstock: fast way acquire stock bar,quote and trades at the same time and insert them into local PostgreSql realtime database.

    RTcrypto: the same as RTstock but in crypto.

    ![RTSHOW](Data/RTshow.gif)

* History data collection
* 
    Authorization: Onestep api access authorized way, can switch between data only or trading access.

    CleanData: Onestep cleandata and tranfer timezone as same as wallstreet(America/NewYork)

    ![CleanData](Data/CleanData.png)

* Database
    ConnectDB: Onestep connect to local PostgreSql database. 

* virtualization
    Dash: dispaly realtime data and chart as a webpage
* Trade
    indicators: Onestep indicators calculator,return combined dataframe.
    Trade: Onestep go long or short bracket orders placer
    Signal: realtime data monitoring with pre set strategies.
    Backtest: strategy filled with history data, strategy evaluator(Logistic Regression created in 'daytrade_models folder' ,can use as a entry point condition checker)

*  Analysis and Machine Learning included
  
    LSTM: connect long term history and trained a module for long term price prediction purpose.(module save in 'lstm_models' folder)

    ![LSTM](Data/LSTM.png)

    ML_SVM: Input daily high and low data,trained a module to predict daily high and low purpose.

    ![SVM](Data/SVM.png)
    
    prophet: timeseries price predication,next day chart protection.

    ![SVM](Data/Prophet.png)
    
    LvsS: history or realtime data bullish or bearlish money flow comparation tool. (can use as a entry point condition checker)
    
    ![SVM](Data/LvsS.png)

---

Installation Guide

Install the app's dependencies first. Refer to the imported libraries. For example: use 'pip install'as follow:

```
  pip install pandas
  pip install hvplot
  pip install sklearn
  pip install Dash

```
---

# Useage

Download all the requirement data and creat local postgresql database

Run the any .ipynb with jupyter notebook or jupyter lab.

use command line to run any .py files


```

---

## Contributors

FinTech Team
Dash - Scott


---

## License

[MIT](https://choosealicense.com/licenses/mit/)
  
  
