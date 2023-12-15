1. 创建pip隔离环境
```shell
python3 -m venv venv
source venv/bin/activate
```
2. 下载依赖
```shell
pip3 install -r requirements.txt
```
3. 执行数据库初始化
```shell
flask db init
flask db migrate
flask db upgrade
```
4. 启动
```shell
python app.py
```