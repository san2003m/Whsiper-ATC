# Whsiper-ATC
2024년 창원대학교 정보통신공학과 캡스톤디자인 - 음성인식을 이용한 항공교통관제(ATC) 보조시스템

## 소개
Whisper-ATC은 OPENAI사가 개발한 Whisper 모델에 항공교통관제(ATC)의 교신내용을 추가로 Fine-Tuning(미세조정)하여 만든 모델을 사용합니다.

해당 모델을 이용하여 항공교통관제의 교신내용을 Speech To Text하여, DB에 저장하고 웹 상에서 열람하도록 하는 기능을 제공합니다.

*웹 페이지 코드는 보안상의 이유로 공개하지 않음.(DB 접속 정보 및 외부 API키) 

*추후, 업로드 예정.

## 웹페이지
웹페이지는 아래 링크를 방문해주세요
* http://atc.kyunsan.com/

## 모델
음성인식 모델은 아래 링크를 방문해주세요
* san2003m/whisper-small-atc
(https://huggingface.co/san2003m/whisper-small-atc)

## 사용기술
<img width="1453" alt="image" src="https://github.com/san2003m/Whsiper-ATC/assets/12150769/5d0c606e-ff61-4c4e-b3ea-b9e1da89c9e0">

## 구성도
<img width="1443" alt="image" src="https://github.com/san2003m/Whsiper-ATC/assets/12150769/59feeae6-7c01-4b43-b805-5ee20aac5f4e">
