import time, yaml, os
from src.log import Log
from src.Push import Push
from src.Miui import Miui
from src.SkyWingsCloud import Cloud
from src.aliyundrive import Aliyundrive
from src.raincloud import RainCloud
from src.hykb import HaoYouKuaiBao
from src.arknights import Arknights
from src.Sign import XiaoHeiHe,JiaoYiMao,wyyyx
log = Log()

def getconfig():
    path = os.path.dirname(os.path.realpath(__file__))
    with open(f'{path}/config.yaml', 'r', encoding='utf-8') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    
    # 从环境变量加载配置，覆盖yaml文件中的配置
    for key in os.environ:
        if key.startswith('CONFIG_'):
            # 解析环境变量，格式如 CONFIG_Push_Qmsg_key=value
            parts = key[7:].split('_')
            current = config
            for part in parts[:-1]:
                if part not in current:
                    current[part] = {}
                current = current[part]
            current[parts[-1]] = os.environ[key]
        elif key.startswith('SWITCH_'):
            # 处理开关配置，格式如 SWITCH_MiUI=true
            service = key[7:]
            if service in config['SignToken']:
                config['SignToken'][service]['switch'] = os.environ[key].lower() == 'true'
    
    return config

def run():
    #开始时间
    Begin = time.time()
    #程序主体
    config = getconfig()
    SignToken = config['SignToken']
    data = "今日签到结果:\n\n"
    # miui历史版本签到
    if SignToken['MiUI']['switch']:
        body = Miui(SignToken['MiUI'])
        data += "MIUI历史版本:\n"+body.Sign()
    if SignToken['Hykb']['switch']:
        body = HaoYouKuaiBao(SignToken['Hykb'])
        data += "\n\n好游快爆:\n"+ body.sgin()
    if SignToken['XiaoHeiHe']['switch']:
        body = XiaoHeiHe(SignToken)
        data += "\n\n小黑盒:\n"+body.Sgin()
    if SignToken['JiaoYiMao']['switch']:
        body = JiaoYiMao(SignToken)
        data += "\n\n交易猫:\n"+body.Sgin()

    # 天翼云盘签到
    if SignToken['Tyyp']['switch']:
        body = Cloud(SignToken['Tyyp'])
        data += "\n天翼云盘:\n"+body.sgin()
    if SignToken['wyyyx']['switch']:
        body = wyyyx(SignToken)
        data += "\n\n网易云游戏:\n"+body.Sgin()
    # 阿里云盘
    if SignToken['Aliyundrive']['switch']:
        body = Aliyundrive(SignToken['Aliyundrive'])
        data += "\n\n阿里云盘:\n"+body.sgin()
    # 雨云签到
    if SignToken['Raincloud']['switch']:
        body = RainCloud(SignToken['Raincloud'])
        data += "\n\n雨云:\n"+body.sgin()
    if SignToken['Arknights']['switch']:
        body = Arknights(SignToken['Arknights'])
        data += "\n\n明日方舟:\n"+body.sgin()
    # 结束时间
    end = time.time()
    sum = f"本次运行时间{round(end-Begin,3)}秒"
    data = data + "\n\n" + sum
    # 推送消息
    ts = Push(data,config['Push'])
    ts.push()

    log.info(sum)
    log.info("\n"+data)

if __name__ == '__main__':
    run()