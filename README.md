# algotrade

## Overview
This script is to help users manage cryptocurrency account, visualize its data, and most importantly allow user to automate trade using various algorithm to make the most margin.
Currently developing algorithms is EMA/SMA and we are looking forward to implement other 
algorithms
## Prerequisites
### Package to install
General Packages
```
pip3 install pandas
pip3 install numpy
```
<br/>


Wrapper for Crypto Currency: https://github.com/ccxt/ccxt
```
pip3 install ccxt
```
<br/>


GUI
```
pip3 install pyqt5
pip3 install pyqtgraph
```
<br/>


Statistic Model
```
pip3 install statsmodels
```

## Run
```
python3 application.py
```
Once the program runs, a user can navigate their account information in account page.
<br>
![alt text](https://github.com/yjang43/algotrade/blob/master/img/img_01.png =250x "img not available")
<br>
With data visualization page, the user can look at current status of the cryptocurrency market,
and apply various algorithms to see which one is more accurate algorithm to apply for a certain market.
Currently, very basic of data visualization is supported.
<br>
![alt text](https://github.com/yjang43/algotrade/blob/master/img/img_02.png =250x "img not available")
<br>
Under auto trade page, user can choose an algorithm to start a session that automates
trading (limited up to five sessions). Currently, a supported algorithms are the followings:
<br>
* ema/sma

<br>
![alt text](https://github.com/yjang43/algotrade/blob/master/img/img_03.png =250x "img not available")
<br>
![alt text](https://github.com/yjang43/algotrade/blob/master/img/img_04.png =250x "img not available")
<br>

We are currently working on adding additional algorithm.

## Contact
We are happy to hear any feed back from you! If there is any improvement we can make, please
let us know.
<br/>
<br/>
Email: yjang43@wisc.edu
