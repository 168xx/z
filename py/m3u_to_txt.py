import re  
  
def read_m3u_file(file_path):  
    with open(file_path, 'r', encoding='utf-8') as file:  
        lines = file.readlines()  
    return lines  
  
def write_txt_file(file_path, content):  
    # 使用列表生成式和字符串的 replace 方法去除每行中的双引号  
    cleaned_content = [line.replace('"', '') for line in content]  
    with open(file_path, 'w', encoding='utf-8') as file:  
        file.writelines(cleaned_content)  
  
def convert_m3u_to_txt(m3u_lines):  
    channels = {}  
    current_group = None  
    i = 0  
  
    while i < len(m3u_lines):  
        line = m3u_lines[i].strip()  
        if line.startswith('#EXTINF'):  
            _, info = line.split('#EXTINF:', 1)  
            info_parts = info.split(',', 1)  
            metadata = [item.split('=') for item in info_parts[0].split() if '=' in item]  
            channel_name = info_parts[1].strip('"')  # 这里已经去除了双引号  
            channel_url = m3u_lines[i + 1].strip()  
  
            group_title_info = next((item for item in metadata if item[0] == 'group-title'), None)  
            if group_title_info:  
                current_group = group_title_info[1]  
  
            channels.setdefault(current_group, []).append({'name': channel_name, 'url': channel_url})  
            i += 2  
        else:  
            i += 1  
  
    txt_content = []  
    for group, channel_list in channels.items():  
        txt_content.append(f"{group},#genre#\n")  
        for channel in channel_list:  
            # 这里不需要再次去除双引号，因为它们在添加到字典时已经被处理过了  
            txt_content.append(f"{channel['name']},{channel['url']}\n")  
  
    return txt_content  
  
def main():  
    m3u_file_path = 'v4/v4.m3u'  
    txt_file_path = 'v4/v4.txt'  
  
    m3u_lines = read_m3u_file(m3u_file_path)  
    txt_content = convert_m3u_to_txt(m3u_lines)  
    write_txt_file(txt_file_path, txt_content)  
  
if __name__ == "__main__":  
    main()