# BizHarness

비즈니스 유스케이스 기반 에이전트 팀 생성기 — 계층화된 QA 검증 내장.

## 개요

BizHarness는 비즈니스 도메인 → 유스케이스 선택 → 에이전트 팀 생성 → QA 검증의
전 과정을 가이드하며, 기계 검증과 모델 판단을 명확히 분리하여 점수의 신뢰도를
투명하게 보여줍니다.

```
도메인 → 유스케이스 → 에이전트 팀 → 계층 QA → 개선 루프 → 검증된 산출물
```

## 핵심 차별점

| 항목 | 기존 Harness | BizHarness |
|------|-------------|------------|
| 시작점 | 기술 패턴 | 비즈니스 유스케이스 |
| QA 방법 | 수동/시뮬레이션 | **Tier A (기계검증) + Tier B (LLM판단) + 적대적 리뷰** |
| 점수 투명성 | 단일 점수 | **Tier A/B 분리 보고 — 검증된 부분이 어딘지 명확** |
| 적대적 테스트 | 없음 | **독립 공격자 에이전트 (6가지 공격 패턴)** |
| 비용 제어 | 전부 또는 없음 | **Quick / Standard / Full 모드 선택** |
| 에이전트 명세 | 비공식 | **필수 포맷 (모델, I/O 계약, 데이터 전달)** |
| 유스케이스 | 없음 | 5도메인 × 4개 + Golden Output |

## 설치

```bash
# 1) 마켓플레이스 등록
claude plugin marketplace add GyumanCho/biz-harness

# 2) 플러그인 설치
claude plugin install biz-harness@biz-harness
```

로컬 개발용:
```bash
claude --plugin-dir /path/to/biz-harness
```

## 사용법

```
> 이 프로젝트에 맞는 harness 만들어줘
> 이커머스 에이전트 팀 구성해줘
> /biz-harness
```

## 6-Phase 워크플로우

1. **Domain Discovery** — 도메인 파악, 기존 에이전트 감지
2. **Use Case Mapping** — 20개 표준 유스케이스에서 선택 또는 커스텀
3. **Agent Team Design** — 에이전트(명세), 스킬(가이드), 오케스트레이터 생성
4. **QA Scenario Generation** — E2E 시나리오 도출
5. **Empirical Validation** — QA 모드 선택, 계층 assertion + 적대적 리뷰
6. **Improvement Loop** — 실패한 assertion 수정 → 재테스트 (최대 3회)

## QA 모드

| 모드 | 실행 내용 | 비용 (3-에이전트 팀) |
|------|----------|---------------------|
| Quick | 실행 + Tier A assertion만 | ~6회 호출 |
| Standard | + Tier B + golden output 비교 | ~7회 호출 |
| Full | + 적대적 리뷰 + with/without 비교 | ~11회 호출 |

## Assertion 계층

| 계층 | 검증 내용 | 검증 방법 |
|------|----------|----------|
| **Tier A** | YAML 유효성, 필드 존재, 타입, 범위, 계약 | 결정적 — LLM 판단 불필요 |
| **Tier B** | 의사결정 정확도, 비즈니스 품질, 도메인 적합도 | LLM 판단 — 별도 보고 |

## 요구사항

- Claude Code
- `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` (Supervisor/Producer-Reviewer만)

## 라이선스

Apache-2.0
