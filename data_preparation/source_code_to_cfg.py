import os
import sys

pass_path = '/home/vienna/FYP/llvm-pass/build/traversal/libTraversalPass.so'
source_path = '/home/vienna/FYP/SampleSource'
cfg_path = '/home/vienna/FYP/cfg'

if __name__ == "__main__":


    def build_cfg(filename):
        file_path = source_path + '/' + filename
        cfg_file_path = cfg_path + '/' + filename + '.cfg.json'

        cmd = 'clang -Xclang -load -Xclang "%s" "%s" > "%s"' % (pass_path, file_path, cfg_file_path)
        print(cmd)
        os.popen(cmd)        

    def init():
        global source_path
        global cfg_path

        if len(sys.argv) != 2:
            print('1 argument (the question number[b-k]) exprected')
            exit()
        else:
            q = sys.argv[1]
            source_path += '/' + q
            cfg_path += '/' + q

    init()
    print('source_path = %s' % source_path)
    print('cfg_path = %s' % cfg_path)
    for (x, y, filenames) in os.walk(source_path):
        for f in filenames:
            if f[0] != '.':
                build_cfg(f)
