setname=sp500Top50
#setname=sp500Top50p
taname=base1_ext4
clsname=GBCv1n600md3lr001
clsname=RFCv1n2000md6
./main/paper/paper.py  `./tool/model_name.py ${setname} ${taname} ${clsname}`  ${setname} ${taname}  --top=10000 --thresh=5000 || exit 1
clsname=GBCv1n600md3lr001
./main/paper/paper.py  `./tool/model_name.py ${setname} ${taname} ${clsname}`  ${setname} ${taname}  --top=10000 --thresh=5000 || exit 1
taname=base1_ext5
./main/paper/paper.py  `./tool/model_name.py ${setname} ${taname} ${clsname}`  ${setname} ${taname}  --top=10000 --thresh=5000 || exit 1
