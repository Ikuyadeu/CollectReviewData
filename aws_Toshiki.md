# Memo for Ubuntu

## Send the File by ssh
```sh
scp -i ~/.ssh/research1.pem ~/Desktop/gm_openstack.csv.zip ubuntu@[IP address]:~/CollectReviewData
```

## Connect by ssh
```sh
ssh -i ~/.ssh/research1.pem ubuntu@[IP address]
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

## Some Setting-Up
```sh
sudo apt-get install python
sudo apt-get install python-minimal
sudo apt-get install python-requests
```

## Run Python
```sh
mkdir revision_files
time python src/RequestFileDiffBase.py gm_openstack https://review.openstack.org _START_ _END_
```

## Get the file by ssh
```sh
scp -i initialkey.pem ubuntu@ec2-user@host:send_file_path.zip .
```
