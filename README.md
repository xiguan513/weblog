# weblog
实时日志 web显示
-----------------------------------  
    实时日志设计: 
      无需登录服务器,web 使用 Server-Sent Events(SSE)保持长连接,实时输出日志,支持关键过虑,红色标记
      方便快速查询日志
      
根据日期查询时间内的日志
-----------------------------------
    使用ansbible获取远端服务器日志信息，通过web展示
    
关键字查询
-----------------------------------
    通过grep查询关键字
    
后台添加主机
-----------------------------------
    通过后台添加主机和日志路径
    此主机和ansible里面hosts文件向对应，现阶段hosts需要手动添加主机信息
    [test]
    192.168.1.230 ansible_ssh_user=root

    
安装ansible
-----------------------------------

    更新安装库
    sudo apt-get update
    
    然后输入最后的四行命令进行安装的操作
    sudo apt-get install software-properties-common
    sudo apt-add-repository ppa:ansible/ansible
    sudo apt-get update
    sudo apt-get install ansible
    
    关闭验证
    host_key_checking = False
    提前配置要密钥连接

安装组件
-----------------------------------
    sudo pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ flask-babelex==0.9.3
    sudo pip  intall -r requirements.txt
        
    python db_create.py #执行sql 
    
    python run.py#运行服务
      
nginx 日志文件下载
----------------------------------

    autoindex on;
    server {
            listen 80;
            server_name 192.168.0.172;
            location /
            {
                    root /home/song/weblog/logs;
                    if ($request_filename ~* ^.*?\.(log|txt|doc|pdf|rar|gz|zip|docx|exe|xlsx|ppt|pptx)$){
                    add_header Content-Disposition 'attachment;';
                    }
    
            }
    }

nginx flask uwsgi配置
----------------------------------
    uWSGI 安装
        sudo apt-get install build-essential python-dev
        sudo pip install uwsgi



    配置nginx文件
    song@ansible:/etc/nginx/conf.d$ cat weblog.conf 
    server {
        listen 81;
        server_name 192.168.0.172
        charset utf-8;
        client_max_body_size 75M;
        location / { try_files $uri @yourapplication; }
        location @yourapplication {
            include uwsgi_params;
            uwsgi_pass 127.0.0.1:5000;
        }
    }
    
    配置uwsgi文件
    song@ansible:~/weblog$ cat config.ini
        [uwsgi]
        socket = 127.0.0.1:5000 #表示和Nginx通信的地址和端口
        processes = 4 #表示开启多少个子进程处理请求。
        threads = 2 #每个进程的线程数
        master = true
        pythonpaht = /home/song/weblog #表示项目目录
        module = run #表示项目启动模块，如上例为run.py，这里就为run
        callable = app #表示Flask项目的实例名称，上例代码中app = Flask(__name__)，所以这里为app
        memory-report = true

    启动uwsgi服务
    song@ansible:~/weblog$ uwsgi -d /var/log/uwsgi.log --ini /home/song/weblog/config.ini
