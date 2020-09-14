import poplib 
import email 
import time 
import os 
from email.parser import Parser 
from email.header import decode_header 
from email.utils import parseaddr
import smtplib
import email.mime.multipart     
import email.mime.text
#-------------------------------------------------------------------------------------
  
address = '小小羊@shanghaitech.edu.cn' # 校园邮箱账号
password = '' # 校园邮箱密码
pop3_server = 'mail.shanghaitech.edu.cn' 
emai_user = '小小羊@163.com'      # 发送者
emai_recver = '小小羊@163.com'  # 接收者
emai_passwd = '小小羊'      # 发送者的授权码
emai_server = 'smtp.163.com'  # 服务器

delete = 0  #若改为1则在下载、转发完成后将原邮件删除
forward = 1 #若改为1则在下载邮件完成后转发到指定邮箱

# ----------------------------------------------------------------------------------
  
def decode_str(s):
  value, charset = decode_header(s)[0] 
  if charset: 
    value = value.decode(charset) 
  return value 

def parse_email(msg, indent,file):
    if indent == 0:
        for header in ['From', 'To', 'Subject']:
            value = msg.get(header, '')
            if value:
                if header=='Subject':
                    value = decode_str(value)
                else:
                    hdr, addr = parseaddr(value)
                    name = decode_str(hdr)
                    value = u'%s <%s>' % (name, addr)
            f.write('%s%s: %s' % ('  ' * indent, header, value))

    if (msg.is_multipart()):
        parts = msg.get_payload()
        for n, part in enumerate(parts):
            return parse_email(part, indent + 1, file)

    else:
        content_type = msg.get_content_type()
        if content_type=='text/plain' or content_type=='text/html':
            content = msg.get_payload(decode=True)
            charset = guess_charset(msg)
            if charset:
                content = content.decode(charset,'ignore')
            f.write('%sText: %s' % ('  ' * indent, content))
        else:
            f.write('%sAttachment: %s' % ('  ' * indent, content_type))

def guess_charset(msg):
    charset = msg.get_charset()
    if charset is None:
        content_type = msg.get('Content-Type', '').lower()
        for item in content_type.split(';'):
            item = item.strip()
            if item.startswith('charset'):
                charset = item.split('=')[1]
                break
    return charset
      
        
server = poplib.POP3_SSL(pop3_server) 
print(server.getwelcome().decode('utf-8'))
server.user(address) 
server.pass_(password)
print('Messages: %s. Size: %s' % server.stat()) 
resp, mails, octets = server.list() 
index = len(mails)

#-----------------------------------------------------------------------------

for i in range(index-5, index - 10, -1):
    
    resp, lines, octets = server.retr(i)
    msg_content = b'\r\n'.join(lines).decode('utf-8')
    msg = Parser().parsestr(msg_content)

    date1 = time.strptime(msg.get("Date")[0:24],'%a, %d %b %Y %H:%M:%S') #时间格式化
    date2 = time.strftime("%Y%m%d", date1)  #格式转换
    print('日期：'+date2)

# --------------------------------------------------------------------------------------

    # if (date2<='20200912'):
    #     continue

# ---------------------------------------------------------------------------------------
    os.mkdir('no' + str(i))
    print('生成文件夹:no'+ str(i))
    AttachmentList = []
    for part in msg.walk():
        if not part.is_multipart():
            file = part.get_filename()  
            if file != None:
                b_filename = email.header.decode_header(file)[0][0]
                filename = str(b_filename)
                # print(filename,type(filename))
                charset = email.header.decode_header(file)[0][1]
                if type(b_filename) is not str:
                    filename = b_filename.decode()
                print(filename)
                # print(charset)
                # print()
                filedata = part.get_payload(decode=True)  # 附件内容
                AttachmentList.append('no' + str(i) + '/' + filename)
                fw = open('no' + str(i) + '/' + filename, "wb")
                fw.write(filedata)
                fw.close() 

    f = open('no' + str(i)+'/context.html', 'w',encoding="utf-8")
    parse_email(msg, 0, f)
    f.close()
    

#----------------------------------------------------------------------------------------
    if forward == 0:
        continue


    for header in ['From', 'To', 'Subject']:
        value = msg.get(header, '')
        if value:
            if header == 'Subject':
                value = decode_str(value)
                emai_subject = value
            elif header in ['From','To']:
                hdr, addr = parseaddr(value)
                name = decode_str(addr)
                value = name
        print(header + ':' + value)

    message = email.mime.multipart.MIMEMultipart()  
    message['from'] = emai_user   
    message['to'] = emai_recver   
    message['subject'] = emai_subject     

    f = open('no' + str(i) + '/context.html', 'r', encoding="utf-8")
    html = email.mime.text.MIMEText(f.read(), 'html', 'utf-8')
    f.close()
    message.attach(html)
    # print(AttachmentList)
    for _file in AttachmentList:
        att = email.mime.text.MIMEText(open(_file, 'rb').read(), 'base64', 'utf-8')
        att["Content-Type"] = 'application/octet-stream'        
        att["Content-Disposition"] = 'attachment;filename="'+ _file +'"' 
        message.attach(att)
        # print(_file)

    stmp_obj = smtplib.SMTP_SSL(emai_server, 465)
    stmp_obj.login(emai_user, emai_passwd) 
    stmp_obj.sendmail(emai_user, emai_recver, message.as_string())
    print('发送邮件：' + emai_subject)

# -------------------------------------------------------------------------------------

    if delete == 1:
        server.dele(i)
        print('删除第'+str(i)+'封邮件')

# ---------------------------------------------------------------------------------------
    print()
  
server.quit()



