설명: 기업 리스트 가져오기
url: https://jasoseol.com/employment/calendar_list.json
method: post
parameters: {"start_time": "2026-02-27T15:00:00.000Z", "end_time": "2026-04-04T15:00:00.000Z"}
result
```json
  {
   "employment": [
        {
            "id": 101823,
            "name": "토스뱅크",
            "title": "Asset Assistant",
            "company_group": {
                "id": 13930,
                "name": "토스뱅크",
                "created_at": "2022-08-10T16:40:13.000+09:00",
                "updated_at": "2024-10-14T16:35:55.000+09:00",
                "business_size": null,
                "business_type": null,
                "image_file_name": "logo-bank.png",
                "image_content_type": "image/png",
                "image_file_size": 106285,
                "image_updated_at": "2024-10-14T16:35:51.000+09:00",
                "settings_json": null,
                "alternate_names": [
                    "tossbank"
                ],
                "premiums": []
            },
            "start_time": "2026-01-02T17:00:00.000+09:00",
            "end_time": "2026-03-01T23:59:00.000+09:00",
            "image_file_name": "https://daoift3qrrnil.cloudfront.net/employment_companies/images/000/101/823/original/jss_hashed_a4495330f376e2a55cb6_20260102T164201_logo-bank.png?1767339721",
            "recruit_type": 1,
            "business_size": null,
            "business_type": null,
            "employments": [
                {
                    "duty_groups": [
                        {
                            "group_id": 128
                        },
                        {
                            "group_id": 130
                        },
                        {
                            "group_id": 107
                        }
                    ],
                    "id": 409164,
                    "division": 4,
                    "duty_category": null,
                    "apply": null
                }
            ],
            "in24hours": false,
            "is_receive_applicant": false
        }
    ]
  }
```
설명: 기업 모집분야 가져오기
url: https://jasoseol.com/employment/get.json
method: post
parameters: {"skip_read_log": true, "employment_company_id": 102727}
result
```json
{
    "ret": true,
    "id": 102727,
    "name": "LX인터내셔널",
    "image_file_name": "https://daoift3qrrnil.cloudfront.net/company_groups/images/000/000/058/webp/sns_lxinternational.webp?1698992522",
    "employment_page_url": "https://apply.lxcareers.com/app/job/RetrieveJobNoticesDetail.rpi?jobNoticeId=16607",
    "start_time": "2026-03-03T08:00:00.000+09:00",
    "end_time": "2026-03-22T23:00:00.000+09:00",
    "content": "\u003c!DOCTYPE html PUBLIC \"-//W3C//DTD HTML 4.0 Transitional//EN\" \"http://www.w3.org/TR/REC-html40/loose.dtd\"\u003e\n\u003chtml\u003e\u003cbody\u003e\u003cdiv\u003e\u003cimg style=\"max-width:100%;\" src=\"https://daoift3qrrnil.cloudfront.net/content_images/images/000/343/449/webp/_%EC%B5%9C%EC%A2%85_26%EC%83%81_LX%EC%9D%B8%ED%84%B0%EB%82%B4%EC%85%94%EB%84%90_%EC%9B%B9%ED%94%8C%EB%9D%BC%EC%9D%B4%EC%96%B4_%282%29.webp?1772156705\" alt=\"LX인터내셔널 2026년 상반기 신입사원 채용 (채용연계형 인턴십)\"\u003e\u003c/div\u003e\u003c/body\u003e\u003c/html\u003e\n",
    "target": 4,
    "created_at": "2026-02-27T10:58:25.000+09:00",
    "recruit_type": 0,
    "view_count": 27305,
    "favorite_count": 1490,
    "homepage_count": 355,
    "is_receive_applicant": false,
    "favorite": false,
    "chat_id": 3949,
    "attached_file_url": null,
    "direct_apply": false,
    "title": "2026년 상반기 신입사원 채용 (채용연계형 인턴십)",
    "resume_expose": true,
    "company_group": {
        "id": 58,
        "name": "LX인터내셔널",
        "business_size": "big_business",
        "business_type": null,
        "created_at": "2015-09-10T05:46:12.000+09:00",
        "updated_at": "2023-11-03T15:22:03.000+09:00",
        "image_url": "https://daoift3qrrnil.cloudfront.net/company_groups/images/000/000/058/original/sns_lxinternational.jpg?1698992522",
        "alternate_names": [
            "엘엑스인터내셔널"
        ],
        "premiums": [
            {
                "type": "JASOSEOL_PICK",
                "name": "자소설 PICK",
                "properties": {
                    "hr_comment": "글로벌 시장을 직접 개척 할 수 있는 기회를 잡아, 세계를 무대로 도전하세요!",
                    "description": ""
                },
                "priority": 100,
                "start_at": "2025-08-26T00:00:00.000+09:00",
                "end_at": null
            }
        ]
    },
    "employments": [
        {
            "id": 412566,
            "field": "자원사업 - 기술지원",
            "division": 1,
            "duty_category": null,
            "employment_resume": true,
            "resume_count": 24,
            "end_time": null,
            "duty_group_ids": [
                187,
                192,
                206,
                207,
                230,
                231,
                183,
                184,
                217
            ],
            "apply": null
        },
    ],
    "has_exceeded_employment": false
}
```
설명: 자소서 질문
url: https://jasoseol.com/employment/employment_question.json
method: post
parameters: {"employment_id": 412567}
result
```json
{
    "employment_question": [
        {
            "id": 2052984,
            "employment_resume_id": 412975,
            "subject": null,
            "question": "지원분야 지원 동기 / 성장 과정 (학창 시절 등) \r\n(지원 동기 및 입사 후 하고 싶은 직무 중심으로 간략하게 기술하여 주시기 바랍니다. 성장 과정과 같은 경우, 시기 및 기간은 자유롭게 선정하여 기술하되 지원 직무와 유관한 경험 및 과정 위주로 기술바랍니다.)",
            "number": 1,
            "is_character": true,
            "include_space": true,
            "total_count": 1000,
            "created_at": "2026-03-03T08:29:58.000+09:00",
            "updated_at": "2026-03-03T08:29:58.000+09:00",
            "count_mode": 1
        }
    ]
}
```

설명: 그룹과 그룹번호 매칭
url: https://jasoseol.com/api/v1/duty-groups
method: get
result
```json
[
{
"id": 160,
"name": "QA",
"order_point": 6900,
"group_id": 94,
"category": "medium"
},
{
"id": 161,
"name": "앱개발",
"order_point": 7000,
"group_id": 94,
"category": "medium"
},
{
"id": 162,
"name": "웹개발",
"order_point": 7100,
"group_id": 94,
"category": "medium"
},
{
"id": 163,
"name": "데이터엔지니어·분석·DBA",
"order_point": 7200,
"group_id": 94,
"category": "medium"
},
{
"id": 164,
"name": "시스템프로그래머",
"order_point": 7300,
"group_id": 94,
"category": "medium"
},
{
"id": 165,
"name": "응용프로그래머",
"order_point": 7400,
"group_id": 94,
"category": "medium"
},
{
"id": 166,
"name": "네트워크·보안·운영",
"order_point": 7500,
"group_id": 94,
"category": "medium"
},
{
"id": 167,
"name": "빅데이터·AI(인공지능)",
"order_point": 7600,
"group_id": 94,
"category": "medium"
},
{
"id": 168,
"name": "게임개발",
"order_point": 7700,
"group_id": 94,
"category": "medium"
},
{
"id": 169,
"name": "HW·임베디드",
"order_point": 7800,
"group_id": 94,
"category": "medium"
},
{
"id": 170,
"name": "SW·솔루션·ERP",
"order_point": 7900,
"group_id": 94,
"category": "medium"
},
{
"id": 171,
"name": "서비스기획·PM",
"order_point": 8000,
"group_id": 94,
"category": "medium"
},
{
"id": 172,
"name": "iOS개발",
"order_point": 8100,
"group_id": 161,
"category": "small"
},
{
"id": 173,
"name": "안드로이드개발",
"order_point": 8200,
"group_id": 161,
"category": "small"
}
]
```

devision
0 : 전체 (\uc804\uccb4)
1 : 신입 (\uc2e0\uc785)
2 : 경력 (\uacbd\ub825)
3 : 인턴 (\uc778\ud134)
4 : 계약직 (\uacc4\uc57d\uc9c1)
5 : 신입/경력 (\uc2e0\uc785/\uacbd\ub825)
6 : 신입/인턴 (\uc2e0\uc785/\uc778\ud134)
7 : 교육 (\uad50\uc721)