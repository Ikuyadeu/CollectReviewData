head -1 gm_openstack.csv  > head.txt
cat gm_openstack.csv | grep .py  > gm_openstack_r.csv
cat head.txt gm_openstack_r.csv > gm_openstack_s.csv