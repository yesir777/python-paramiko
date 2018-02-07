import json
import paramiko
import threading

class Remotehost(object):
    def __init__(self,host,port,username,password,cmd):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.cmd = cmd

    def command(self):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        ssh.connect(hostname=self.host,port=self.port,username=self.username,password=self.password)
        stdin,stdout,stderr = ssh.exec_command(self.cmd)
        res,err = stdout.read(),stderr.read()
        result = res if res else err
        print("[%s]".center(50,"-")%self.host)
        print(result.decode())
        ssh.close()
    #
    # def put(self):
    #      try:
    #          transport = paramiko.Transport((self.host,self.port))
    #          transport.connect(username=self.username,password=self.password)
    #          sftp = paramiko.SFTPClient.from_transport(transport)
    #          sftp.put(self.cmd.split()[1],self.cmd.split()[2])
    #          transport.close()
    #          print("\033[32;0m【%s】 上传 文件【%s】 成功....\033[0m" % (self.host, self.cmd.split()[2]))
    #      except Exception as error:
    #          print("\033[31;0m错误:【%s】【%s】\033[0m" % (self.host, error))

    # def get(self):
    #      try:
    #          transport = paramiko.Transport((self.host, self.port))
    #          transport.connect(username=self.username, password=self.password)
    #          sftp = paramiko.SFTPClient.from_transport(transport)
    #          sftp.get(self.cmd.split()[1],self.cmd.split()[2])
    #          transport.close()
    #          print("\033[32;0m【%s】 下载 文件【%s】 成功....\033[0m" % (self.host, self.cmd.split()[2]))
    #      except Exception as error:
    #          print("\033[31;0m错误12:【%s】【%s】\033[0m" % (self.host, error))

    def run(self):
        cmd_str = self.cmd.split()[0]
        if hasattr(self,cmd_str):
            getattr(self,cmd_str)()
        else:
            setattr(self,cmd_str,self.command)
            getattr(self,cmd_str)()

if __name__ == "__main__":
    with open("database","r") as file:
        data_dice = json.loads(file.read())
    for k in data_dice:
        print(k)

    group_choice = input("输入要操作的组名>>：").strip()
    if data_dice.get(group_choice):
        host_dict =  data_dice[group_choice]
        for k in host_dict:
            print(k)
        while True:
            cmd = input("选择进行的操作命令>>：").strip()
            thread_list=[]
            if cmd:
                for k in host_dict:
                    host, port, username, password = k, host_dict[k]["port"], host_dict[k]["username"], host_dict[k][ "password"]
                    func = Remotehost(host,port,username,password,cmd)
                    t = threading.Thread(target=func.run)
                    t.start()
                   # print("test")
                    thread_list.append(t)
                for t in thread_list:
                    t.join()
                   # print(thread_list)
    else:
        print("\033[31;0m操作组不存在\033[0m")
