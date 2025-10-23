## ChillMCP 서버 구현 계획

### 1. 코드베이스 구조 설계

프로젝트의 확장성과 유지보수성을 위해 다음과 같은 구조를 제안합니다. 모든 구현은 이 구조를 따라야 합니다.

```
chillmcp/
├── .github/workflows/         # (선택) CI/CD 파이프라인 (lint, test, type-check)
│   └── ci.yml
├── src/
│   └── chillmcp/              # 메인 소스 코드 패키지
│       ├── __init__.py
│       ├── main.py            # 서버 진입점, MCP 인스턴스화, 도구 등록, CLI 파싱
│       ├── state.py           # ServerState 데이터 클래스 정의 (상태 관리 중앙화)
│       │
│       ├── domain/            # 순수 함수로 구성된 핵심 비즈니스 로직
│       │   ├── __init__.py
│       │   ├── stress.py      # 스트레스 계산 관련 순수 함수
│       │   └── boss.py        # '상사' 경계도 계산 관련 순수 함수
│       │
│       ├── tools/             # MCP 도구 구현
│       │   ├── __init__.py
│       │   ├── registration.py # 모든 도구를 서버에 등록하는 함수
│       │   ├── basic.py       # 기본 휴식 도구
│       │   └── advanced.py    # 고급 농땡이 도구
│       │
│       └── lib/               # 공통 유틸리티 및 헬퍼 함수
│           ├── __init__.py
│           ├── response.py    # 표준 응답 텍스트 포맷 생성 함수
│           └── time.py        # 시간 관련 헬퍼 함수
│
├── tests/                     # 모든 테스트 코드
│   ├── __init__.py
│   ├── domain/                # 도메인 로직 유닛 테스트
│   │   ├── test_stress.py
│   │   └── test_boss.py
│   └── lib/                   # 라이브러리 함수 유닛 테스트
│       └── test_response.py
│
├── pyproject.toml             # 프로젝트 의존성 및 빌드/품질 도구 설정
├── requirements.txt           # (pyproject.toml 기반으로 생성)
└── README.md
```

---

### 2. 단계별 구현 계획

#### **Step 1: 프로젝트 구조 생성 및 공통 라이브러리 초기 구현**

- **상세 지침:**
  1.  위에 명시된 `src/chillmcp`, `tests`를 포함한 모든 디렉터리 구조를 생성하세요. 각 디렉터리에 `__init__.py` 파일을 추가하여 파이썬 패키지로 만드세요.
  2.  `src/chillmcp/lib/response.py` 파일을 생성하세요.
  3.  해당 파일 안에 `build_response_text(summary: str, stress_level: int, boss_alert_level: int) -> str` 함수를 정의하세요. 이 함수는 요구사항에 명시된 "파싱 가능한 텍스트 규격"을 정확히 따르는 문자열을 반환해야 합니다.
      - 예: `f"...\n\nBreak Summary: {summary}\nStress Level: {stress_level}\nBoss Alert Level: {boss_alert_level}"`
- **Acceptance Test:**
  1.  프로젝트 루트에 모든 디렉터리와 파일이 정확히 생성되었는지 확인합니다.
  2.  Python 인터프리터에서 `from src.chillmcp.lib.response import build_response_text`가 에러 없이 실행되어야 합니다.
  3.  `build_response_text("test", 50, 2)` 호출 시, 반환된 문자열이 요구사항의 정규표현식으로 파싱 가능한지 확인합니다.

---

#### **Step 2: 코드 품질 및 테스트 환경 구축 (TDD 시작)**

- **상세 지침:**
  1.  프로젝트 루트에 `pyproject.toml` 파일을 생성하세요.
  2.  `[project]` 섹션에 `fastmcp`를 의존성으로 추가하세요.
  3.  개발 의존성(`[project.optional-dependencies.dev]`)으로 `pytest`, `mypy`, `ruff`를 추가하세요.
  4.  `[tool.ruff]`, `[tool.mypy]` 설정을 추가하여 린팅, 포맷팅, 타입 체킹 규칙을 구성하세요.
  5.  `tests/lib/test_response.py` 파일을 생성하세요.
  6.  **TDD:** `build_response_text` 함수에 대한 유닛 테스트를 작성하세요.
      - `test_build_response_format`: 함수가 생성한 문자열이 요구사항의 정규표현식 패턴 3개(`Break Summary`, `Stress Level`, `Boss Alert Level`) 모두와 일치하는지 검증하는 테스트를 추가하세요.
  7.  `pip install -e .[dev]` 명령으로 프로젝트를 설치하고, `pytest`를 실행하여 모든 테스트가 통과하는지 확인하세요.
  8.  `ruff check .`, `ruff format .`, `mypy src` 명령을 실행하여 코드 품질 검사를 통과하는지 확인하세요.
- **Acceptance Test:**
  1.  `pytest` 실행 시 모든 테스트가 성공(PASS)해야 합니다.
  2.  `ruff check .` 및 `mypy src` 실행 시 어떠한 에러도 출력되지 않아야 합니다.

---

#### **Step 3: 기본 MCP 서버 및 상태 관리 객체 구현**

- **상세 지침:**
  1.  `src/chillmcp/state.py` 파일을 생성하고, `dataclasses` 모듈을 사용하여 `ServerState` 클래스를 정의하세요. 이 클래스는 다음 필드를 포함해야 합니다.
      - `stress_level: int`
      - `boss_alert_level: int`
      - `last_stress_update_time: float` (초 단위 타임스탬프)
      - `last_boss_cooldown_time: float` (초 단위 타임스탬프)
      - `boss_alertness: int` (CLI 파라미터)
      - `boss_alertness_cooldown: int` (CLI 파라미터)
  2.  `src/chillmcp/main.py` 파일을 생성하세요.
  3.  `argparse`를 사용하여 `--boss_alertness`와 `--boss_alertness_cooldown` 커맨드라인 인자를 파싱하는 로직을 구현하세요. 기본값도 설정해야 합니다. (예: 50, 300)
  4.  `main` 함수에서 파싱된 인자와 현재 시간을 사용하여 `ServerState` 객체를 초기화하세요.
  5.  `FastMCP` 인스턴스를 생성하고, `stdio` transport를 사용하도록 설정하세요.
  6.  서버가 정상적으로 실행되는지 확인하기 위한 임시 `ping` 도구를 `main.py`에 직접 추가하세요. 이 도구는 "pong"을 반환합니다.
  7.  `mcp.run()`을 호출하여 서버를 실행하는 코드를 추가하세요.
- **Acceptance Test:**
  1.  `python -m src.chillmcp.main --help` 실행 시, `--boss_alertness`와 `--boss_alertness_cooldown` 옵션이 설명과 함께 표시되어야 합니다.
  2.  `python -m src.chillmcp.main`을 실행하여 서버가 에러 없이 시작되어야 합니다.
  3.  서버 실행 중, 다른 터미널에서 `{"jsonrpc": "2.0", "method": "ping", "id": 1}` 형식의 JSON 요청을 stdin으로 입력하면, stdout으로 `"pong"`이 포함된 응답이 출력되어야 합니다.

---

#### **Step 4: 핵심 도메인 로직 구현 (TDD, 병렬 진행 가능)**

- **상세 지침 (Task A - Stress Logic):**
  1.  **Test First:** `tests/domain/test_stress.py` 파일을 생성하세요.
      - `test_calculate_stress_increase_over_time`: 특정 시간이 지났을 때 스트레스가 `1분당 1포인트` 규칙에 따라 정확히 증가하는지 검증하는 테스트를 작성하세요.
      - `test_apply_stress_reduction`: 스트레스 감소량이 적용된 후, 결과 값이 0 미만으로 내려가지 않는지(최소 0) 검증하는 테스트를 작성하세요.
  2.  **Implementation:** `src/chillmcp/domain/stress.py` 파일을 생성하고 위 테스트를 통과하는 `calculate_stress_increase`, `apply_stress_reduction` 순수 함수들을 구현하세요.
- **상세 지침 (Task B - Boss Logic):**
  1.  **Test First:** `tests/domain/test_boss.py` 파일을 생성하세요.
      - `test_should_increase_boss_alert`: `boss_alertness` 확률(%)에 따라 `True` 또는 `False`를 반환하는지 검증하는 테스트를 작성하세요. (확률 100일 때 항상 True, 0일 때 항상 False)
      - `test_calculate_boss_alert_cooldown`: 특정 시간이 지났을 때 경계도가 `cooldown 주기`에 따라 정확히 감소하는지, 그리고 0 미만으로 내려가지 않는지 검증하는 테스트를 작성하세요.
  2.  **Implementation:** `src/chillmcp/domain/boss.py` 파일을 생성하고 위 테스트를 통과하는 `should_increase_boss_alert`, `calculate_boss_alert_cooldown` 순수 함수들을 구현하세요.
- **Acceptance Test:**
  1.  `pytest tests/domain/` 실행 시 `test_stress.py`와 `test_boss.py`의 모든 테스트가 통과해야 합니다.

---

#### **Step 5: 상태 업데이트 로직 및 도구 등록 구조 구현 (TDD)**

- **상세 지침:**
  1.  **TDD:** `ServerState` 객체를 직접 수정하는 상태 업데이트 함수에 대한 통합 테스트를 `tests/`에 추가하는 것을 고려하세요. (예: `tests/test_state_integration.py`)
  2.  `src/chillmcp/state.py`에 `update_state(self)` 메소드를 `ServerState` 클래스에 추가하세요. 이 메소드는 현재 시간을 기준으로 `stress.calculate_stress_increase`와 `boss.calculate_boss_alert_cooldown`을 호출하여 `self.stress_level`, `self.boss_alert_level` 및 관련 타임스탬프를 업데이트합니다.
  3.  `src/chillmcp/tools/registration.py` 파일을 생성하고 `register_all_tools(mcp: FastMCP, state: ServerState)` 함수를 정의하세요. 이 함수는 향후 모든 도구 모듈의 등록 함수를 호출하는 중앙 허브 역할을 합니다.
  4.  `main.py`에서 `ping` 도구를 제거하고, `register_all_tools`를 호출하도록 수정하세요.
- **Acceptance Test:**
  1.  `ServerState` 객체를 생성하고, `time.sleep()`으로 시간을 보낸 뒤 `update_state()`를 호출했을 때, 스트레스와 상사 경계도가 예상대로 변경되는지 검증하는 테스트가 통과해야 합니다.
  2.  `main.py` 실행 시 에러가 없어야 합니다. (아직 등록된 실제 도구는 없음)

---

#### **Step 6: 기본 및 고급 도구 구현 (병렬 진행 가능)**

- **상세 지침 (Task A - Basic Tools):**
  1.  `src/chillmcp/tools/basic.py` 파일을 생성하세요.
  2.  `register_basic_tools(mcp: FastMCP, state: ServerState)` 함수를 정의하세요.
  3.  이 함수 내에서 `take_a_break`, `watch_netflix`, `show_meme` 도구를 `@mcp.tool` 데코레이터를 사용하여 구현하세요.
  4.  각 도구의 로직은 다음 순서를 따라야 합니다.
      a. `state.update_state()`를 호출하여 현재 상태를 최신으로 만듭니다.
      b. `boss.should_increase_boss_alert`를 호출하여 상사 경계도를 올릴지 결정하고 `state`를 업데이트합니다. (최대 5)
      c. `stress.apply_stress_reduction`을 호출하여 `state`의 스트레스를 감소시킵니다.
      d. `state.boss_alert_level`이 5이면 `time.sleep(20)`을 실행합니다.
      e. `lib.response.build_response_text`를 사용하여 최종 응답 문자열을 생성하고, MCP 표준 응답 형식으로 래핑하여 반환합니다.
  5.  `tools/registration.py`에서 `register_basic_tools`를 호출하도록 추가하세요.
- **상세 지침 (Task B - Advanced Tools):**
  1.  `src/chillmcp/tools/advanced.py` 파일을 생성하고 `basic.py`와 동일한 구조로 `register_advanced_tools` 함수와 고급 도구들을 구현하세요. 로직 흐름은 기본 도구와 동일합니다.
  2.  `tools/registration.py`에서 `register_advanced_tools`를 호출하도록 추가하세요.
- **Acceptance Test:**
  1.  서버를 `--boss_alertness 100 --boss_alertness_cooldown 60`으로 실행합니다.
  2.  `take_a_break` 도구를 호출하면 응답의 `Boss Alert Level`이 이전보다 1 증가해야 합니다.
  3.  `Boss Alert Level`이 5가 될 때까지 도구를 반복 호출합니다.
  4.  다음에 도구를 호출했을 때, 응답이 오기까지 약 20초의 지연이 발생하는지 확인합니다.
  5.  서버를 60초 이상 방치한 뒤 도구를 다시 호출하면, `Stress Level`이 증가해 있고 `Boss Alert Level`이 감소해 있는지 확인합니다.
  6.  모든 도구의 응답은 요구사항의 정규표현식으로 완벽하게 파싱되어야 합니다.
