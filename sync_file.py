import sys
import os
import subprocess
import time
remote_dir = sys.argv[1]
local_dir = sys.argv[2]
file_to_download = sys.argv[3]
assert(os.path.basename(remote_dir) == os.path.basename(local_dir))
assert(os.path.isabs(local_dir))

work_queue = [x[0] for x in os.walk(local_dir)]
work_queue = [x.replace(local_dir,"") for x in work_queue]
for each_dir in work_queue:
    cmd = ["scp","changming@129.10.122.21:{}".format(os.path.join("/home/changming/",remote_dir,each_dir,file_to_download)),os.path.join(local_dir,each_dir)]
    print(cmd)
    sp = subprocess.Popen(cmd)
    time.sleep(4)
