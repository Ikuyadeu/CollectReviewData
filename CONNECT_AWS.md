# Memo for Ubuntu

## Send the File by ssh
```sh
scp -i ../forAWS/initialkey.pem gm_openstack.csv.zip ubuntu@ecxxx.xxxxxx.compute.amazonaws.com:~/
```

## Connect by ssh
```sh
ssh -i ../forAWS/initialkey.pem ubuntu@ecxxx.xxxxxx.compute.amazonaws.com
```

## Clone Git
```sh
git clone https://github.com/Ikuyadeu/CollectReviewData.git
cd CollectReviewData
```

## Unzip database csv
```sh
mv ../gm_openstack.csv.zip .
sudo apt install unzip
unzip ./gm_openstack.csv.zip
rm ./gm_openstack.csv.zip
```

## Run Python
```sh
mkdir revision_files
python3 src/RequestFileDiff.py gm_openstack https://review.openstack.org start end --from-ini
```

## Compress files
```sh
sudo apt install zip
cd revision_files
zip gm_openstackstart_end -r gm_openstack
mv gm_openstackstart_end.zip ~
```

## Get the file by ssh
```sh
exit
scp -i initialkey.pem ubuntu@ec2-user@host:~/gm_openstackstart_end.zip .
```

## Note
* 200000ファイルを取得するのに約２日(インスタンスはt2mediumだが，t2microでもあまり早さは変わらない)
* ファイル容量は7GB後半(圧縮すれば800MB前後)