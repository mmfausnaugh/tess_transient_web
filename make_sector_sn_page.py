import os
import glob
import sys
import re
import scipy as sp

#assume the argument has the entire directory
image_path = sys.argv[1]

suse = os.path.basename(image_path)
dout = 'content/pages/sn_' + suse
if not os.path.isdir(dout):
    os.mkdir(dout)

outfile = 'sn_' + suse+'.md'

template='title: {}\nstatus: hidden\n'.format(suse+ ' supernovae')


images = glob.glob(image_path + '/*')


strtemplate = '![{}]({{filename}}../../{})\n'

SNlist = sp.genfromtxt('SNlist',dtype=str)

for image in images:
    obj_search = re.search('lc_(\w*)_',image)
    obj = obj_search.group(1)
    outpath = image.split('/')
    outpath = '/'.join(outpath[1:])

    if obj in SNlist:
        template += strtemplate.format(obj, outpath)


#print(template)
with open(os.path.join(dout,outfile),'w') as fout:
    fout.write(template)

    
