#-*- coding:utf-8 -*-
from multiprocessing import Process
from subprocess import Popen, PIPE, STDOUT
import shlex
import os
import time
import psutil
import fcntl
import traceback
from kd_exception import *
import socket
import sys

class BasePipe(object):
    def __init__(self, command_line):
        #if 'bash' not in command_line:
        #    command_line = 'env -i bash -c \'' + command_line + '\''
        self.__cmd_args = shlex.split(command_line)
        if 'python' in self.__cmd_args and '-u' not in self.__cmd_args:
            self.__cmd_args.insert(self.__cmd_args.index('python')+1, '-u')
        self.__pid = os.getpid()
        self.proc_pid = None
        self.popen_inst = None
        self.__memory = None
        self.__proc = None
        self.__p_pid = None
        
    def start(self):
        self.popen_inst = Popen(self.__cmd_args, stdout=PIPE, stderr=PIPE, shell=False)
        self.__p_pid = self.popen_inst.pid
        self.__proc = psutil.Process(self.__p_pid)   #NoSuchProcess: No process found 
        time_start = time.time()
        while True:
            children = self.__proc.children()
            if len(children) != 0:
                child = children[0]
                self.proc_pid = child.pid
                break
            if time.time() - time_start >= 3:
                self.proc_pid = self.__p_pid
                break
        #sys.stdout.write('父进程id: %s\n' % str(self.__pid))
        sys.stdout.write('进程id: %s\n' % str(self.proc_pid))
        #设置stdout为非堵塞状态
        self.__output = self.popen_inst.stdout
        fd_out = self.__output.fileno()
        fl_out = fcntl.fcntl(fd_out, fcntl.F_GETFL)
        fcntl.fcntl(fd_out, fcntl.F_SETFL, fl_out | os.O_NONBLOCK)
        #设置stderr为非堵塞状态
        self.__errput = self.popen_inst.stderr
        fd_err = self.__errput.fileno()
        fl_err = fcntl.fcntl(fd_err, fcntl.F_GETFL)
        fcntl.fcntl(fd_err, fcntl.F_SETFL, fl_err | os.O_NONBLOCK)
        return self.popen_inst
    
    def noneblock_get_out(self):
        buff_out = ''
        try:
            while True:
                line = self.__output.read()
                if not line:
                    break
                buff_out += line
            return buff_out
        except:
            return buff_out
   
    def noneblock_get_err(self):
        buff_err = ''
        try:
            while True:
                line = self.__errput.read()
                if not line:
                    break
                buff_err += line
            return buff_err
        except:
            return buff_err


 
    def wait(self):
        self.popen_inst.wait()
 
    #只杀死子进程
    def kill(self, signal=15):
        self.__kill_pid(self.__p_pid, signal)
        self.wait()
        
    def __kill_pid(self, pid, signal):
        p = psutil.Process(self.__p_pid)
        os.system('kill -%s %s' % (str(signal), str(pid)))
        for child in p.children():
            if child:
                #sys.stderr.write(child.pid)
                self.__kill_pid(self, signal)
            else:
                return 

    #获取子进程的返回值
    def get_return_code(self):
        self.popen_inst.wait()
        value = self.popen_inst.returncode
        return value

    def get_rss_memory(self):
        proc = psutil.Process(self.proc_pid)   #NoSuchProcess: No process found 
        self.__memory = proc.memory_info().rss *1.0 / 1024 / 1024    
        return self.__memory
   
    def gen_core(self, pid):
        #设置coredump文件大小
        coreSize_cmd = 'ulimit -c unlimited'
        os.system(coreSize_cmd)
        #查询coredump文件产生位置
        corePath = os.popen('cat /proc/sys/kernel/core_pattern').read()
        sys.stderr.write('coredump文件: %s\n' % corePath)
        coreDump_cmd = 'kill -11 ' + str(pid)
        try:
            coreDump_inst = Popen(coreDump_cmd, stdout=PIPE, stderr=PIPE, shell=True)
            coreDump_out = coreDump_inst.stdout.readline()
            sys.stderr.write('%s\n' % coreDump_out)
            sys.stderr.write('Segmentation fault (core dumped)\n')
        except Exception, e:
            sys.stderr.write(traceback.format_exc())


class AdvPipe(BasePipe):
    def __init__(self, command_line, timeout, total_memory):
        super(AdvPipe, self).__init__(command_line)
        self.__timeout = float(timeout)
        self.__child_oom = float(total_memory)
    
    def run(self, verbose=False):
        if not verbose:
            self.popen_inst.communicate()
        else:
            how_long_no_stdout = 0
            how_long_no_stderr = 0
            #sys.stderr.write(str(self.proc_pid) + '\n')
            try:
                time_start_out = time.time()
                time_start_err = time_start_out
                while self.popen_inst.poll() is None:
                    buff_out = None
                    buff_err = None
                    buff_out = self.noneblock_get_out()
                    how_long_no_stdout = time.time() - time_start_out
                    if buff_out:
                        sys.stdout.write(buff_out)
                        time_start_out = time.time()
                    buff_err = self.noneblock_get_err()
                    how_long_no_stderr = time.time() - time_start_err
                    if buff_err:
                        sys.stderr.write(buff_err)
                        time_start_err = time.time() 
                    if how_long_no_stdout > self.__timeout and how_long_no_stderr > self.__timeout:
                        raise ProcessTimeOutException(time=self.__timeout, pid=self.proc_pid, hostname=socket.gethostname(), how_long_no_output=max(how_long_no_stdout, how_long_no_stderr)) # out和err都超时没有输出
                    total_memory = self.get_rss_memory()
                    if total_memory > self.__child_oom:
                        raise ProcessMemoryOutException(total_memory=total_memory, limit_memory=self.__child_oom, pid=self.proc_pid, hostname=socket.gethostname()) #超出限制内存
                    time.sleep(0.001)
                # 进程结束之后，可能管道里还有数据
                buff_out_list = self.popen_inst.stdout.readlines()
                if len(buff_out_list) != 0:
                    sys.stdout.write(''.join(buff_out_list))
                buff_err_list = self.popen_inst.stderr.readlines()
                if len(buff_err_list) != 0:
                    sys.stderr.write(''.join(buff_err_list))
                self.wait()
            except ProcessTimeOutException, e: 
                sys.stderr.write(traceback.format_exc())
                self.kill(9)
            except ProcessMemoryOutException, e:
                sys.stderr.write(traceback.format_exc())
                self.kill(9)
            except psutil.NoSuchProcess, e:
                sys.stderr.write('This process is already dead.\n')

        

def test1():
    p = AdvPipe('env -i bash -c "export CUDA_VISIBLE_DEVICES=99 && /opt/mr_binary/autohdmap_multi_merge_diff_cli_v1.6.3/autohdmap_multi_merge_diff_cli is_parallel_computing=true is_diff_by_task_id=false work_dir=task_400227183 diff_config_path=/opt/mr_binary/autohdmap_multi_merge_diff_cli_v1.6.3 project_id=400002378 fusion_area_id=copy_110000_576226_6 is_bridge=true taskId=400227183 ref_version=yy_0322_1"', '100', '50')
    #p = AdvPipe('python child.py', '6', '6')
    #p = WorkerProcess('python test.py')
    p.start()
    #os.system('ps -ef|grep python')
    #time.sleep(10)
    #os.system('ps -ef|grep test_lane_client')
    p.run(True)
    #time.sleep(10)
    print 'finish'
    #print '子进程占用内存大小: %d KB' % p.get_rss_memory()
    #p.kill()
    #p.wait()
    #time.sleep(1)
    #print '子进程返回值: %s' % p.get_return_code()

if __name__ == '__main__':
    test1()
