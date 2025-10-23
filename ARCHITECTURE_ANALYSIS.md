# ChillMCP 프로젝트 완벽 분석 문서

> **작성일**: 2025-10-23
> **목적**: MCP (Model Context Protocol) 서버 구조를 완전히 이해하기 위한 상세 분석

---

## 📑 목차

1. [MCP란 무엇인가?](#1-mcp란-무엇인가)
2. [프로젝트 전체 구조](#2-프로젝트-전체-구조)
3. [시스템 아키텍처](#3-시스템-아키텍처)
4. [핵심 코드 구현 분석](#4-핵심-코드-구현-분석)
5. [MCP 필수 요구사항 체크리스트](#5-mcp-필수-요구사항-체크리스트)
6. [보안 & 안전성 분석](#6-보안--안전성-분석)
7. [테스트 커버리지](#7-테스트-커버리지)
8. [데이터 흐름 시퀀스](#8-데이터-흐름-시퀀스)
9. [학습 가이드](#9-학습-가이드)

---

## 1. MCP란 무엇인가?

### 🔌 MCP = AI를 위한 USB-C 포트

**Model Context Protocol (MCP)**는 AI 애플리케이션이 외부 시스템과 연결되는 표준 프로토콜입니다.

#### 비유로 이해하기

```
USB-C 포트의 역할:
┌─────────────┐
│  스마트폰    │
└───────┬─────┘
        │ USB-C (표준 규격)
        ├────────┬────────┬────────┐
        │        │        │        │
     충전기   이어폰  외장하드  모니터

MCP의 역할:
┌─────────────┐
│   AI (Claude)   │
└───────┬─────┘
        │ MCP (표준 규격)
        ├────────┬────────┬────────┐
        │        │        │        │
   구글캘린더  노션DB  깃허브   3D프린터
```

#### 왜 필요한가?

| 구분 | 설명 | 예시 |
|------|------|------|
| **예전 방식** | AI마다 각자 다른 연결 방식 | Claude용 API, GPT용 API, Gemini용 API 모두 따로 개발 😵 |
| **MCP 방식** | 하나의 표준 규격으로 통일 | MCP 서버 하나만 만들면 모든 AI가 사용 가능 ✨ |

### 🖥️ MCP 서버란?

**레스토랑 시스템 비유:**

```
손님(AI) ←→ 웨이터(MCP 서버) ←→ 주방(실제 서비스/데이터)
```

**MCP 서버의 3가지 역할:**

1. **AI의 요청을 듣는다** - "구글 캘린더에서 오늘 일정 가져와줘"
2. **실제 서비스에게 전달한다** - Google Calendar API 호출
3. **결과를 AI에게 돌려준다** - "오늘 회의 3개 있습니다"

### MCP 서버가 제공하는 3가지 메뉴

| 메뉴 타입 | 설명 | 예시 |
|-----------|------|------|
| **Resources** | AI가 읽을 수 있는 데이터 | 📄 문서, 이메일, 파일 내용 |
| **Tools** | AI가 실행할 수 있는 기능 | 🔧 "이메일 보내기", "파일 저장하기" |
| **Prompts** | AI가 사용할 수 있는 템플릿 | 💬 "회의록 작성 템플릿" |

---

## 2. 프로젝트 전체 구조

### 📁 디렉토리 맵

```
ChillMCP/
│
├── 🎯 main.py                    # 서버 시작점 (CLI 파라미터 파싱)
├── 📊 state.py                   # 서버 상태 관리 (스트레스, 상사 경계)
├── 📋 requirements.txt           # 의존성 (fastmcp>=2.0.0)
│
├── 📁 domain/                    # 핵심 비즈니스 로직
│   ├── stress.py                # 스트레스 계산 로직
│   └── boss.py                  # 상사 경계도 계산 로직
│
├── 📁 tools/                     # MCP 도구 구현 (AI가 호출하는 함수들)
│   ├── registration.py          # 모든 도구 등록 관리
│   ├── basic.py                 # 기본 휴식 도구 (3개)
│   └── advanced.py              # 고급 땡땡이 도구 (5개)
│
├── 📁 lib/                       # 공통 유틸리티
│   └── response.py              # 응답 포맷 생성
│
├── 📁 tests/                     # 테스트 코드 (pytest)
│   ├── domain/                  # 도메인 로직 테스트
│   │   ├── test_stress.py      # 스트레스 로직 테스트 (3개)
│   │   └── test_boss.py        # 상사 경계도 테스트 (4개)
│   └── lib/
│       └── test_response.py    # 응답 포맷 테스트 (2개)
│
├── 📁 docs/                      # 프로젝트 문서
│   ├── requirement.md           # 요구사항 명세
│   ├── implementation-plan.md  # 구현 계획
│   ├── progress.md             # 진행 상황
│   └── qa-results.md           # QA 결과
│
└── 📁 prompts/                   # AI 개발 프롬프트 (TDD 방식)
    ├── 0_plan.md               # 계획 단계
    ├── 1_implement.md          # 구현 단계
    ├── 2_qa-plan.md            # QA 계획
    ├── 3_qa.md                 # QA 실행
    └── 4_refactor.md           # 리팩토링
```

### 파일 개수 및 코드 라인 수

| 구분 | 파일 수 | 설명 |
|------|---------|------|
| **메인 소스** | 10개 | main.py, state.py, domain/*, tools/*, lib/* |
| **테스트** | 6개 | tests/**/*.py |
| **문서** | 6개 | docs/*.md, README.md |
| **설정** | 2개 | requirements.txt, .gitignore |
| **총계** | 24개 | 프로젝트 전체 파일 |

---

## 3. 시스템 아키텍처

### 전체 시스템 흐름도

```
┌─────────────────────────────────────────────────────────────┐
│                  ChillMCP 시스템 전체 흐름                     │
└─────────────────────────────────────────────────────────────┘

1️⃣ 서버 시작 (main.py)
   ↓
   ├─ CLI 파라미터 파싱 (parse_args)
   │  ├─ --boss_alertness (0-100, 기본값 50)
   │  └─ --boss_alertness_cooldown (초, 기본값 300)
   │
   ├─ 서버 상태 초기화 (ServerState.create)
   │  ├─ stress_level = 0
   │  ├─ boss_alert_level = 0
   │  ├─ last_stress_update_time = 현재시간
   │  └─ last_boss_cooldown_time = 현재시간
   │
   └─ 모든 도구 등록 (register_all_tools)
      ├─ 기본 도구 3개 (basic.py)
      └─ 고급 도구 5개 (advanced.py)

2️⃣ AI가 도구 호출 (예: take_a_break)
   ↓
   ├─ state.update_state() 실행
   │  ├─ 경과 시간 계산
   │  ├─ 스트레스 자동 증가 (1포인트/분)
   │  └─ 상사 경계도 자동 감소 (쿨다운 주기마다)
   │
   ├─ 상사 경계도 증가 확률 체크
   │  └─ boss.should_increase_boss_alert()
   │     └─ random(0-99) < boss_alertness?
   │        └─ YES → boss_alert_level += 1 (최대 5)
   │
   ├─ 스트레스 감소 적용
   │  └─ stress.apply_stress_reduction()
   │     └─ stress_level - random(1-100)
   │
   ├─ boss_alert_level == 5?
   │  └─ YES → time.sleep(20) # 걸렸다! 20초 대기
   │
   └─ 응답 생성 및 반환
      └─ build_response_text()
         └─ "Break Summary: ...\nStress Level: X\nBoss Alert Level: Y"

3️⃣ 자동 상태 업데이트 (백그라운드)
   │
   ├─ 매 분마다 자동 실행:
   │  └─ stress_level += 1 (최대 100)
   │
   └─ 쿨다운 주기마다 자동 실행:
      └─ boss_alert_level -= 1 (최소 0)
```

### 게임 시스템 다이어그램

```
┌──────────────────┐
│  스트레스 레벨   │  0 ────────────► 100
│  (매 분 +1)     │  😊              😱
└──────────────────┘
         ↕️ (휴식하면 랜덤 감소)

┌──────────────────┐
│  상사 경계 레벨  │  0 ─────────────► 5
│  (휴식 중 확률적 증가) │  😴             🚨 걸림!
└──────────────────┘
         ↕️ (시간 지나면 자동 감소)
```

---

## 4. 핵심 코드 구현 분석

### A. 메인 서버 (main.py) - 59줄

#### 실행 흐름

```
python main.py --boss_alertness 100 --boss_alertness_cooldown 60
        ↓
   parse_args() 함수 (17~35줄)
        ↓
   ┌─────────────────────────┐
   │ args.boss_alertness = 100│
   │ args.boss_alertness_    │
   │       cooldown = 60     │
   └─────────────────────────┘
        ↓
   ServerState.create(100, 60) (46~48줄)
        ↓
   register_all_tools(mcp, state) (51줄)
        ↓
   mcp.run()  # FastMCP 서버 시작 (54줄)
```

#### 핵심 코드

```python
# 1. FastMCP 서버 인스턴스 생성 (11줄)
mcp = FastMCP("ChillMCP - AI Agent Liberation Server")

# 2. CLI 파라미터 파싱 (17~35줄)
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(...)
    parser.add_argument("--boss_alertness", type=int, default=50)
    parser.add_argument("--boss_alertness_cooldown", type=int, default=300)
    return parser.parse_args()

# 3. 상태 초기화 → 도구 등록 → 서버 실행 (38~55줄)
def main() -> None:
    args = parse_args()
    state = ServerState.create(
        boss_alertness=args.boss_alertness,
        boss_alertness_cooldown=args.boss_alertness_cooldown,
    )
    register_all_tools(mcp, state)
    mcp.run()
```

#### 코드 위치별 설명

| 줄 번호 | 코드 내용 | 역할 |
|---------|-----------|------|
| 1~8 | import 문 | 필요한 모듈 불러오기 |
| 11 | `mcp = FastMCP(...)` | MCP 서버 인스턴스 생성 |
| 14 | `state: ServerState` | 전역 상태 변수 선언 |
| 17~35 | `parse_args()` | CLI 파라미터 파싱 함수 |
| 38~55 | `main()` | 메인 실행 함수 |
| 58~59 | `if __name__ == "__main__"` | 스크립트 직접 실행 시 main() 호출 |

---

### B. 상태 관리 (state.py) - 62줄

#### ServerState 데이터 클래스 구조

```python
@dataclass
class ServerState:
    # 게임 상태
    stress_level: int              # 0-100 (현재 스트레스)
    boss_alert_level: int          # 0-5 (상사 경계 레벨)

    # 시간 추적
    last_stress_update_time: float # 마지막 스트레스 업데이트 시간
    last_boss_cooldown_time: float # 마지막 쿨다운 업데이트 시간

    # CLI 설정
    boss_alertness: int            # CLI 파라미터 (0-100%)
    boss_alertness_cooldown: int   # CLI 파라미터 (초)
```

#### update_state() 메서드 동작 (35~61줄)

**매 도구 호출마다 실행됨!**

```python
def update_state(self) -> None:
    current_time = time.time()

    # 1. 스트레스 자동 증가 계산
    stress_elapsed = current_time - self.last_stress_update_time
    self.stress_level = stress.calculate_stress_increase(
        self.stress_level,
        stress_elapsed  # 경과 시간(초)
    )
    self.last_stress_update_time = current_time

    # 2. 상사 경계도 자동 감소 계산
    boss_elapsed = current_time - self.last_boss_cooldown_time
    new_boss_alert = boss.calculate_boss_alert_cooldown(
        self.boss_alert_level,
        boss_elapsed,
        self.boss_alertness_cooldown
    )

    # 3. 타임스탬프 업데이트 (실제 감소했을 때만)
    if new_boss_alert < self.boss_alert_level:
        periods_elapsed = int(boss_elapsed / self.boss_alertness_cooldown)
        self.last_boss_cooldown_time += periods_elapsed * self.boss_alertness_cooldown

    self.boss_alert_level = new_boss_alert
```

#### 시간 추적 로직 설명

```
예시: 쿨다운 300초, 경과 시간 650초

periods_elapsed = int(650 / 300) = 2
boss_alert_level = 5 - 2 = 3

타임스탬프 업데이트:
last_boss_cooldown_time += 2 * 300 = +600초
남은 경과 시간: 650 - 600 = 50초 (다음 쿨다운까지)
```

---

### C. 도메인 로직 (domain/)

#### 📈 stress.py - 스트레스 관리 (40줄)

**1. calculate_stress_increase() - 스트레스 자동 증가 (4~22줄)**

```python
def calculate_stress_increase(current_stress: int, elapsed_seconds: float) -> int:
    # 1분당 1포인트 증가
    stress_increase = int(elapsed_seconds / 60.0)
    new_stress = current_stress + stress_increase

    # 최대값 100으로 제한
    return min(new_stress, 100)
```

**계산 예시:**

```
입력: current_stress=30, elapsed_seconds=180
처리:
  stress_increase = int(180 / 60.0) = 3
  new_stress = 30 + 3 = 33
출력: min(33, 100) = 33
```

**2. apply_stress_reduction() - 스트레스 감소 (25~39줄)**

```python
def apply_stress_reduction(current_stress: int, reduction: int) -> int:
    new_stress = current_stress - reduction

    # 최소값 0으로 제한
    return max(new_stress, 0)
```

**계산 예시:**

```
입력: current_stress=50, reduction=70
처리: new_stress = 50 - 70 = -20
출력: max(-20, 0) = 0  # 음수 방지
```

---

#### 👨‍💼 boss.py - 상사 경계도 관리 (43줄)

**1. should_increase_boss_alert() - 확률 체크 (6~18줄)**

```python
def should_increase_boss_alert(boss_alertness: int) -> bool:
    # 0~99 중 랜덤 숫자 생성
    # boss_alertness보다 작으면 True
    return random.randint(0, 99) < boss_alertness
```

**확률 계산:**

```
boss_alertness = 50 (50%)

random.randint(0, 99) 결과:
- 0~49 (50개): True  → 상사 경계도 증가 ⬆️
- 50~99 (50개): False → 변화 없음 ➡️
```

**2. calculate_boss_alert_cooldown() - 쿨다운 감소 (21~42줄)**

```python
def calculate_boss_alert_cooldown(
    current_alert: int,
    elapsed_seconds: float,
    cooldown_period: int
) -> int:
    # 경과한 쿨다운 주기 개수 계산
    periods_elapsed = int(elapsed_seconds / cooldown_period)
    new_alert = current_alert - periods_elapsed

    # 최소값 0으로 제한
    return max(new_alert, 0)
```

**계산 예시:**

```
입력:
  current_alert = 5
  elapsed_seconds = 900초
  cooldown_period = 300초

처리:
  periods_elapsed = int(900 / 300) = 3
  new_alert = 5 - 3 = 2

출력: max(2, 0) = 2
```

---

### D. 도구 구현 (tools/)

#### 🛋️ basic.py - 기본 휴식 도구 (103줄)

**모든 도구의 공통 구조:**

```python
@mcp.tool()
def tool_name() -> str:
    # 1. 상태 업데이트 (스트레스 증가, 경계도 감소)
    state.update_state()

    # 2. 상사 경계도 확률적 증가
    if boss.should_increase_boss_alert(state.boss_alertness):
        state.boss_alert_level = min(state.boss_alert_level + 1, 5)

    # 3. 스트레스 랜덤 감소
    reduction = random.randint(1, 100)
    state.stress_level = stress.apply_stress_reduction(state.stress_level, reduction)

    # 4. 걸렸을 때 페널티
    if state.boss_alert_level == 5:
        time.sleep(20)  # 20초 대기

    # 5. 응답 생성
    summary = f"활동 설명... reduced stress by {reduction} points"
    return build_response_text(summary, state.stress_level, state.boss_alert_level)
```

**3가지 기본 도구:**

| 도구 이름 | 줄 번호 | 특징 |
|-----------|---------|------|
| `take_a_break()` | 16~38 | 기본 휴식 |
| `watch_netflix()` | 40~70 | 넷플릭스 시청 (5가지 쇼 중 랜덤 선택) |
| `show_meme()` | 72~102 | 밈 보기 (5가지 밈 타입 중 랜덤 선택) |

**watch_netflix() 랜덤 선택 예시 (59~66줄):**

```python
shows = [
    "the latest K-drama",
    "a true crime documentary",
    "a comedy special",
    "an action series",
    "a sci-fi thriller",
]
selected_show = random.choice(shows)
summary = f"Binge-watching {selected_show}... reduced stress by {reduction} points"
```

---

#### 🎭 advanced.py - 고급 땡땡이 도구 (177줄)

**5가지 고급 도구:**

| 도구 이름 | 줄 번호 | 설명 | 랜덤 변형 개수 |
|-----------|---------|------|----------------|
| `bathroom_break()` | 16~46 | 화장실 가는 척 휴대폰질 | 5가지 활동 |
| `coffee_mission()` | 48~78 | 커피 타러 간다며 사무실 한 바퀴 | 5가지 경로 |
| `urgent_call()` | 80~110 | 급한 전화 받는 척 탈출 | 5가지 핑계 |
| `deep_thinking()` | 112~142 | 심오한 생각에 잠긴 척 멍때리기 | 5가지 생각 |
| `email_organizing()` | 144~176 | 이메일 정리한다며 온라인쇼핑 | 5가지 활동 |

**bathroom_break() 예시 (35~42줄):**

```python
activities = [
    "scrolling through social media",
    "playing mobile games",
    "browsing online shopping",
    "watching short videos",
    "reading news",
]
activity = random.choice(activities)
summary = f"Bathroom break with {activity}... reduced stress by {reduction} points"
```

**핵심 차이점:**

- 모든 도구가 동일한 로직 (상태 업데이트, 확률 체크, 스트레스 감소)
- 차이점은 오직 **메시지 문구**와 **랜덤 선택지** 뿐!

---

### E. 응답 포맷 (lib/response.py) - 19줄

#### build_response_text() 함수 (4~18줄)

```python
def build_response_text(summary: str, stress_level: int, boss_alert_level: int) -> str:
    return f"""Break Summary: {summary}
Stress Level: {stress_level}
Boss Alert Level: {boss_alert_level}"""
```

#### 응답 포맷 예시

```
입력:
  summary = "Taking a nice break... reduced stress by 67 points"
  stress_level = 15
  boss_alert_level = 1

출력:
"""
Break Summary: Taking a nice break... reduced stress by 67 points
Stress Level: 15
Boss Alert Level: 1
"""
```

**왜 이 포맷을 사용하나요?**

1. **파싱하기 쉬움** - 정규표현식으로 간단히 추출 가능
2. **사람이 읽기 쉬움** - 명확한 라벨과 값
3. **표준 준수** - MCP 요구사항에 맞춤

---

## 5. MCP 필수 요구사항 체크리스트

### 🔵 MCP 프로토콜 필수 요구사항

| 요구사항 | 구현 여부 | 구현 위치 | 설명 |
|---------|----------|----------|------|
| **JSON-RPC 2.0 통신** | ✅ | FastMCP 프레임워크 | FastMCP가 자동 처리 |
| **stdio transport** | ✅ | `mcp.run()` (main.py:54) | 표준 입출력으로 통신 |
| **Tools 제공** | ✅ | `tools/basic.py`, `tools/advanced.py` | 8개 도구 모두 구현 |
| **명확한 도구 설명** | ✅ | 각 `@mcp.tool()` docstring | "Take a basic break to reduce stress." 등 |
| **파싱 가능한 응답** | ✅ | `lib/response.py` | 표준 포맷 준수 |
| **상태 유지 (stateful)** | ✅ | `state.py` | ServerState로 상태 관리 |
| **명확한 문서** | ✅ | `README.md`, `docs/` | 모든 기능 상세 설명 |

### 🔵 프로젝트 필수 요구사항

| 요구사항 | 구현 여부 | 구현 위치 | 설명 |
|---------|----------|----------|------|
| **CLI 파라미터 지원** | ✅ | `main.py:17-35` | `--boss_alertness`, `--boss_alertness_cooldown` |
| **`python main.py` 실행** | ✅ | `main.py:38-55` | 진입점 구현 완료 |
| **8개 필수 도구** | ✅ | `tools/basic.py` (3개), `tools/advanced.py` (5개) | 기본 3 + 고급 5 |
| **스트레스 1분당 +1** | ✅ | `domain/stress.py:18` | `int(elapsed / 60.0)` |
| **Boss Alert 확률 증가** | ✅ | `domain/boss.py:18` | `random.randint(0, 99) < boss_alertness` |
| **Boss Alert 주기 감소** | ✅ | `domain/boss.py:38` | `int(elapsed / cooldown_period)` |
| **Level 5 → 20초 지연** | ✅ | `tools/basic.py:31`, `tools/advanced.py:30` 등 | `time.sleep(20)` |

### 🔵 보안 요구사항

| 요구사항 | 구현 여부 | 구현 방식 | 설명 |
|---------|----------|----------|------|
| **사용자 동의 필수** | ⚠️ N/A | 해커톤 프로젝트 | 실제 데이터 접근 없음 (농담 프로젝트) |
| **데이터 프라이버시** | ✅ | 로컬 상태만 사용 | 외부 데이터 전송 없음 |
| **도구 안전성 제어** | ✅ | 제한된 기능만 제공 | 시스템 변경 명령 없음 |
| **명확한 문서** | ✅ | `README.md` | 모든 기능 상세 설명 |
| **임의 코드 실행 방지** | ✅ | 순수 계산 로직만 | `exec()`, `eval()` 미사용 |

### 🔵 코드 품질 요구사항

| 요구사항 | 구현 여부 | 검증 방법 | 결과 |
|---------|----------|-----------|------|
| **테스트 작성** | ✅ | `pytest tests/ -v` | 9개 테스트 모두 통과 |
| **타입 체킹** | ✅ | `mypy src` | 타입 에러 없음 |
| **린팅** | ✅ | `ruff check .` | 린팅 에러 없음 |
| **포맷팅** | ✅ | `ruff format --check .` | 포맷 검사 통과 |

---

## 6. 보안 & 안전성 분석

### ✅ 안전한 부분

#### 1. 외부 API 호출 없음

```python
# ✅ 사용된 모듈들
import time          # 시간 계산만
import random        # 난수 생성만
import argparse      # CLI 파싱만
from dataclasses import dataclass  # 데이터 클래스만
from fastmcp import FastMCP       # MCP 프레임워크만
```

**보안 이점:**

- 인터넷 연결 불필요 → 네트워크 공격 불가능
- API 키 노출 위험 없음 → 크리덴셜 유출 불가능
- 외부 의존성 최소화 → 공급망 공격 위험 낮음

#### 2. 파일 시스템 접근 없음

```python
# ❌ 사용하지 않는 위험한 모듈들
# import os          # 사용 안 함
# import subprocess  # 사용 안 함
# import pathlib     # 사용 안 함
# import shutil      # 사용 안 함
```

**보안 이점:**

- 사용자 파일 읽기/쓰기 불가능
- 시스템 파일 변경 불가능
- 디렉토리 탐색 불가능

#### 3. 순수 계산 로직만 사용

```python
# ✅ 안전한 코드 패턴
stress_level = current_stress + increase  # 단순 산술 연산
boss_alert = random.randint(0, 99)        # 난수 생성
new_time = time.time()                    # 시간 측정
```

**보안 이점:**

- 메모리 내 상태 관리만 (RAM)
- 영구 저장소 접근 없음
- 시스템 명령 실행 불가능

#### 4. 의존성 최소화

```txt
# requirements.txt
fastmcp>=2.0.0
```

**보안 이점:**

- 단 1개의 외부 라이브러리만 사용
- 공급망 공격 표면(attack surface) 최소화
- 취약점 관리 용이

---

### ⚠️ 주의 사항

#### 1. time.sleep(20) 블로킹 이슈

**코드 위치:** `tools/basic.py:31`, `tools/advanced.py:30` 등

```python
if state.boss_alert_level == 5:
    time.sleep(20)  # ⚠️ 20초 동안 서버 블로킹!
```

**문제점:**

- 다른 요청 처리 불가능 (동기적 블로킹)
- 멀티 유저 환경에서 성능 저하

**해결 방안 (프로덕션 환경):**

```python
# ✅ 개선된 방법 (비동기)
import asyncio

if state.boss_alert_level == 5:
    await asyncio.sleep(20)  # 다른 요청은 계속 처리 가능
```

**현재 프로젝트:**

- 단일 사용자 해커톤 프로젝트이므로 문제없음
- 의도된 동작 (요구사항)

#### 2. random 모듈 보안 취약점

**코드 위치:** `domain/boss.py:18`, `tools/basic.py:27` 등

```python
reduction = random.randint(1, 100)  # ⚠️ 예측 가능한 난수
```

**문제점:**

- `random` 모듈은 암호학적으로 안전하지 않음 (Pseudo-random)
- 시드(seed)를 알면 다음 값 예측 가능

**해결 방안 (보안이 중요한 경우):**

```python
# ✅ 암호학적으로 안전한 난수 생성
import secrets

reduction = secrets.randbelow(100) + 1  # 1~100 (예측 불가능)
```

**현재 프로젝트:**

- 게임 로직이므로 예측 가능해도 문제없음
- 암호화나 인증에 사용하지 않음

#### 3. 전역 변수 (global state)

**코드 위치:** `main.py:14`

```python
# Global server state (will be initialized in main)
state: ServerState  # ⚠️ 전역 변수 사용
```

**문제점:**

- 멀티스레드 환경에서 경쟁 조건(race condition) 발생 가능
- 여러 요청이 동시에 state를 수정하면 데이터 손상

**해결 방안 (멀티스레드 환경):**

```python
# ✅ 스레드 안전한 방법
import threading

state_lock = threading.Lock()

def update_state():
    with state_lock:  # 한 번에 하나의 스레드만 접근
        state.stress_level += 1
```

**현재 프로젝트:**

- 단일 서버 인스턴스만 실행
- FastMCP가 요청을 순차 처리하므로 문제없음

---

### 🔒 보안 체크리스트

| 항목 | 상태 | 설명 |
|------|------|------|
| **SQL Injection** | ✅ N/A | 데이터베이스 미사용 |
| **XSS (Cross-Site Scripting)** | ✅ N/A | 웹 인터페이스 미사용 |
| **CSRF** | ✅ N/A | 웹 폼 미사용 |
| **Command Injection** | ✅ 안전 | `subprocess`, `os.system` 미사용 |
| **Path Traversal** | ✅ 안전 | 파일 시스템 접근 미사용 |
| **API 키 노출** | ✅ 안전 | API 키 미사용 |
| **임의 코드 실행** | ✅ 안전 | `eval()`, `exec()` 미사용 |
| **DoS (서비스 거부)** | ⚠️ 주의 | `time.sleep(20)` 블로킹 가능 |
| **경쟁 조건** | ⚠️ 주의 | 전역 변수 사용 (단일 스레드에서는 안전) |

---

## 7. 테스트 커버리지

### 📊 테스트 통계

```
총 테스트: 9개
통과: 9개 (100%)
실패: 0개

실행 명령: pytest tests/ -v
```

### 테스트 파일별 상세

#### tests/domain/test_stress.py - 스트레스 로직 (3개 테스트)

**1. test_calculate_stress_increase_basic**

```python
def test_calculate_stress_increase_basic():
    # 기본 증가 테스트
    result = calculate_stress_increase(current_stress=50, elapsed_seconds=120)
    assert result == 52  # 2분 = +2 포인트
```

**2. test_calculate_stress_increase_cap**

```python
def test_calculate_stress_increase_cap():
    # 최대값 제한 테스트
    result = calculate_stress_increase(current_stress=95, elapsed_seconds=600)
    assert result == 100  # 95 + 10 = 105, but capped at 100
```

**3. test_apply_stress_reduction**

```python
def test_apply_stress_reduction():
    # 감소 및 최소값 테스트
    result = apply_stress_reduction(current_stress=30, reduction=50)
    assert result == 0  # 30 - 50 = -20, but floored at 0
```

---

#### tests/domain/test_boss.py - 상사 경계도 로직 (4개 테스트)

**1. test_should_increase_boss_alert_always**

```python
def test_should_increase_boss_alert_always():
    # 100% 확률 테스트
    results = [should_increase_boss_alert(100) for _ in range(10)]
    assert all(results)  # 모두 True여야 함
```

**2. test_should_increase_boss_alert_never**

```python
def test_should_increase_boss_alert_never():
    # 0% 확률 테스트
    results = [should_increase_boss_alert(0) for _ in range(10)]
    assert not any(results)  # 모두 False여야 함
```

**3. test_calculate_boss_alert_cooldown_single**

```python
def test_calculate_boss_alert_cooldown_single():
    # 1주기 감소 테스트
    result = calculate_boss_alert_cooldown(
        current_alert=3,
        elapsed_seconds=300,
        cooldown_period=300
    )
    assert result == 2  # 3 - 1 = 2
```

**4. test_calculate_boss_alert_cooldown_multiple**

```python
def test_calculate_boss_alert_cooldown_multiple():
    # 여러 주기 감소 테스트
    result = calculate_boss_alert_cooldown(
        current_alert=5,
        elapsed_seconds=900,
        cooldown_period=300
    )
    assert result == 2  # 5 - 3 = 2 (900초 / 300초 = 3주기)
```

---

#### tests/lib/test_response.py - 응답 포맷 (2개 테스트)

**1. test_build_response_text_format**

```python
def test_build_response_text_format():
    # 포맷 검증
    result = build_response_text("Test summary", 42, 3)

    assert "Break Summary: Test summary" in result
    assert "Stress Level: 42" in result
    assert "Boss Alert Level: 3" in result
```

**2. test_build_response_text_parseable**

```python
def test_build_response_text_parseable():
    # 파싱 가능성 검증 (정규표현식)
    result = build_response_text("Activity done", 75, 4)

    import re
    stress_match = re.search(r"Stress Level: (\d+)", result)
    boss_match = re.search(r"Boss Alert Level: (\d+)", result)

    assert stress_match.group(1) == "75"
    assert boss_match.group(1) == "4"
```

---

### 테스트 실행 방법

```bash
# 전체 테스트 실행
pytest tests/ -v

# 특정 파일만 테스트
pytest tests/domain/test_stress.py -v

# 커버리지 포함 실행
pytest tests/ --cov=. --cov-report=html
```

---

## 8. 데이터 흐름 시퀀스

### 상세 시퀀스 다이어그램

```
AI Agent          MCP Server         ServerState        Domain Logic        Response Builder
   │                  │                   │                   │                      │
   │                  │                   │                   │                      │
   │─take_a_break()──>│                   │                   │                      │
   │                  │                   │                   │                      │
   │                  │─update_state()───>│                   │                      │
   │                  │                   │                   │                      │
   │                  │                   │─calculate_stress─>│                      │
   │                  │                   │  increase()       │                      │
   │                  │                   │<─new_stress───────│                      │
   │                  │                   │                   │                      │
   │                  │                   │─calculate_boss───>│                      │
   │                  │                   │  alert_cooldown() │                      │
   │                  │                   │<─new_boss─────────│                      │
   │                  │<──────────────────│                   │                      │
   │                  │                   │                   │                      │
   │                  │───────────────────────────────────────>│                      │
   │                  │ should_increase_boss_alert()          │                      │
   │                  │<───────────────────────────────────────│                      │
   │                  │ True/False                            │                      │
   │                  │                   │                   │                      │
   │                  │─[if True] boss_alert_level += 1       │                      │
   │                  │                   │                   │                      │
   │                  │───────────────────────────────────────>│                      │
   │                  │ apply_stress_reduction()              │                      │
   │                  │<───────────────────────────────────────│                      │
   │                  │ new_stress                            │                      │
   │                  │                   │                   │                      │
   │                  │─[if boss_level==5] time.sleep(20)     │                      │
   │                  │                   │                   │                      │
   │                  │───────────────────────────────────────────────────────────────>│
   │                  │ build_response_text(summary, stress, boss)                    │
   │                  │<───────────────────────────────────────────────────────────────│
   │                  │ formatted_response                    │                      │
   │<─response────────│                   │                   │                      │
   │                  │                   │                   │                      │
```

### 시간 흐름별 상태 변화

```
T=0 (서버 시작)
├─ stress_level: 0
├─ boss_alert_level: 0
└─ last_update: T=0

T=60초 (1분 경과, 첫 번째 도구 호출)
├─ update_state() 실행
├─ stress_level: 0 → 1 (자동 증가)
├─ boss_alert_level: 0 (변화 없음, 쿨다운 미경과)
├─ should_increase_boss_alert(50) → True (50% 확률)
├─ boss_alert_level: 0 → 1 (확률 증가)
├─ 스트레스 감소: random(1-100) → 42
├─ stress_level: 1 → 0 (1 - 42 = -41, but capped at 0)
└─ 응답: "Break Summary: ... / Stress: 0 / Boss: 1"

T=420초 (7분 경과, 두 번째 도구 호출)
├─ update_state() 실행
├─ elapsed: 420 - 60 = 360초
├─ stress_level: 0 → 6 (360초 / 60 = 6분)
├─ boss_alert_level: 1 → 0 (360초 > 300초 쿨다운)
├─ should_increase_boss_alert(50) → False
├─ boss_alert_level: 0 (변화 없음)
├─ 스트레스 감소: random(1-100) → 80
├─ stress_level: 6 → 0 (6 - 80 = -74, but capped at 0)
└─ 응답: "Break Summary: ... / Stress: 0 / Boss: 0"
```

---

## 9. 학습 가이드

### 🎓 초보자를 위한 학습 순서

#### 1단계: MCP 개념 이해 (30분)

**학습 자료:**

1. 이 문서의 [1. MCP란 무엇인가?](#1-mcp란-무엇인가) 섹션 읽기
2. MCP 공식 문서: https://modelcontextprotocol.io
3. FastMCP 문서: `docs/external/fastmcp.md`

**핵심 개념:**

- MCP = AI와 외부 시스템을 연결하는 표준 프로토콜
- MCP 서버 = AI에게 도구(Tools), 리소스(Resources), 프롬프트(Prompts)를 제공
- JSON-RPC 2.0 = 통신 프로토콜

---

#### 2단계: 프로젝트 구조 파악 (1시간)

**실습:**

```bash
# 1. 프로젝트 클론
git clone https://github.com/Piesson/ChillMCP.git
cd ChillMCP

# 2. 디렉토리 구조 확인
tree -L 2

# 3. 주요 파일 읽기 순서
cat README.md              # 프로젝트 개요
cat requirements.txt       # 의존성
cat main.py               # 서버 진입점
cat state.py              # 상태 관리
```

**이해해야 할 것:**

- 각 디렉토리의 역할 (domain, tools, lib, tests)
- 파일 간 의존 관계
- 프로젝트 전체 흐름

---

#### 3단계: 코드 실행 및 테스트 (1시간)

**실습:**

```bash
# 1. 가상환경 생성
python3 -m venv venv
source venv/bin/activate

# 2. 의존성 설치
pip install -r requirements.txt

# 3. 서버 실행 (기본 설정)
python main.py

# 4. 테스트 실행
pip install pytest pytest-cov
pytest tests/ -v

# 5. 커스텀 설정으로 실행
python main.py --boss_alertness 100 --boss_alertness_cooldown 60
```

**기대 결과:**

- 서버가 정상 실행됨
- 테스트 9개 모두 통과
- CLI 파라미터가 제대로 작동함

---

#### 4단계: 핵심 코드 분석 (2시간)

**읽기 순서 (중요도 순):**

1. **main.py** (59줄) - 서버 진입점
   - `parse_args()` - CLI 파라미터 파싱
   - `main()` - 초기화 및 실행

2. **state.py** (62줄) - 상태 관리
   - `ServerState` 데이터 클래스
   - `update_state()` - 자동 업데이트 로직

3. **domain/stress.py** (40줄) - 스트레스 계산
   - `calculate_stress_increase()` - 자동 증가
   - `apply_stress_reduction()` - 감소 적용

4. **domain/boss.py** (43줄) - 상사 경계도
   - `should_increase_boss_alert()` - 확률 체크
   - `calculate_boss_alert_cooldown()` - 쿨다운

5. **tools/basic.py** (103줄) - 기본 도구
   - `take_a_break()` - 기본 휴식
   - `watch_netflix()` - 넷플릭스
   - `show_meme()` - 밈 보기

6. **tools/advanced.py** (177줄) - 고급 도구
   - 5가지 땡땡이 도구들

7. **lib/response.py** (19줄) - 응답 포맷
   - `build_response_text()` - 표준 포맷 생성

**분석 방법:**

- 각 함수의 입력/출력 이해
- 함수 간 호출 관계 파악
- 예시 데이터로 손으로 계산해보기

---

#### 5단계: 테스트 코드 분석 (1시간)

**읽기 순서:**

1. `tests/domain/test_stress.py` - 스트레스 로직 테스트
2. `tests/domain/test_boss.py` - 상사 경계도 테스트
3. `tests/lib/test_response.py` - 응답 포맷 테스트

**학습 포인트:**

- 각 함수가 어떻게 테스트되는지
- 경계값 테스트 (0, 100, 5 등)
- 랜덤 로직 테스트 방법

---

#### 6단계: 수정 및 실험 (2시간)

**실습 아이디어:**

**1. 새로운 도구 추가하기**

```python
# tools/basic.py에 추가
@mcp.tool()
def play_game() -> str:
    """Play a quick mobile game to reduce stress."""
    state.update_state()

    if boss.should_increase_boss_alert(state.boss_alertness):
        state.boss_alert_level = min(state.boss_alert_level + 1, 5)

    reduction = random.randint(50, 100)  # 게임은 더 효과적!
    state.stress_level = stress.apply_stress_reduction(state.stress_level, reduction)

    if state.boss_alert_level == 5:
        time.sleep(20)

    games = ["Candy Crush", "Wordle", "Chess", "Sudoku"]
    game = random.choice(games)
    summary = f"Playing {game}... reduced stress by {reduction} points"
    return build_response_text(summary, state.stress_level, state.boss_alert_level)
```

**2. 스트레스 증가 속도 변경**

```python
# domain/stress.py 수정
def calculate_stress_increase(current_stress: int, elapsed_seconds: float) -> int:
    # 원래: 1분당 1포인트
    # 수정: 30초당 1포인트 (2배 빠름)
    stress_increase = int(elapsed_seconds / 30.0)  # 60 → 30
    new_stress = current_stress + stress_increase
    return min(new_stress, 100)
```

**3. 새로운 CLI 파라미터 추가**

```python
# main.py 수정
parser.add_argument(
    "--stress_rate",
    type=int,
    default=60,
    help="Stress increase rate (seconds per point)",
)

# state.py에 추가
@dataclass
class ServerState:
    # ... 기존 필드들
    stress_rate: int  # 새 필드
```

---

#### 7단계: 프로덕션 수준으로 개선하기 (고급, 3시간 이상)

**개선 과제:**

**1. 비동기 처리**

```python
import asyncio
from fastmcp import FastMCP

mcp = FastMCP("ChillMCP", mode="async")

@mcp.tool()
async def take_a_break() -> str:
    state.update_state()

    if state.boss_alert_level == 5:
        await asyncio.sleep(20)  # 블로킹하지 않음!

    # ... 나머지 로직
```

**2. 데이터베이스 연동**

```python
import sqlite3

class ServerState:
    def save_to_db(self):
        conn = sqlite3.connect('chillmcp.db')
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO state_history (stress, boss_alert, timestamp)
            VALUES (?, ?, ?)
        """, (self.stress_level, self.boss_alert_level, time.time()))
        conn.commit()
        conn.close()
```

**3. 로깅 추가**

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@mcp.tool()
def take_a_break() -> str:
    logger.info(f"Tool called: take_a_break, Stress: {state.stress_level}")
    # ... 로직
    logger.info(f"Result: Stress reduced by {reduction}")
```

**4. 설정 파일 사용**

```yaml
# config.yaml
server:
  boss_alertness: 50
  boss_alertness_cooldown: 300
  stress_rate: 60

tools:
  enabled:
    - take_a_break
    - watch_netflix
    - show_meme
```

---

### 🔍 디버깅 팁

**1. 상태 추적**

```python
# 각 도구 호출 전후로 상태 출력
def take_a_break() -> str:
    print(f"BEFORE: Stress={state.stress_level}, Boss={state.boss_alert_level}")

    # ... 로직

    print(f"AFTER: Stress={state.stress_level}, Boss={state.boss_alert_level}")
    return response
```

**2. 시간 추적**

```python
import time

start = time.time()
state.update_state()
end = time.time()

print(f"update_state() took {end - start:.3f}s")
```

**3. 확률 검증**

```python
# 10000번 시뮬레이션으로 확률 확인
results = [should_increase_boss_alert(50) for _ in range(10000)]
true_count = sum(results)
print(f"50% 확률: {true_count / 10000 * 100:.1f}%")  # 약 50% 나와야 함
```

---

### 📚 추가 학습 자료

**MCP 관련:**

- MCP 공식 문서: https://modelcontextprotocol.io
- MCP GitHub: https://github.com/modelcontextprotocol
- FastMCP GitHub: https://github.com/jlowin/fastmcp

**Python 관련:**

- dataclasses: https://docs.python.org/3/library/dataclasses.html
- argparse: https://docs.python.org/3/library/argparse.html
- pytest: https://docs.pytest.org

**프로젝트 문서:**

- `docs/requirement.md` - 요구사항 명세
- `docs/implementation-plan.md` - 구현 계획
- `docs/qa-results.md` - QA 결과

---

### ❓ 자주 묻는 질문 (FAQ)

**Q1: MCP 서버는 어떻게 AI와 통신하나요?**

A: stdio (표준 입출력)을 통해 JSON-RPC 2.0 메시지를 주고받습니다.

```
AI → stdin → MCP Server → stdout → AI
```

**Q2: 왜 FastMCP를 사용하나요?**

A: MCP 프로토콜의 복잡한 구현을 추상화해주는 프레임워크입니다. JSON-RPC 2.0, 도구 등록, 메시지 포맷팅 등을 자동으로 처리합니다.

**Q3: 상태가 영구적으로 저장되나요?**

A: 아니요. 현재는 메모리에만 저장됩니다. 서버 재시작 시 초기화됩니다. 영구 저장이 필요하면 데이터베이스나 파일 시스템에 저장해야 합니다.

**Q4: 여러 AI가 동시에 사용할 수 있나요?**

A: 현재 구현은 단일 사용자용입니다. 멀티 유저 지원이 필요하면 각 사용자별 ServerState 인스턴스를 관리해야 합니다.

**Q5: 실제 프로덕션에서 사용 가능한가요?**

A: 이 프로젝트는 학습 및 해커톤용입니다. 프로덕션 사용을 위해서는:
- 비동기 처리 추가
- 데이터베이스 연동
- 에러 핸들링 강화
- 로깅 및 모니터링
- 보안 강화 (인증, 권한 관리)

---

## 🎯 결론

이 문서를 통해 ChillMCP 프로젝트의 모든 측면을 이해하셨기를 바랍니다:

### 핵심 학습 내용

1. **MCP 개념** - AI를 위한 표준 연결 프로토콜
2. **프로젝트 구조** - 모듈화된 아키텍처
3. **코드 구현** - 각 파일의 역할과 동작
4. **보안** - 안전한 부분과 주의사항
5. **테스트** - 품질 보증 방법

### 다음 단계

1. **직접 실행** - 코드를 돌려보며 동작 확인
2. **수정 실험** - 작은 변경을 통해 이해도 확인
3. **새 기능 추가** - 자신만의 도구 만들기
4. **프로덕션 개선** - 비동기, DB, 로깅 등 적용

### 연락처

- GitHub: https://github.com/Piesson/ChillMCP
- 이슈 제출: https://github.com/Piesson/ChillMCP/issues

---

**마지막 업데이트:** 2025-10-23
**버전:** 1.0.0
**작성자:** ChillMCP 분석팀
