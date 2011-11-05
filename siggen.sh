TIME=`date +%s`
key=YOURKEY
secret=YOURSECRET

allconcat="${key}${secret}${TIME}"
echo $allconcat
md5 -s "$allconcat"
