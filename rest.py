__author__ = 'walter'
import owncloud
import owncloudadmin

oc = owncloudadmin.Client('http://owncloud.gis3w.it/owncloud','admin01', 'kote@25#t',debug=True)
print oc.getUser('walter')


