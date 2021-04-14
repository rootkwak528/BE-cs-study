# CS 그룹 스터디 웹 애플리케이션

> written by Root_Kwak on April, 2021



## 1. 실행결과

> https://root-cs-vote.herokuapp.com/

### 1-1. 계정 생성과 로그인

작성 예정



## 2. 코드

작성 예정



## 3. 개발환경

* OS : macOS Big Sur
* Python : Python 3.8.6
* 라이브러리 항목은 requirements.txt 참고



## 4. 로컬 설치 방법

> 로컬에서 설치하려면 아래 방법을 순차적으로 실행하면 됩니다. (기본 로컬 서버 실행 주소 [127.0.0.1:8000](http://127.0.0.1:8000/))
> 외부 서버로 배포하려면 `$ python manage.py collectstatic` 및 사용하는 배포 서비스의 세부사항을 따르면 됩니다.

```bash
# 1. 가상환경 생성 및 실행
$ python3 -m venv venv
$ source venv/bin/activate

# 2. 라이브러리 설치
(venv)$ pip install -r requirements.txt

# 3. DB 마이그레이션 적용
(venv)$ python manage.py migrate

# 4. 장고 서버 실행
(venv)$ python manage.py runserver
```



fin.