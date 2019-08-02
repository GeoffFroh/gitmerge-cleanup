import shutil, os

import argparse,datetime

description = """Removes bad git merge blocks from files."""

epilog = """
This command removes git-format merge blocks from files that were accidentally 
committed. It retains the HEAD versions.

EXAMPLE
  $ gitmerge-cleanup.py ./ddr-densho-2 ./output
"""

def cleanIt(filename):
    is_dirty = False
    cleaned = ''
    inmergeblock = False
    f = open(filename, 'r')
    for line in f:
	readthis = True
        if "=======" in line:
            is_dirty = True
            readthis = False
            inmergeblock = True
        if ">>>>>>>" in line:
            readthis = False
            inmergeblock = False
        if "<<<<<<<" in line:
            readthis = False
        if readthis and not inmergeblock:
            cleaned += line
    return is_dirty, cleaned

def cleanFiles(filesdir,outputpath):
    # get all entity.jsons
    files_to_clean = []
    files_cleaned = 0
    files_skipped = 0
    for root, dirs, files in os.walk(filesdir):
        for filename in files:
            if filename == 'entity.json':
                files_to_clean.append(os.path.join(root,filename))
    for fi in files_to_clean:
        is_dirty, clean_str = cleanIt(fi)
        if is_dirty:
            # write the clean file
            outdir, outname = os.path.split(os.path.abspath(fi))
            cfilepath = os.path.join(outputpath,outdir,outname)
            cleaned_file = open(cfilepath, 'w')
            cleaned_file.write(clean_str)
            cleaned_file.close()
            files_cleaned += 1
            print("{} - Saved clean file: {}".format(datetime.datetime.now(),cfilepath))
        else:
            # skip writing
            print("{} - Skipped file: {}".format(datetime.datetime.now(),fi))
            files_skipped += 1
    
    return(files_cleaned,files_skipped,len(files_to_clean))

# Main
def main():

    parser = argparse.ArgumentParser(description=description, epilog=epilog,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('filesdir', help='Path to DDR repo with bad files.')
    parser.add_argument('outputpath', nargs='?', default=os.path.join(os.getcwd(),"gitmerge-cleanupOut/"), help='Path to save output.')

    args = parser.parse_args()
    print('Repo dir path: {}'.format(args.filesdir))
    print('Output path: {}'.format(args.outputpath))

    started = datetime.datetime.now()
    inputerrs = ''
    if not os.path.isdir(args.filesdir):
        inputerrs + 'Repo dir does not exist: {}\n'.format(args.filesdir)
    if not os.path.exists(args.outputpath):
        inputerrs + 'Output path does not exist: {}'.format(args.outputpath)
    if inputerrs != '':
        print('Error -- script exiting...\n{}'.format(inputerrs))
    else:
        print('{} - Starting run.'.format(datetime.datetime.now()))
        print('Cleaned files will be saved to: {}'.format(args.outputpath))
        cleanFiles(args.filesdir,args.outputpath)
    
    finished = datetime.datetime.now()
    elapsed = finished - started
    
    print('Started: {}'.format(started))
    print('Finished: {}'.format(finished))
    print('Elapsed: {}'.format(elapsed))
    
    return

if __name__ == '__main__':
    main()
    
