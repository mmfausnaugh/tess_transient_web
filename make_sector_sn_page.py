import os
import glob
import sys
import re
import numpy as np

def make_sector_sn_page(image_path):
    #assume the argument has the entire directory

    suse = os.path.basename(image_path)
    dout = 'content/pages/sn_' + suse
    if not os.path.isdir(dout):
        os.mkdir(dout)

    outfile = 'sn_' + suse+'.md'

    head_template='title: {sn} ({ntotal} total)\nslug: {slug}\nstatus: hidden\n  Each figure has three panels.  The top panel shows the transient light curve, the middle panel shows the local background (estimated in an annulus), and the bottom panel shows a "background-model corrected" light curve. Details about the background model are in the [README]({{filename}}../README/README.md). \n \n The vertical red line marks the time of discovery reported to TNS. Other useful metadata from TNS is in the figure title.\n\n Note that the top and bottom panel are in magnitudes, while the middle panel is in differential flux units. The magnitudes are calibrated to the flux in the reference image used for image subtraction. Thus, flux from the host galaxy is included in these magnitudes. \n\n  3-sigma upper limits are plotted as triangles with no errorbars. A typical limiting magnitude is 19.6 in 30 minutes or 18.4 in 200 seconds (for low backgrounds).\n\nThe links allow you to download the light curve data as a text file. \n\nMore details in the [README]({{filename}}../README/README.md).\n\n\n'
    template = ''
    
    images = glob.glob(image_path + '/*')


    strtemplate = '[{}]({{static}}../..//{})\n![{}]({{static}}../../{})\n'
    
    SNlist = np.genfromtxt('SNlist',dtype=str)

    N = 0
    for image in images:
        obj_search = re.search('lc_(\w*)_',image)
        obj = obj_search.group(1)
        outpath = image.split('/')
        outpath = '/'.join(outpath[1:])

        datapath = outpath.replace('images','light_curves')
        datapath = datapath.replace('.png','')


        
        if obj in SNlist:
            template += strtemplate.format(obj,datapath,
                                           obj, outpath)
            N += 1

    template = head_template.format(sn=suse+ ' supernovae', ntotal=N,slug = suse+'-supernovae') + template
    with open(os.path.join(dout,outfile),'w') as fout:
        fout.write(template)
    return N
        
    
