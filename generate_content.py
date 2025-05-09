import os
import glob
import re

from make_sector_page import make_sector_page
from make_sector_sn_page import make_sector_sn_page

idirs = glob.glob('content/images/*')
idirs.sort()

cell_fmt = '[{}]({{filename}}../{})'
line_fmt = '|{}|{}|\n'

sn_out = 'title: Supernovae ({} total)\nSlug: supernovae\npageorder: 2\n \nClick on the sector you are interested in to see the transients that TESS observed.\n\n '

at_out = 'title: All Astrophysical Transients  ({} total)\nSlug:all-astrophysical-transients\npageorder: 1\n\nClick on the sector you are interested in to see the transients that TESS observed.\n \n '

#primary mission
year1 = ['01','02','03','04','05','06','07','08','09','10','11','12','13']
year2 = ['14','15','16','17','18','19','20','21','22','23','24','25','26']

#em1
year3 = ['27','28','29','30','31','32','33','34','35','36','37','38','39']
year4 = ['40','41','42','43','44','45','46','47','48','49','50','51','52']
extra_year4 = ['53','54','55']

year5 = ['56','57','58','59','60','61','62','63','64','65','66','67','68','69']
year6 = ['70','71','72','73','74','75','76','77','78','79','80','81','82','83']

year7 = ['83','84','85','86','87','88','89','90','91','92','93','94','95','96']

sn_outdir = {}
at_outdir = {}
for year in [year1, year2, year3, year4, extra_year4, year5, year6, year7]:
    for s in year:
        sn_outdir[s] = ''
        at_outdir[s] = ''

N_sn = 0
N_at = 0
for idir in idirs:
    N_at += make_sector_page(idir)
    N_sn += make_sector_sn_page(idir)

    sector_search = re.search('sector(\d\d)',idir)
    sector = sector_search.group(1)
    sn_outdir[sector]  = cell_fmt.format('SN sector{}'.format(sector),
                                         'sn_sector{}/sn_sector{}.md'.format(sector,sector))
    at_outdir[sector]  = cell_fmt.format('sector{}'.format(sector),
                                         'sector{}/sector{}.md'.format(sector,sector))


print(N_sn,N_at)
sn_out = sn_out.format(N_sn)
at_out = at_out.format(N_at)

sn_out += '| Cycle 7 |  |\n|-----|------|\n'
at_out += '| Cycle 7 |  |\n|-----|------|\n'

for z in year7:
    sn_out += line_fmt.format( sn_outdir[z], ' ' )
    at_out += line_fmt.format( at_outdir[z], ' ' )

    
sn_out += '| Cycle 5 | Cycle 6|\n'
at_out += '| Cycle 5 | Cycle 6|\n'


for z in zip(year5,year6):
    sn_out += line_fmt.format( sn_outdir[z[0]], sn_outdir[z[1]] )
    at_out += line_fmt.format( at_outdir[z[0]], at_outdir[z[1]] )
    

sn_out += '| Cycle 3 | Cycle 4|\n'
at_out += '| Cycle 3 | Cycle 4|\n'
for z in zip(year3,year4):
    sn_out += line_fmt.format( sn_outdir[z[0]], sn_outdir[z[1]] )
    at_out += line_fmt.format( at_outdir[z[0]], at_outdir[z[1]] )
for z in extra_year4:
    sn_out += line_fmt.format( '', sn_outdir[z] )
    at_out += line_fmt.format( '', at_outdir[z] )

sn_out += ' | Cycle 1 | Cycle 2|\n'
at_out += '| Cycle 1 | Cycle 2|\n'

for z in zip(year1,year2):
    sn_out += line_fmt.format( sn_outdir[z[0]], sn_outdir[z[1]] )
    at_out += line_fmt.format( at_outdir[z[0]], at_outdir[z[1]] )



with open('content/pages/SN/SN.md','w') as fout:
    fout.write(sn_out)
with open('content/pages/all_AT/all_AT.md','w') as fout:
    fout.write(at_out)


with open('content/pages/README/README.md','w') as fout:
    with open('README.md','r') as fin:
        fout.write(fin.read())

with open('content/pages/lc_bulk/lc_bulk.md','w') as fout:
    fout.write('title: Bulk Downloads\nSlug: lc-bulk\npageorder: 4\n \n We keep the latest version of the data in these tarballs. However, you can access older versions of the data, which are under version control, through [this github repo](https://github.com/mmfausnaugh/lc_bulk). \n\n')
    tarballs = glob.glob('content/lc_bulk/*tgz')
    tarballs.sort()
    tarballs.reverse()
    for tarball in tarballs:
        fout.write('- [{filename}]({{static}}../../lc_bulk/{filename})\n'.format(filename=
                                                                               os.path.basename(tarball) ) )



with open('content/pages/transient_table/transient_table.md','w') as fout:
    fout.write('title: Transient Table\n slug: transient-table\n pageorder: 5 \n \n [Table of All Transients Observed by TESS]({filename}../../lc_bulk/count_transients.txt)' )
