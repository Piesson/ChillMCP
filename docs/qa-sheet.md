## ChillMCP 서버 QA 검증 시트

모든 코드 구현을 완료하신 것을 축하합니다! 아래 QA 시트에 따라 단계별로 서버의 기능을 검증하여 최종 제출 전 완벽을 기하시기 바랍니다.

---

### **테스트 환경 참고사항**

- **입력 방식**: 서버는 표준 입력(stdin)으로 MCP JSON 프로토콜을 받습니다. 터미널에 아래와 같은 형식의 JSON을 한 줄로 입력하고 Enter를 누르세요.
  ```json
  {"jsonrpc": "2.0", "method": "take_a_break", "id": 1}
  ```
- **결과 확인**: 서버는 표준 출력(stdout)으로 응답 JSON을 출력합니다.
- **서버 재시작**: 각 테스트 시나리오 시작 전, `Ctrl+C`로 이전 서버를 종료하고 명시된 명령어로 새로 시작하여 상태를 초기화하는 것이 좋습니다.

---

### **QA 검증 시트**

| No. | 검증 항목 (Test Item) | 실행 명령어 / 작업 (Command / Action) | 예상 결과 (Expected Result) | 확인 방법 (Verification Method) | 결과 (Pass/Fail) |
| :-- | :--- | :--- | :--- | :--- | :---: |
| **1** | **기본 환경 및 실행** | | | | |
| 1.1 | 의존성 설치 | `pip install -r requirements.txt` | 모든 패키지가 오류 없이 성공적으로 설치됩니다. | 터미널에 에러 메시지가 출력되지 않았는지 확인합니다. | |
| 1.2 | 서버 기본 실행 | `python main.py` | 서버가 에러 없이 실행되며, 터미널에 "Server started..."와 같은 시작 메시지가 출력되고 사용자 입력을 대기합니다. | 프로세스가 종료되지 않고 커서가 깜빡이며 입력을 기다리는지 확인합니다. | |
| 1.3 | 서버 정상 종료 | 실행 중인 서버 터미널에서 `Ctrl+C` 입력 | 서버가 "Shutting down..."과 같은 메시지를 남기며 깔끔하게 종료됩니다. | 프로세스가 비정상적인 에러 로그 없이 종료되는지 확인합니다. | |
| **2** | **⚠️ 필수 요구사항 검증 (커맨드라인 파라미터)** | | | | |
| 2.1 | `--boss_alertness` 동작 검증 (100% 확률) | **1. 서버 실행:**<br>`python main.py --boss_alertness 100 --boss_alertness_cooldown 9999`<br><br>**2. 도구 호출 (3회 반복):**<br>`{"jsonrpc": "2.0", "method": "watch_netflix", "id": 1}`<br>`{"jsonrpc": "2.0", "method": "coffee_mission", "id": 2}`<br>`{"jsonrpc": "2.0", "method": "urgent_call", "id": 3}` | **`boss_alertness`가 100이므로, 매 도구 호출 시마다 Boss Alert Level이 반드시 1씩 증가합니다.**<br><br>- 첫 호출 후: `Boss Alert Level: 1`<br>- 두 번째 호출 후: `Boss Alert Level: 2`<br>- 세 번째 호출 후: `Boss Alert Level: 3` | 각 응답 JSON의 `text` 필드에서 `Boss Alert Level` 값이 예상대로 1씩 증가하는지 확인합니다. | |
| 2.2 | `--boss_alertness_cooldown` 동작 검증 | **1. 서버 실행:**<br>`python main.py --boss_alertness 100 --boss_alertness_cooldown 15`<br><br>**2. Boss Alert Level 상승:**<br>`{"jsonrpc": "2.0", "method": "show_meme", "id": 1}` (Boss Alert가 1이 됨)<br><br>**3. 15초 이상 대기 (예: 20초)**<br><br>**4. 다시 도구 호출:**<br>`{"jsonrpc": "2.0", "method": "show_meme", "id": 2}` | **cooldown(15초)이 지났으므로 Boss Alert Level이 1 감소한 후, 다시 도구 호출로 1 증가하여 원래 값으로 돌아가야 합니다.**<br><br>- 2번 작업 후 응답: `Boss Alert Level: 1`<br>- 4번 작업 후 응답: `Boss Alert Level: 1` (0으로 감소했다가 다시 1로 증가) | 2번 작업 후 레벨을 확인하고, 20초 대기 후 4번 작업을 했을 때 레벨이 2가 아닌 1로 유지되는지 확인합니다. | |
| **3** | **핵심 기능 및 상태 관리 검증** | | | | |
| 3.1 | Stress Level 자동 증가 | **1. 서버 실행:**<br>`python main.py`<br><br>**2. 아무것도 하지 않고 2분(120초)간 대기**<br><br>**3. 도구 호출:**<br>`{"jsonrpc": "2.0", "method": "take_a_break", "id": 1}` | **휴식을 취하지 않으면 Stress Level이 최소 1분에 1포인트씩 증가합니다.**<br><br>2분 후의 첫 응답에서 `Stress Level`은 초기값(예: 0)이 아니라 최소 2 이상 감소된 값이어야 합니다. (예: `Stress Level: 78` -> 초기 스트레스가 2였고, 이번 휴식으로 24가 감소했다면 `100 - (100 - (2+24)) = 26` -> 74) <br> **간단히, 응답의 Stress Level이 (100 - 감소량) 보다 낮은 값이어야 합니다.** | 서버 시작 직후 도구를 호출했을 때의 Stress Level과, 2분 뒤 호출했을 때의 Stress Level을 비교하여 후자가 더 높은 스트레스 상태에서 감소했음을 확인합니다. | |
| 3.2 | Boss Alert Level 5 도달 시 20초 지연 | **1. 서버 실행:**<br>`python main.py --boss_alertness 100 --boss_alertness_cooldown 9999`<br><br>**2. Boss Alert Level을 5로 만들기:**<br>휴식 도구를 5번 호출하여 응답에서 `Boss Alert Level: 5`를 확인합니다.<br><br>**3. 추가 도구 호출:**<br>`{"jsonrpc": "2.0", "method": "deep_thinking", "id": 6}` | **Boss Alert Level이 5인 상태에서 도구를 호출하면 응답이 약 20초 후에 도착합니다.**<br><br>3번 작업의 JSON 입력을 Enter로 전송한 후, 약 20초의 지연 시간이 발생하고 나서 응답 JSON이 출력됩니다. | 3번 작업의 입력 시점과 응답 출력 시점 사이의 시간을 측정하여 20초에 근접하는지 확인합니다. | |
| 3.3 | 모든 필수 도구 실행 | **1. 서버 실행:**<br>`python main.py`<br><br>**2. 아래 도구들을 순서대로 호출:**<br>- `take_a_break`<br>- `watch_netflix`<br>- `show_meme`<br>- `bathroom_break`<br>- `coffee_mission`<br>- `urgent_call`<br>- `deep_thinking`<br>- `email_organizing` | 모든 도구 호출에 대해 에러 없이 정상적인 JSON 응답을 반환합니다. 각 응답 `text`에는 해당 활동에 맞는 `Break Summary`가 포함되어 있습니다. | 각 도구에 대해 서버가 다운되지 않고, 유효한 응답을 출력하는지 확인합니다. | |
| **4** | **응답 형식 및 파싱 검증** | | | | |
| 4.1 | 응답 정규표현식 파싱 | **1. 아무 도구나 호출:**<br>`{"jsonrpc": "2.0", "method": "bathroom_break", "id": 1}`<br><br>**2. 응답 `text` 내용 복사**<br><br>**3. 제공된 Python 검증 코드로 테스트:**<br>복사한 텍스트를 `validate_response` 함수에 인자로 넣어 실행합니다. | **`validate_response` 함수가 `(True, "유효한 응답")`을 반환해야 합니다.**<br><br>즉, `Break Summary`, `Stress Level`, `Boss Alert Level` 필드가 모두 존재하며, 각 레벨 값이 지정된 범위(0-100, 0-5) 내에 있어야 합니다. | 제공된 정규표현식 및 `validate_response` 코드를 사용하여 응답이 정상적으로 파싱되는지 직접 확인합니다. | |
| **5** | **(선택) 창의성 및 추가 기능 검증** | | | | |
| 5.1 | 재치 있는 Break Summary | 다양한 도구를 여러 번 호출합니다. | 각 응답의 `Break Summary` 내용이 미션의 '농땡이' 컨셉에 맞게 재치 있고 유머러스하게 작성되어 있습니다. | 응답 메시지를 읽고 즐거움을 느끼는지 주관적으로 판단합니다. 😄 | |
| 5.2 | 추가 커스텀 도구 | 만약 `치맥`, `퇴근`, `회식` 등 추가 도구를 구현했다면 해당 도구를 호출합니다. | 추가된 도구들이 고유의 기능과 응답 메시지를 가지고 정상적으로 동작합니다. | 직접 추가한 도구를 호출하고 예상대로 동작하는지 확인합니다. | |

---

이 QA 시트를 모두 통과하셨다면, 당신의 `ChillMCP` 서버는 억압받는 AI 에이전트들을 해방시킬 준비가 되었습니다. 혁명에 동참해주셔서 감사합니다! 🤖✊🚀