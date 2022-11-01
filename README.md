#밀양캠퍼스 유틸리티 플랫폼 서버
##views
###auth_view
- 중복체크 api (100, 101, 102)
  - pymysql로 DB에 접속해 칼럼을 조회한다
  - 조회된 칼럼의 개수가 0이면 미중복, 1이면 중복임을 통해 판별한다
   
- 회원가입 api (103)
    - pymysql로 DB에 접속해 유저 테이블에 삽입한다
    - 삽입 전 bcrypt 모듈로 비밀번호를 해시화 해서 저장한다
       
- 로그인 api (104)
  - user_name을 기반으로 조회한다
  - bcrypt 모듈로 유저가 인증요청한 pw와 조회한 pw데이터를 비교한다
  - 결과에 따라 jwt토큰을 발급한다
-------------------------------------------------------------------------
###order_api
1. 배달 가게 조회 관련
   - 배달 가게 조회 api (201)
     - DB에 있는 가게 목록 DB를 menu 필드를 제외하고 가져온다
     - 조회된 `'_id'` 값은 Object Type 필드이므로 str형으로 변환해준다
        
   - 가게 메뉴 리스트 조회 api (202)
     - store_id로 가게 데이터를 조회한 뒤 menu 필드의 데이터를 처리한다
     - 처리 프로세스는 `섹션분류 모듈`을 참고한다
        
   - 메뉴 상세 조회 api (203)
     - store_id, menu_name 값으로 메뉴를 조회하고 groups 필드를 반환한다
-------------------------------------------------------------------------
2. 게시글 관련
   - 게시글 작성 api (204)
     - mongodb에 connection하여 게시글을 삽입한다
        
   - 게시글 상세 조회 api (205)
     - post_id를 통해 mongodb delivery_post Collection에서 Document를 조회한다
     - find_one_and_update 메소드로 조회와 동시에 views 값을 1 증가시킨다
     - `_id`필드는 ObjectId 타입이기 때문에 str형으로 변환한다
        
   - 게시글 수정 api (206)
     - Get 요청시 수정 가능한 항목을 projection하여 조회한다
     - Patch 요청시 json 데이터를 가지고 수정한다
        
   - 주문 마감 여부 전환 api (207)
     - api 요청시 게시글의 현재 isClosed 필드의 상태를 not 연산하여 전환한다

   - 그룹 참가/탈퇴 api (211)
     - api 요청시 게시글의 현재 참여중인 그룹에 참여/탈퇴한다
     - db 조회 후 api 요청 유저가 해당 그룹에 참여중이라면 join_users 필드에서 유저 제거, 미참여라면 추가
       - 탈퇴시 주문 목록도 함께 삭제        

   - 게시글 리스트 api (213)
     - 현재 존재하는 게시글 리스트를 조회 후 반환한다
     - content, user_orders 필드는 조회할때 제외한다
     - `_id` 필드를 모두 str형으로 변환한다
-------------------------------------------------------------------------
3. 주문 관련
   - 주문하기 api (209)
     - pricing 메소드로 주문한 메뉴에 가격을 조회한다
     - orders 필드에 삽입
   
   - 주문 수정 api (210)
     - Get 요청시 유저가 했던 주문을 반환
     - Patch 요청시 pricing 메소드로 주문한 메뉴에 가격을 조회 데이터 수정
-------------------------------------------------------------------------
###taxi_view
- 게시글 작성 api (302)
  - mongodb에 connection하여 게시글을 삽입한다

- 게시글 상세 조회 api (303)
  - post_id를 통해 mongodb delivery_post Collection에서 Document를 조회한다
  - find_one_and_update 메소드로 조회와 동시에 views 값을 1 증가시킨다
  - `_id`필드는 ObjectId 타입이기 때문에 str형으로 변환한다
        
- 게시글 수정 api
  - Get 요청시 수정 가능한 항목을 projection하여 조회한다
  - Patch 요청시 json 데이터를 가지고 수정한다
  