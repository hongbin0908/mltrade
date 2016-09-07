setname=sp500
taname=base1_with_stable_phase1
clsname=RFCv1n2000md6msl1000
./main/yeod/yeod.py index_dow  -p1 || exit 1
./main/yeod/yeod.py ${setname}  -p10 || exit 1
./main/ta/build.py ${setname} ${taname}  -p10 || exit 1
./main/model/model_work.py  ${setname} ${taname} ${clsname} || exit 1 
./main/paper/paper.py  `./tool/model_name.py ${setname} ${taname} ${clsname}`  ${setname} ${taname}  --top=10 --thresh=3000 || exit 1
./main/pred/pred_b.py  `./tool/model_name.py ${setname} ${taname} ${clsname}`  ${setname} ${taname} || exit 1

setname=sp500R0T50
taname=base1_ext4_e1
clsname=RFCv1n2000md6msl1000
./main/yeod/yeod.py index_dow  -p1 || exit 1
./main/yeod/yeod.py ${setname}  -p10 || exit 1
./main/ta/build.py ${setname} ${taname}  -p10 || exit 1
./main/model/model_work.py  ${setname} ${taname} ${clsname} || exit 1 
./main/paper/paper.py  `./tool/model_name.py ${setname} ${taname} ${clsname}`  ${setname} ${taname}  --top=10 --thresh=3000 || exit 1
./main/pred/pred_b.py  `./tool/model_name.py ${setname} ${taname} ${clsname}`  ${setname} ${taname} || exit 1
