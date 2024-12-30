![Logo(Black)](https://github.com/user-attachments/assets/8d2ec67f-df6c-4127-a613-7ac5af76556f)
# Whsiper-ATC

2024년 국립창원대학교 정보통신공학과 캡스톤디자인(졸업작품) - 음성인식을 이용한 항공교통관제(ATC) 보조시스템 (김동균, 손승광)
Capstone Design (Graduation Work), Department of Information and Communication Engineering, Changwon National University, 2024 - Air Traffic Control (ATC) Auxiliary System using Voice Recognition (Dongkyun Kim, Seungkwang Son)

## 소개
Whisper-ATC은 OPENAI사가 개발한 Whisper 모델에 항공교통관제(ATC)의 교신내용을 추가로 Fine-Tuning(미세조정)하여 만든 모델을 사용합니다.
해당 모델을 이용하여 항공교통관제의 교신내용을 Speech To Text하여, DB에 저장하고 웹 상에서 열람하도록 하는 기능을 제공합니다.
Whisper-ATC uses the Whisper model developed by OPENAI, which is an additional Fine-Tuning model of Air Traffic Control (ATC) communications.
Using this model, it provides a function that allows you to speak to text communication content of air traffic control, store it in the DB, and view it on the web.

## 웹페이지
* https://home.kyunsan.com:3000/ 

<메인>
<img width="1902" alt="image" src="https://github.com/user-attachments/assets/e875aaf5-8764-4da9-81e6-613b25787bdc">

<기록열람>
<img width="2156" alt="image" src="https://github.com/user-attachments/assets/f60de4ab-2662-468d-8ed4-6b35920826a3">

<통계>
<img width="1919" alt="image" src="https://github.com/user-attachments/assets/94887105-10bb-48db-98c1-4483cef06e3d">

<녹음>
<img width="1937" alt="image" src="https://github.com/user-attachments/assets/b7dcac65-8b04-495d-b4e5-2f96225c6472">

  
## 모델
음성인식 모델은 아래 링크를 방문해주세요.
For voice recognition models, please visit the link below.

* san2003m/whisper-small-atc
(https://huggingface.co/san2003m/whisper-small-atc)

## 사용기술
<img width="1453" alt="image" src="https://github.com/san2003m/Whsiper-ATC/assets/12150769/5d0c606e-ff61-4c4e-b3ea-b9e1da89c9e0">

## 구성도
<img width="1443" alt="image" src="https://github.com/san2003m/Whsiper-ATC/assets/12150769/59feeae6-7c01-4b43-b805-5ee20aac5f4e">

## 참고
* Zuluaga-Gomez, Juan, et al. "How does pre-trained wav2vec 2.0 perform on domain-shifted asr? an extensive benchmark on air traffic control communications." 2022 IEEE Spoken Language Technology Workshop (SLT). IEEE, 2023.

* Zuluaga-Gomez, Juan, et al. "Bertraffic: Bert-based joint speaker role and speaker change detection for air traffic control communications." 2022 IEEE Spoken Language Technology Workshop (SLT). IEEE, 2023.

* Zuluaga-Gomez, Juan, et al. "Atco2 corpus: A large-scale dataset for research on automatic speech recognition and natural language understanding of air traffic control communications." arXiv preprint arXiv:2211.04054 (2022).
