import os
import glob
import sys
import re


def make_sector_page(image_path):
    #assume this has the entire directory
    suse = os.path.basename(image_path)

    if not os.path.isdir('content/pages/' + suse):
        os.mkdir('content/pages/' + suse)

    outfile = suse+'.md'

    template='title: {}\nstatus: hidden\n'.format('all transients in ' + suse)


    images = glob.glob(image_path + '/*')


    strtemplate = '![{}]({{filename}}../../{})\n'

    N = 0
    for image in images:
        obj_search = re.search('lc_(\w*)_',image)
        obj = obj_search.group(1)
        outpath = image.split('/')
        outpath = '/'.join(outpath[1:])
    
        template += strtemplate.format(obj, outpath)
        N += 1

    #print(template)
    with open(os.path.join('content/pages',suse,outfile),'w') as fout:
        fout.write(template)

    return N
