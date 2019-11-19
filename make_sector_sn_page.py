import os
import glob
import sys
import re
import scipy as sp

def make_sector_sn_page(image_path):
    #assume the argument has the entire directory

    suse = os.path.basename(image_path)
    dout = 'content/pages/sn_' + suse
    if not os.path.isdir(dout):
        os.mkdir(dout)

    outfile = 'sn_' + suse+'.md'

    head_template='title: {sn} ({ntotal} total)\nslug: {slug}\nstatus: hidden\n'
    template = ''
    
    images = glob.glob(image_path + '/*')


    strtemplate = '![{}]({{filename}}../../{})\n'
    
    SNlist = sp.genfromtxt('SNlist',dtype=str)

    N = 0
    for image in images:
        obj_search = re.search('lc_(\w*)_',image)
        obj = obj_search.group(1)
        outpath = image.split('/')
        outpath = '/'.join(outpath[1:])

        if obj in SNlist:
            template += strtemplate.format(obj, outpath)
            N += 1

    template = head_template.format(sn=suse+ ' supernovae', ntotal=N,slug = suse+'-supernovae') + template
    with open(os.path.join(dout,outfile),'w') as fout:
        fout.write(template)
    return N
        
    
