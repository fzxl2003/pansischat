
import hashlib

deomo_val = 'k213ngines'
md5_val = hashlib.md5(deomo_val.encode('utf8')).hexdigest()
print ('src_val : %s \nmd5_val : %s' % (deomo_val,md5_val))