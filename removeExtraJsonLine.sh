for fname in json/gm_openstack/*/*.json; do
echo $fname
sed -i -e '1d' $fname;
rm ${fname}-e
done
