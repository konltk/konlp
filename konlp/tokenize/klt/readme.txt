# Klt
Klt Tokenizer

## klt_asp
```
국민대학교 강승식 교수님의 자동 띄어쓰기 기능입니다.
한글 문장이 주어지면 자동 띄어쓰기를 진행 후,
공백(white-space) 기준으로 tokenize를 합니다.
Args:
    string(str): 띄어쓰기를 할 문장
    dic_path(str): 사전 폴더의 위치
    split(bool): 결과를 split할지 결정 하는 변수
Returns:
    list: tokenize된 list
    string: 만약 split이 `Flase`이면 한 문장
Example:
    >>> from konlp.tokenize import klt_asp
    >>> klt_asp(text="국민대학교자연어처리연구실")
    ['국민대학교', '자연어처리', '연구실']
    >>> klt_asp(text="국민대학교자연어처리연구실", split=False)
    '국민대학교 자연어처리 연구실'
    >>> klt_asp(text="국민대학교자연어처리연구실", split=True)
    ['국민대학교', '자연어처리', '연구실']
```