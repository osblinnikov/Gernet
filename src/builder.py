# realpath() with make your script run, even if you symlink it :)
#
# cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
# if cmd_folder not in sys.path:
# sys.path.insert(0, cmd_folder)
#
# use this if you want to include modules from a subforder
import inspect
import re
import sys
from attrs import attrs
import json, os

cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0])))
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)

from cogapp import cogapp
from mako.template import Template
from mako.lookup import TemplateLookup

join = os.path.join

#PLEASE change it if you don't want the standard workspace root folder location
PROJECTS_ROOT_PATH = os.path.abspath(join(os.path.dirname(__file__), '..', '..', '..', '..', '..'))


def tpl(strfile, args):
    mylookup = TemplateLookup(directories=[
        os.path.abspath(os.getcwd())
    ])
    tplFromFile = Template(filename=strfile, lookup=mylookup, imports=['from src.attrs import attrs'])
    return tplFromFile.render(a=args)


def getArgs(firstRealArgI, argv, Types):
    all_args = []
    compiling_arg = ['-U', '-c']  #-U means unix style line endings

    if len(argv) > firstRealArgI + 1:
        for i in range(firstRealArgI + 1, len(argv)):
            if argv[i] == '-c':
                compiling_arg = ['-x']
            elif argv[i] == '-g':
                if i + 1 == len(argv) or argv[i + 1].startswith("-"):
                    raise Exception("expected language type after -lang option")
                else:
                    Types.append(argv[i + 1])
                    i = i + 1
            elif argv[i - 1] == '-g' or i == 1:
                continue
            else:
                all_args.push(argv[i])
    all_args += compiling_arg
    return all_args

def readJson(topology_dir):
    json_file_to_read = join(topology_dir, "gernet.json")
    read_data = None
    with open (json_file_to_read, "r") as jsonfile:
        json_data = re.sub(r'/\*.*?\*/', '', jsonfile.read())
        try:
            read_data = json.loads(json_data)
        except:
            print json_file_to_read+" invalid"
            jsonfile.close()
            raise
        jsonfile.close()
    return read_data


def getFilteredSubFolders(folder, filters):
    res = []
    d = []
    for root, dirs, files in os.walk(folder):
        d = dirs
        break

    for i in d:
        if len(filters) == 0 or i in filters:
            res.append(i)
    return res

def getPath(pathSrc):
    path = pathSrc.split('.')
    if len(path) < 3:
        raise Exception("path: \""+pathSrc+"\" is not a full package name")
    arr = [PROJECTS_ROOT_PATH, 'src', path[1] + "." + path[0]]
    to_delete = [0, 1]
    for offset, index in enumerate(to_delete):
        index -= offset
        del path[index]
    return '/'.join(arr + path)


def generateMissedFiles(topology_dir, generator_dir, classPath, className, extra_args):
    json_file_to_read = join(topology_dir, "gernet.json")
    for root, dirs, files in os.walk(generator_dir):
        for fileName in files:
            file = os.path.join(root,fileName)
            if (len(fileName)>4 and fileName[-4:] == '.tpl') or not os.path.exists(file+".tpl"):
                continue

            generator_dirLen = (len(generator_dir))+1
            relativeFilePath =  file[generator_dirLen:]\
                .replace("_NAME_", className)\
                .replace("_PATH_", classPath)\
                .replace("_GERNET_","gernet")
            absDstFilePath = os.path.join(topology_dir, os.path.split(generator_dir)[1], relativeFilePath)
            if not os.path.exists(absDstFilePath):
                checkDir(absDstFilePath)

                f = open(absDstFilePath,'w')#output file
                f.write(tpl(
                    file,#input template
                    attrs(
                        prefix=json_file_to_read,#required for parser of json file
                        parserPath=generator_dir
                    )#args
                ))
                f.close()

            cogapp.Cog().main(['cogging']+extra_args+[
                '-I',
                os.path.abspath(os.path.dirname(__file__)),
                '-I',
                generator_dir,
                '-r',#replace in file
                "-D","configFile="+json_file_to_read, #specify config as global variable
                "-D","templateFile="+file+'.tpl', #specify config as global variable
                absDstFilePath
            ])


def runGernet(firstRealArgI, argv, topology_dir):
    Types = []
    extra_args = getArgs(firstRealArgI, argv, Types)
    read_data = readJson(topology_dir)
    Types = getFilteredSubFolders(getPath(read_data["type"]), Types)
    if len(Types) == 0:
        print ("No one generator was found")
        return
    for i in range(0, len(Types)):
        generateMissedFiles(
            topology_dir,
            os.path.join(getPath(read_data["type"]), Types[i]),
            '/'.join(read_data["path"].split('.') + [""]),
            read_data["path"].split('.')[-1],
            extra_args
        )


def checkDir(directory):
    fPath, fName = os.path.split(directory)
    if not os.path.exists(fPath):
        os.makedirs(fPath)
    return fPath
