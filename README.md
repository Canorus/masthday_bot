# masthday_bot
#### Mastodon 인스턴스 [트윙여](https://twingyeo.kr)의 새로운 멤버와 n 주년을 맞은 멤버를 축하하는 봇입니다.

- 트윙여의 로컬 타임라인을 지켜보다가 툿을 한 사용자의 가입일이 오늘이면 (즉, 새로운 가입자면) 사용자의 `display_name`과 가입 축하 툿을 합니다.
- 트윙여의 로컬 타임라인을 지켜보다가 툿을 한 사용자의 가입일이 n주년이면 n주년 축하 툿을 합니다.
- 로컬 타임라인을 지켜보기 때문에 다른 인스턴스의 사용자에 대해서는 해당사항이 없습니다. 팔로우백 기능과 홈 타임라인을 이용하여 다른 인스턴스의 사용자에 대해서도 작동하도록 추가할 계획입니다. 언제일지는 기약이 없습니다.
- `display_name`을 사용하기 때문에 `display_name`이 등록되지 않은 계정에 대해서는 정상적으로 동작하지 않습니다. `username` 이나 다른 값을 사용하도록 변경이 될 지도?
- 해당 봇은 [트윙여](https://twingyeo.kr)의 규정을 존중하고 준수하며, 위반사항 또는 위반 의심사항이 있을 경우에는 [관리자](https://twingyeo.kr/@canor)에게 알려주시면 대단히 감사하겠습니다.
- 트윙여 조직의 트래디션: *소고기는 자유 소프트웨어가 아닙니다.*

------

#### Welcome new member of Mastodon instance [twingyeo.kr](https://twingyeo.kr) and n-th anniversary

- Watches local timeline and send congratulation message with `display_name` if account's `created_at` is today
- Watches local timeline and send congratulation message with `display_name` and `n`th year.
- This bot watches local timeline, which means it won't congratulate other member on different instance. I'm planning an update for members on other instances with follow-back and home timeline. No ETA tho.
- This bot uses `display_name` to send toot so if `display_name` is not set, it won't work properly. Maybe I should use `username` or something like that?
- This bot respects and complies to [twingyeo](https://twingyeo.kr)'s rule, please notify [admin](https://twingyeo.kr/@canor) asap if any violation or suspicious behaviour is observed.

------

### TMI

- 본 봇은 가정 내의 ~~Synology DS216j~~컴퓨터에서 구동중입니다. 따라서 다소 지연이 있거나 (드물지만) 가정에 인터넷 연결이 중단될 경우 작동하지 않을 수도 있습니다.
- ~~로컬에서 구동되기 때문에 트윙여 서버의 시간대와 약간(9시간 또는 8시간) 차이가 있습니다. 이 부분은 최우선 순위로 수정이 될 예정이나 정확한 예정일자는 없습니다.~~ 수정됨.

### Todo

- [x] 표준 시간대와 일치시키기
- [x] `display_name` 이 없을 경우 `username` 으로 fallback하기
- [x] 팔로우백 기능
- [x] 가입 일자 묻는 멘션에 가입일자 답해주기
- [ ] 멘션 내용 파악 및 답변 세분화하기(진행중)
