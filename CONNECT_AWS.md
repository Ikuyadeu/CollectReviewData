Send the File by ssh
```sh
scp -i XXX.pem send_file_path.zip ubuntu@ecxxx.xxxxxx.compute.amazonaws.com:/~
```

Connect by ssh
```
ssh -i XXX.pem ubuntu@ecxxx.xxxxxx.compute.amazonaws.com
```

Get the file by ssh
```
scp -i XXX.pem ubuntu@ec2-user@host:send_file_path.zip .
```
