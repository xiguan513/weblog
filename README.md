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
    
安装ansible
-----------------------------------

    更新安装库
    sudo apt-get update
    
    然后输入最后的四行命令进行安装的操作
    sudo apt-get install software-properties-common
    sudo apt-add-repository ppa:ansible/ansible
    sudo apt-get update
    sudo apt-get install ansible

安装组件
-----------------------------------

    pip  intall -r requirements.txt
        
    python db_create.py #执行sql 
    
    python run.py#运行服务
      
      

