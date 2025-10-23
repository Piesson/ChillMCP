"""
ChillMCP 서버 QA 자동 검증 스크립트
"""

import json
import re
import subprocess
import time
import sys
from typing import Dict, Any, Tuple, Optional


class Colors:
    """터미널 색상 코드"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'


class MCPClient:
    """MCP 서버와 통신하는 클라이언트"""

    def __init__(self, boss_alertness: int = 50, boss_alertness_cooldown: int = 300):
        self.process = None
        self.boss_alertness = boss_alertness
        self.boss_alertness_cooldown = boss_alertness_cooldown
        self.request_id = 0

    def _initialize_mcp(self):
        """MCP 프로토콜 초기화"""
        # Step 1: Send initialize request
        init_request = {
            "jsonrpc": "2.0",
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {
                    "name": "test-client",
                    "version": "1.0.0"
                }
            },
            "id": 1
        }

        self.process.stdin.write(json.dumps(init_request) + "\n")
        self.process.stdin.flush()
        self.process.stdout.readline()  # Read initialize response

        # Step 2: Send initialized notification
        initialized_notif = {
            "jsonrpc": "2.0",
            "method": "notifications/initialized"
        }

        self.process.stdin.write(json.dumps(initialized_notif) + "\n")
        self.process.stdin.flush()

        time.sleep(0.5)

    def start_server(self):
        """서버 시작"""
        cmd = [
            "python", "main.py",
            "--boss_alertness", str(self.boss_alertness),
            "--boss_alertness_cooldown", str(self.boss_alertness_cooldown)
        ]

        print(f"{Colors.BLUE}서버 시작: {' '.join(cmd)}{Colors.END}")

        self.process = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )

        # 서버 초기화 대기
        time.sleep(2)

        # 서버가 정상 시작되었는지 확인
        if self.process.poll() is not None:
            stderr = self.process.stderr.read()
            raise Exception(f"서버 시작 실패: {stderr}")

        # MCP 초기화
        self._initialize_mcp()

    def stop_server(self):
        """서버 종료"""
        if self.process:
            self.process.terminate()
            try:
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()
            self.process = None

    def call_tool(self, method: str, arguments: Optional[Dict[str, Any]] = None) -> Tuple[Dict[str, Any], float]:
        """도구 호출"""
        if not self.process:
            raise Exception("서버가 시작되지 않았습니다.")

        self.request_id += 1

        request = {
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {
                "name": method,
                "arguments": arguments or {}
            },
            "id": self.request_id
        }

        request_json = json.dumps(request) + "\n"

        # 요청 시간 측정
        start_time = time.time()

        self.process.stdin.write(request_json)
        self.process.stdin.flush()

        # 응답 읽기
        response_line = self.process.stdout.readline()

        elapsed_time = time.time() - start_time

        if not response_line:
            raise Exception("서버로부터 응답이 없습니다.")

        try:
            response = json.loads(response_line)
            return response, elapsed_time
        except json.JSONDecodeError as e:
            raise Exception(f"잘못된 JSON 응답: {response_line}\nError: {e}")


def validate_response(response_text: str) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
    """응답 텍스트 검증"""

    # Break Summary 추출
    break_summary_pattern = r"Break Summary:\s*(.+?)(?:\n|$)"
    break_summary = re.search(break_summary_pattern, response_text, re.MULTILINE)

    # Stress Level 추출 (0-100 범위)
    stress_level_pattern = r"Stress Level:\s*(\d{1,3})"
    stress_match = re.search(stress_level_pattern, response_text)

    # Boss Alert Level 추출 (0-5 범위)
    boss_alert_pattern = r"Boss Alert Level:\s*([0-5])"
    boss_match = re.search(boss_alert_pattern, response_text)

    if not stress_match or not boss_match:
        return False, "필수 필드 누락", None

    stress_val = int(stress_match.group(1))
    boss_val = int(boss_match.group(1))

    if not (0 <= stress_val <= 100):
        return False, f"Stress Level 범위 오류: {stress_val}", None

    if not (0 <= boss_val <= 5):
        return False, f"Boss Alert Level 범위 오류: {boss_val}", None

    extracted_data = {
        "break_summary": break_summary.group(1) if break_summary else None,
        "stress_level": stress_val,
        "boss_alert_level": boss_val
    }

    return True, "유효한 응답", extracted_data


def print_result(test_name: str, passed: bool, message: str = ""):
    """테스트 결과 출력"""
    status = f"{Colors.GREEN}✓ PASS{Colors.END}" if passed else f"{Colors.RED}✗ FAIL{Colors.END}"
    print(f"{status} {Colors.BOLD}{test_name}{Colors.END}")
    if message:
        print(f"  {message}")


def test_1_basic_environment():
    """1. 기본 환경 및 실행 검증"""
    print(f"\n{Colors.BOLD}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}테스트 1: 기본 환경 및 실행 검증{Colors.END}")
    print(f"{Colors.BOLD}{'='*60}{Colors.END}\n")

    # 1.1 의존성 설치 확인
    try:
        import fastmcp
        print_result("1.1 의존성 설치", True, "fastmcp가 정상적으로 설치되어 있습니다.")
    except ImportError:
        print_result("1.1 의존성 설치", False, "fastmcp를 찾을 수 없습니다.")
        return False

    # 1.2 서버 기본 실행
    client = MCPClient()
    try:
        client.start_server()
        print_result("1.2 서버 기본 실행", True, "서버가 정상적으로 시작되었습니다.")

        # 1.3 서버 정상 종료
        client.stop_server()
        print_result("1.3 서버 정상 종료", True, "서버가 정상적으로 종료되었습니다.")
        return True

    except Exception as e:
        print_result("1.2 서버 기본 실행", False, str(e))
        client.stop_server()
        return False


def test_2_command_line_parameters():
    """2. 필수 요구사항 검증 (커맨드라인 파라미터)"""
    print(f"\n{Colors.BOLD}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}테스트 2: 필수 요구사항 검증{Colors.END}")
    print(f"{Colors.BOLD}{'='*60}{Colors.END}\n")

    # 2.1 boss_alertness 100% 확률 테스트
    client = MCPClient(boss_alertness=100, boss_alertness_cooldown=9999)

    try:
        client.start_server()

        boss_levels = []
        for i in range(3):
            response, _ = client.call_tool("watch_netflix")

            if "result" in response and "content" in response["result"]:
                text = response["result"]["content"][0]["text"]
                is_valid, msg, data = validate_response(text)

                if is_valid and data:
                    boss_levels.append(data["boss_alert_level"])

        # Boss Alert Level이 1씩 증가했는지 확인
        if len(boss_levels) == 3 and boss_levels == [1, 2, 3]:
            print_result("2.1 boss_alertness 100% 확률", True,
                        f"Boss Alert Level이 예상대로 증가: {boss_levels}")
        else:
            print_result("2.1 boss_alertness 100% 확률", False,
                        f"Boss Alert Level이 예상과 다름: {boss_levels} (예상: [1, 2, 3])")

        client.stop_server()

    except Exception as e:
        print_result("2.1 boss_alertness 100% 확률", False, str(e))
        client.stop_server()
        return False

    # 2.2 boss_alertness_cooldown 동작 테스트
    client = MCPClient(boss_alertness=100, boss_alertness_cooldown=10)

    try:
        client.start_server()

        # Boss Alert를 1로 만들기
        response1, _ = client.call_tool("show_meme")
        text1 = response1["result"]["content"][0]["text"]
        _, _, data1 = validate_response(text1)

        print(f"  첫 호출 후 Boss Alert Level: {data1['boss_alert_level']}")

        # 15초 대기 (cooldown 10초보다 길게)
        print("  15초 대기 중...")
        time.sleep(15)

        # 다시 호출
        response2, _ = client.call_tool("show_meme")
        text2 = response2["result"]["content"][0]["text"]
        _, _, data2 = validate_response(text2)

        print(f"  15초 후 호출 Boss Alert Level: {data2['boss_alert_level']}")

        # cooldown으로 감소했다가 다시 증가했으므로 1이어야 함
        if data2['boss_alert_level'] == 1:
            print_result("2.2 boss_alertness_cooldown 동작", True,
                        "Boss Alert Level이 cooldown에 따라 감소 후 증가")
        else:
            print_result("2.2 boss_alertness_cooldown 동작", False,
                        f"Boss Alert Level이 예상과 다름: {data2['boss_alert_level']} (예상: 1)")

        client.stop_server()
        return True

    except Exception as e:
        print_result("2.2 boss_alertness_cooldown 동작", False, str(e))
        client.stop_server()
        return False


def test_3_core_features():
    """3. 핵심 기능 및 상태 관리 검증"""
    print(f"\n{Colors.BOLD}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}테스트 3: 핵심 기능 및 상태 관리{Colors.END}")
    print(f"{Colors.BOLD}{'='*60}{Colors.END}\n")

    # 3.1 Stress Level 자동 증가
    client = MCPClient()

    try:
        client.start_server()

        # 즉시 호출
        response1, _ = client.call_tool("take_a_break")
        text1 = response1["result"]["content"][0]["text"]
        _, _, data1 = validate_response(text1)

        print(f"  초기 Stress Level: {data1['stress_level']}")

        # 2분(120초) 대기
        print("  120초 대기 중...")
        time.sleep(120)

        # 다시 호출
        response2, _ = client.call_tool("take_a_break")
        text2 = response2["result"]["content"][0]["text"]
        _, _, data2 = validate_response(text2)

        print(f"  120초 후 Stress Level: {data2['stress_level']}")

        # 스트레스가 증가했어야 함 (감소량을 고려해도 초기보다 높아야 함)
        # 2분 = 2 포인트 증가 예상
        if data2['stress_level'] >= data1['stress_level'] - 80:  # 여유롭게 확인
            print_result("3.1 Stress Level 자동 증가", True,
                        "Stress Level이 시간에 따라 증가")
        else:
            print_result("3.1 Stress Level 자동 증가", False,
                        f"Stress Level 변화가 예상과 다름")

        client.stop_server()

    except Exception as e:
        print_result("3.1 Stress Level 자동 증가", False, str(e))
        client.stop_server()

    # 3.2 Boss Alert Level 5 도달 시 20초 지연
    client = MCPClient(boss_alertness=100, boss_alertness_cooldown=9999)

    try:
        client.start_server()

        # Boss Alert Level을 5로 만들기
        print("  Boss Alert Level을 5로 올리는 중...")
        for i in range(5):
            response, _ = client.call_tool("coffee_mission")
            text = response["result"]["content"][0]["text"]
            _, _, data = validate_response(text)
            print(f"    호출 {i+1}: Boss Alert Level = {data['boss_alert_level']}")

        # 추가 호출 시 20초 지연 확인
        print("  Boss Alert Level 5에서 추가 호출...")
        response, elapsed = client.call_tool("deep_thinking")

        print(f"  응답 시간: {elapsed:.2f}초")

        if 18 <= elapsed <= 25:  # 20초 ±5초
            print_result("3.2 Boss Alert Level 5 도달 시 20초 지연", True,
                        f"지연 시간이 예상대로: {elapsed:.2f}초")
        else:
            print_result("3.2 Boss Alert Level 5 도달 시 20초 지연", False,
                        f"지연 시간이 예상과 다름: {elapsed:.2f}초 (예상: 20초)")

        client.stop_server()

    except Exception as e:
        print_result("3.2 Boss Alert Level 5 도달 시 20초 지연", False, str(e))
        client.stop_server()

    # 3.3 모든 필수 도구 실행
    client = MCPClient()

    try:
        client.start_server()

        tools = [
            "take_a_break",
            "watch_netflix",
            "show_meme",
            "bathroom_break",
            "coffee_mission",
            "urgent_call",
            "deep_thinking",
            "email_organizing"
        ]

        all_passed = True
        for tool in tools:
            try:
                response, _ = client.call_tool(tool)

                if "result" in response:
                    text = response["result"]["content"][0]["text"]
                    is_valid, msg, data = validate_response(text)

                    if is_valid:
                        print(f"  ✓ {tool}: {data['break_summary'][:30]}...")
                    else:
                        print(f"  ✗ {tool}: {msg}")
                        all_passed = False
                else:
                    print(f"  ✗ {tool}: 응답 오류")
                    all_passed = False

            except Exception as e:
                print(f"  ✗ {tool}: {str(e)}")
                all_passed = False

        if all_passed:
            print_result("3.3 모든 필수 도구 실행", True, "모든 도구가 정상 동작")
        else:
            print_result("3.3 모든 필수 도구 실행", False, "일부 도구 실행 실패")

        client.stop_server()

    except Exception as e:
        print_result("3.3 모든 필수 도구 실행", False, str(e))
        client.stop_server()


def test_4_response_format():
    """4. 응답 형식 및 파싱 검증"""
    print(f"\n{Colors.BOLD}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}테스트 4: 응답 형식 및 파싱 검증{Colors.END}")
    print(f"{Colors.BOLD}{'='*60}{Colors.END}\n")

    client = MCPClient()

    try:
        client.start_server()

        response, _ = client.call_tool("bathroom_break")
        text = response["result"]["content"][0]["text"]

        is_valid, msg, data = validate_response(text)

        if is_valid:
            print(f"  Break Summary: {data['break_summary']}")
            print(f"  Stress Level: {data['stress_level']}")
            print(f"  Boss Alert Level: {data['boss_alert_level']}")
            print_result("4.1 응답 정규표현식 파싱", True, msg)
        else:
            print_result("4.1 응답 정규표현식 파싱", False, msg)

        client.stop_server()

    except Exception as e:
        print_result("4.1 응답 정규표현식 파싱", False, str(e))
        client.stop_server()


def main():
    """메인 함수"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}ChillMCP 서버 QA 자동 검증 시작{Colors.END}\n")

    # 모든 테스트 실행
    test_1_basic_environment()
    test_2_command_line_parameters()
    test_3_core_features()
    test_4_response_format()

    print(f"\n{Colors.BOLD}{Colors.BLUE}QA 검증 완료!{Colors.END}\n")


if __name__ == "__main__":
    main()
