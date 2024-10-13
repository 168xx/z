import datetime  
import os  
  
def txt_to_m3u(input_file, output_file):  
    # 获取当前 UTC 时间并转换为北京时间  
    now = datetime.datetime.now(datetime.timezone.utc).astimezone(datetime.timezone(datetime.timedelta(hours=8)))  
    current_time = now.strftime("%m-%d %H:%M")  
  
    try:  
        # 读取 txt 文件内容  
        with open(input_file, 'r', encoding='utf-8') as f:  
            lines = f.readlines()  
    except FileNotFoundError:  
        print(f"文件 {input_file} 不存在。")  
        return  
  
    try:  
        # 生成输出文件名，假设输出文件与输入文件同名，但扩展名为 .m3u  
        base_name = os.path.basename(input_file)  
        root, ext = os.path.splitext(base_name)  
        output_file = os.path.join(os.path.dirname(input_file), root + '.m3u')  
          
        # 如果指定了特定的输出目录，则使用该目录  
        # 这里我们暂时保留原逻辑中的 output_file 参数作为可能的自定义输出路径  
        # 但实际上，我们可以根据需求调整  
        # output_file = os.path.join('指定输出目录', root + '.m3u')  # 如果需要自定义输出目录，取消注释并修改  
  
        with open(output_file, 'w', encoding='utf-8') as f:  
            f.write('#EXTM3U x-tvg-url="https://live.fanmingming.com/e.xml" catchup="append" catchup-source="?playseek=${(b)yyyyMMddHHmmss}-${(e)yyyyMMddHHmmss}"\n')  
            f.write(f'#EXTINF:-1 group-title="💚更新时间{current_time}",仅供学习使用\n')  
            f.write(f'http://ali.hlspull.yximgs.com/live/asdfg863678266.flv\n')  
  
            # 初始化 genre 变量  
            genre = ''  
            # 遍历 txt 文件内容  
            for line in lines:  
                line = line.strip()  
                if "," in line:  
                    channel_name, channel_url = line.split(',', 1)  
                    if channel_url == '#genre#':  
                        genre = channel_name  
                    else:  
                        f.write(f'#EXTINF:-1 tvg-id="{channel_name}" tvg-name="{channel_name}" tvg-logo="https://live.fanmingming.com/tv/{channel_name}.png" group-title="{genre}",{channel_name}\n')  
                        f.write(f'{channel_url}\n')  
    except IOError:  
        print(f"无法写入文件 {output_file}。")  
  
def convert_all_txt_to_m3u(input_folder):  
    # 遍历输入文件夹中的所有文件  
    for filename in os.listdir(input_folder):  
        if filename.endswith('.txt'):  
            input_file = os.path.join(input_folder, filename)  
            # 调用转换函数  
            txt_to_m3u(input_file, os.path.join(input_folder, os.path.splitext(filename)[0] + '.m3u'))  
  
# 将 tv 文件夹中的所有 txt 文件转换为 m3u 文件  
convert_all_txt_to_m3u('tv')