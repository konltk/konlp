import subprocess
import locale
import json
import os
import konlp
os_encoding = locale.getpreferredencoding()
print(os_encoding)

class klt2023:
    def __init__(self):
        jarpath = konlp.__path__[0] + "/kma/klt2023/lib/klt2023.jar"
        dicpath = os.sep.join([konlp.__path__[0],"kma","klt2023","hdic"])+os.sep
        self.proc = subprocess.Popen('java -jar {} {}'.format(jarpath,dicpath),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)

    def call_klt2023(self,mode:str, string:str):
        self.proc.stdin.write("{}\n".format(mode).encode())
        self.proc.stdin.flush()
        self.proc.stdin.write((string+"\n").encode())
        self.proc.stdin.flush()

        jsonStr = self.proc.stdout.readline().decode()
        try:
            jsons = json.loads(jsonStr)
        except:
            jsons = json.loads('["error"]')

        return jsons

    def pos(self,string:str):
        return self.call_klt2023('pos',string)
    
    def nouns(self,string:str):
        return self.call_klt2023('nouns',string)
    
    def morphs(self,string:str):
        return self.call_klt2023('morphs',string)
    
    def __del__(self):
        self.proc.kill()
        # print("klt2023 killed")

if __name__ == '__main__':    
    klt = klt2023()
    # print(klt.pos('나는 밥을 먹고 학교에 갔다.'))
    cnt = 10
# while cnt >= 0:
    file = open('klt_kcc150.txt','w',encoding='utf-8')
    from tqdm import tqdm
    # klt.pos('막연히 훌륭한 정치가가 되어야 겠다는 부르주아적 정치관도 어느정도 극복되었다.')
    # file = open('extractive_summarization.txt','w',encoding='utf-8')
    with open('KCC150_Korean_sentences_UTF8.txt',encoding='utf-8') as f:
        cnt = len(f.readlines())
        f.seek(0)
        for _ in tqdm(range(cnt)):
            l = f.readline().strip()
            # print(l)
            a = klt.pos(l)
            file.write(' '.join(a) + '\n')
    file.close()
# cnt = 10
# while cnt >= 0:
# from tqdm import tqdm
# file = open('extractive_summarization.txt','w',encoding='utf-8')
# with open('KCC150_Korean_sentences_UTF8.txt',encoding='utf-8') as f:
#     # cnt = len(f.readlines())
#     # f.seek(0)
#     for _ in tqdm(range(10)):
#         l = f.readline().strip()
#         if l == '[EOD]':
#             file.write('[EOD]\n')
#             continue
#         proc.stdin.write("pos\n".encode("cp949"))
#         proc.stdin.flush()
#         proc.stdin.write((l+"\n").encode("cp949"))
#         proc.stdin.flush()

#         a = proc.stdout.readline().decode("cp949")
#         # cnt -= 1
#         # a = a.strip()
#         # print(a)
#         a = json.loads(a)

#         file.write(' '.join(a) + '\n')
# file.close()
