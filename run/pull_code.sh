#!/bin/sh
############################
#@author hongbin@youzan.com
#@date
#@desc TODO
############################
export PATH=/usr/bin:$PATH
export SCRIPT_PATH=`dirname $(readlink -f $0)` # get the path of the script
pushd . > /dev/null
cd "$SCRIPT_PATH"/../

last_date=`python2.7 -c "import main.base as base; print base.last_trade_date()"`
ta=base1_top29_s1
eod=sp500Top100
batch=50
model=GBCv1n600md3lr001-${ta}-sp500Top100-${batch}-label5-1700-01-01-2009-12-31-0-0
 
rsync -avr --exclude=".git" main hongbin@login1.qima-inc.com:~/pytrade/ 
popd  > /dev/null # return the directory orignal
