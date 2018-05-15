import os, re, subprocess, thread, threading, time, fileinput, urllib, commands, sys
import xml.etree.ElementTree as ET
from subprocess import Popen

pybotPath = "pybot"
rebotPath = "rebot"
prefix = "grid"
# pybotPath="/usr/local/bin/pybot"
# ttabPath="/usr/local/bin/ttab"

# pybotPath="/Library/Frameworks/Python.framework/Versions/2.7/bin/pybot"
# ttabPath="/Users/syam/.npm-packages/bin//ttab"
ttabPath = ""


# rebotPath="/usr/local/bin/rebot"
# rebotPath="/Library/Frameworks/Python.framework/Versions/2.7/bin//rebot"


def initilize():
    delete_all_grid_arg_files()
    xml_name = sys.argv[1]
    # print 'xml_name=%s'%xml_name
    argument_files_list = parse_config_xml(xml_name)
    # print  argument_files_list

    call_pybot(argument_files_list)
    combine_all_report(argument_files_list)


def delete_all_grid_arg_files():
    cwd = os.getcwd()
    for file in os.listdir(cwd):
        if file.startswith(prefix):
            try:
                os.remove(file)
            except OSError:
                pass


def combine_all_report(argument_files_list):
    output_xml_list = []
    xunit_xml_list = []
    for argument_file in argument_files_list:
        file = str(argument_file)
        # get the output xml report path
        output_xml = get_html_path_from_file(file)
        output_xml_list.append(output_xml)

    all_output_xml = " ".join(output_xml_list)
    # print   'all_output_xml %s'%all_output_xml

    for f in output_xml_list:
        f = f.replace('output.xml', 'output_xunit.xml')
        xunit_xml_list.append(f)

    all_xunit_output_xml = " ".join(xunit_xml_list)
    # print   'all_xunit_output_xml %s'%all_xunit_output_xml


    rebot_command = rebotPath + " --xunit output_xunit.xml" + " --output output.xml " + all_output_xml
    # +all_xunit_output_xml
    run_command(rebot_command)


def get_html_path_from_file(file):
    rel_path = os.getcwd() + "/" + file
    file_content = open(rel_path).read()
    outptDirMatch = re.search('--outputdir .(.*)\n', file_content)
    output_dir = outptDirMatch.group(1)
    output_xml = os.getcwd() + "/" + output_dir + "/output.xml"
    return output_xml


def get_txt_files():
    cwd = os.getcwd()
    argument_files_list = []
    for file in os.listdir(cwd):
        if file.startswith(prefix):
            # print file
            argument_files_list.append(file)
    return argument_files_list


def call_pybot(argument_files_list):
    # print argument_files_list
    size = len(argument_files_list)
    if size == 1:
        run_command('pybot -A ' + argument_files_list[0])
    else:
        threads = []
        for argument_file in argument_files_list:
            print '---------------------------------------'
            cmd = pybotPath + ' -x  output_xunit.xml ' + ' -A ' + str(argument_file)
            print  'Executing %s' % cmd
            t = threading.Thread(target=run_command, args=(cmd,))
            t.daemon = True
            threads.append(t)

        for x in threads:
            x.start()
            time.sleep(1)
        for x in threads:
            x.join()


def run_command(cmd):
    # print   os.getcwd()
    print cmd
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=os.getcwd())
    out = p.communicate()[0]
    print out
    return out


def parse_config_xml(xml_name):
    variables = []
    include = []
    exclude = []
    argfilesnamelist = []
    output = "."
    testsuitename = ""
    testcases = []

    tree = ET.ElementTree(file=xml_name)
    root = tree.getroot()
    for elem in tree.iterfind("common/variable"):
        # print elem.get("name")
        # print elem.text
        variables.append(elem.get("name") + ":" + elem.text)

    print "------------------------------------------------"
    customvariables = []
    for elem in tree.iterfind("node"):
        # print "++++++++++++++"
        # print "variables"
        for ele in elem.iterfind("variable"):
            # print ele.text
            customvariables.append(ele.get("name") + ":" + ele.text)
        # print "exclude"
        for ele in elem.iterfind("exclude"):
            # print ele.text
            exclude.append(ele.text)
        # print "include"
        for ele in elem.iterfind("include"):
            # print ele.text
            include.append(ele.text)
        # print "outputdir"
        for ele in elem.iterfind("outputdir"):
            # print ele.text
            output = ele.text
        # print "test-suites"
        arg_file_name = ''
        for ele in elem.iterfind("testsuites"):
            # print ele.get("name")
            arg_file_name = ele.get("name")
            testsuitename = arg_file_name
            argfilesnamelist.append(prefix + "_" + arg_file_name + ".txt")
            # print "path"
        for tc in ele.iterfind("path"):
            # print tc.text
            testcases.append(tc.text)
        fo = open(prefix + "_" + arg_file_name + ".txt", "wb")
        fin = customvariables + variables
        for var in fin:
            fo.write("--variable " + var + "\n")
        for inc in include:
            fo.write("--include " + inc + "\n")
        for exc in exclude:
            fo.write("--exclude " + exc + "\n")
        fo.write("--outputdir " + output + "\n")
        fo.write("--name " + testsuitename + "\n")
        for t in testcases:
            fo.write("    " + t + "\n")
        testcases = []
        customvariables = []
        include = []
        exclude = []

        fo.close()
    return argfilesnamelist


if __name__ == "__main__": initilize()
# if __name__ == "__main__":parse_config_xml()
# if __name__ == "__main__":start_grid()
# if __name__ == "__main__":run_command('pybot -A grid_MRA_Eligibility.txt')
