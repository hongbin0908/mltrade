setname=sp500Top50
#setname=sp500Top50p
taname=base1
clsname=GBCv1n600md3lr001
clsname=RFCv1n2000md6
clsname=RFCv1n2000md6msl100
./main/yeod/yeod.py index_dow  -p1 || exit 1
./main/yeod/yeod.py ${setname}  -p1 || exit 1
