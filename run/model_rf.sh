setname=sp500Top100
#taname=base1
taname=base1_ext3
clsname=RFCv1n600md8
./main/yeod/yeod.py index_dow  -p1 || exit 1
./main/yeod/yeod.py ${setname}  -p10 || exit 1
./main/ta/build.py ${setname} ${taname}  -p10 || exit 1
./main/model/model_work.py  ${setname} ${taname} ${clsname} || exit 1 
./main/paper/paper.py  `./tool/model_name.py ${setname} ${taname} ${clsname}`  ${setname} ${taname} --thresh=3000 || exit 1
