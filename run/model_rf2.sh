setname=sp500Top50
taname=base3
#taname=base1_cdl
clsname=RFCv1n600md8
./main/yeod/yeod.py index_dow  -p1
./main/yeod/yeod.py ${setname}  -p10
./main/ta/build.py ${setname} ${taname}  -p10
./main/model/model_work.py  ${setname} ${taname} ${clsname} --sw=linear --start='1970-01-01'
./main/paper/paper.py  `./tool/model_name.py ${setname} ${taname} ${clsname} --sw=linear --start='1970-01-01'`  ${setname} ${taname} --thresh=800
