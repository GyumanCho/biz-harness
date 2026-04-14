# BizHarness

> 비즈니스 유스케이스 기반 Claude Code 에이전트 팀 생성기 — 계층화된 QA 검증 내장

[![Claude Code Plugin](https://img.shields.io/badge/Claude%20Code-Plugin-blueviolet)](https://github.com/GyumanCho/biz-harness)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](./LICENSE)
[![Version](https://img.shields.io/badge/version-1.5.0-green)]()

[English](./README.md) | **한국어**

---

## 한 줄 요약

**"우리 회사 업무에 맞는 Claude Code 에이전트 팀을 만들고, 진짜로 작동하는지 검증까지"** — 도메인 선택부터 실증 검증까지 30분 내에 끝납니다.

```
도메인 → 유스케이스 → 에이전트 팀 → 계층 QA → 개선 루프 → 검증된 산출물
```

---

## 🎯 핵심 특징

### 1. **비즈니스 유스케이스에서 출발**
기술 패턴이 아닌 **실제 업무**에서 시작. 20개 표준 유스케이스 라이브러리(5도메인 × 4개) 또는 커스텀 정의 지원.
- **도메인**: SaaS / 이커머스 / 금융 / 미디어 / 개발
- 예시: *티켓 분류*, *상품 리스팅 생성*, *리스크 스코어링*, *콘텐츠 모더레이션*, *코드 리뷰*

### 2. **3계층 QA 검증** (자체 평가 루프 차단)
| 계층 | 검증 내용 | 방법 | 신뢰도 |
|------|----------|------|--------|
| **Tier A** | YAML 유효성, 필드 존재, 타입, 범위, 계약 | 결정적 Python 스크립트 | 100% 재현 |
| **Tier B** | 의사결정 정확도, 비즈니스 품질 | LLM 판단 (별도 보고) | 투명하게 분리 |
| **Adversarial** | 6가지 공격 패턴으로 취약점 노출 | 독립 에이전트 (생성 컨텍스트 비접근) | 자체 편향 차단 |

**차별점**: 단일 점수가 아닌 **Tier별 분리 보고** — 기계 검증 부분과 모델 판단 부분이 명확히 구분됩니다.

### 3. **비용 통제 가능한 QA 모드**
| 모드 | 실행 내용 | 예상 호출 수 (3-에이전트 팀) |
|------|----------|------------------------------|
| **Quick** | 실행 + Tier A만 | ~6회 |
| **Standard** | + Tier B + Golden Output 비교 | ~7회 |
| **Full** | + 적대적 리뷰 + With/Without 베이스라인 | ~11회 |

예산·단계에 맞춰 선택 (개발 중 Quick, 릴리즈 전 Full).

### 4. **필수 에이전트 명세 포맷**
자유 형식 프롬프트가 아닌 **구조화된 명세** 강제:
- 모델 선택 근거 (Haiku / Sonnet / Opus)
- I/O 계약 (input YAML 스키마 → output YAML 스키마)
- 데이터 전달 프로토콜 (에이전트 간)
- 실행 모드 (서브에이전트 vs Agent Teams)

### 5. **Golden Output 내장**
7개의 사전 검증된 기대 출력 (5 happy path + 1 edge case + 1 failure case) — 비교 기준점이 없는 LLM 평가의 고질병 해결.

### 6. **재사용 가능한 산출물**
- **에이전트 파일** (`.claude/agents/*.md`) — Claude Code가 바로 사용
- **스킬 가이드** (`.claude/skills/*/SKILL.md`) — 도메인 지식 문서화
- **오케스트레이터** — 6개 아키텍처 패턴 템플릿 (Pipeline, Supervisor, Expert Pool, Producer-Reviewer, Hierarchical, Peer)
- **QA 시나리오** — Happy/Edge/Failure YAML
- **Score Card** — 재현 가능한 검증 리포트

---

## 🚀 설치

### 마켓플레이스에서 설치 (권장)
```bash
# 1) 마켓플레이스 등록 (최초 1회)
claude plugin marketplace add GyumanCho/biz-harness

# 2) 플러그인 설치
claude plugin install biz-harness@biz-harness
```

### 로컬 개발용
```bash
claude --plugin-dir /path/to/biz-harness
```

### 업데이트
```bash
claude plugin marketplace update biz-harness
claude plugin update biz-harness@biz-harness
```

---

## 💡 사용법

### 가장 빠른 시작
프로젝트 디렉토리에서 Claude Code를 연 뒤:
```
> /biz-harness
```
또는 자연어로:
```
> 이 프로젝트에 맞는 에이전트 팀 만들어줘
> 이커머스 상품 리스팅 자동화 팀 구성해줘
> 고객 지원 티켓 분류 harness 만들어줘
```

### 예시 세션 흐름
```
You   > /biz-harness
Claude> [Phase 1] 프로젝트 분석 중...
        도메인: E-commerce (package.json에서 shopify API 발견)
        기존 에이전트: 없음
        사용자 레벨: Intermediate

You   > 진행해줘
Claude> [Phase 2] 추천 유스케이스:
        1. UC-ECOM-01 — 상품 리스팅 파이프라인 ⭐ (추천)
        2. UC-ECOM-02 — 재고 동기화
        3. UC-ECOM-03 — 주문 상태 알림
        4. 커스텀 정의
        선택하세요:

You   > 1번
Claude> [Phase 3] 에이전트 팀 설계 중...
        - listing-writer (Sonnet, SEO 카피 생성)
        - image-tagger (Haiku, 속성 추출)
        - qa-reviewer (Sonnet, 브랜드 톤 검증)
        아키텍처: Pipeline
        orchestrator.md 생성 완료.

You   > QA 모드는 Standard로
Claude> [Phase 5] 실증 검증 (Standard 모드)...
        ✅ Tier A: 12/12 passed
        ⚠️  Tier B: 8/10 (브랜드 톤 어긋남 2건)
        Golden Output 비교: 일치도 87%
        → [Phase 6] 개선 루프 진행할까요?
```

### 단독 실행 가능한 도구
플러그인 없이도 `tools/` 디렉토리 Python 스크립트 사용 가능:
```bash
# Tier A assertion 검증
python tools/verify_tier_a.py output.yaml assertions.yaml

# Golden output → assertion 변환
python tools/convert_golden.py golden.yaml -o assertions.yaml
```

---

## 📋 6-Phase 워크플로우

| Phase | 이름 | 핵심 활동 | 산출물 |
|-------|------|----------|--------|
| 1 | Domain Discovery | 프로젝트 분석, 기존 에이전트 감지, 충돌 체크 | 도메인 리포트 |
| 2 | Use Case Mapping | 20개 표준 유스케이스 제시 또는 커스텀 정의 | 선택된 UC-ID |
| 3 | Agent Team Design | 에이전트(명세), 스킬, 오케스트레이터 생성 | `.claude/agents/*`, `.claude/skills/*`, orchestrator |
| 4 | QA Scenario Generation | Happy/Edge/Failure 시나리오 도출 | YAML 시나리오 파일 |
| 5 | Empirical Validation | QA 모드 선택, Tier A/B assertion + 적대적 리뷰 | Score Card |
| 6 | Improvement Loop | 실패 assertion 수정 → 재테스트 (최대 3회) | 개선된 팀 + 변경 로그 |

---

## 📚 참조 파일 (12개)

| 파일 | 용도 |
|------|------|
| `usecase-catalog.md` | 5도메인 × 4유스케이스 템플릿 |
| `agent-patterns.md` | 6개 아키텍처 패턴 + 결정 트리 |
| `agent-definition-spec.md` | 에이전트 파일 필수 포맷 |
| `skill-writing-guide.md` | Why-first 지시문, 안티패턴 |
| `qa-scoring-engine.md` | Tier A/B 프레임워크, 비용 가이드 |
| `qa-adversary-guide.md` | 6가지 적대적 공격 패턴 |
| `qa-scenario-templates.md` | Happy/Edge/Failure 템플릿 |
| `improvement-playbook.md` | 축별 개선 전략, 리포트 템플릿 |
| `orchestrator-templates.md` | 6개 패턴 오케스트레이터 |
| `team-examples.md` | 완성된 팀 2개 + 점수 분해 |
| `execution-trace-example.md` | 실제 실행 트레이스 예시 |
| `golden-outputs/` | 사전 검증된 기대 출력 7개 |

---

## 🛠 요구사항

- **Claude Code** (플러그인 지원 버전)
- **환경변수** (선택): `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` — Supervisor/Producer-Reviewer 패턴 사용 시만 필요
- **Python 3.8+** (도구 스크립트 사용 시): `pip install -r tools/requirements.txt`

---

## 🐛 트러블슈팅

**"Plugin not found"**
```bash
claude plugin marketplace update biz-harness
claude plugin marketplace list   # 등록 여부 확인
```

**"Tier A assertion 파싱 실패"**
→ YAML 문법 확인. `python tools/verify_tier_a.py <output> <assertions>` 로 구체적 에러 확인.

**"Adversarial 리뷰 비용이 예상보다 큼"**
→ `Quick` 모드로 전환. Full은 릴리즈 직전에만 사용 권장.

---

## 🗺 로드맵

- [ ] 커스텀 도메인 템플릿 빌더
- [ ] MCP 서버 통합 유스케이스
- [ ] 다국어 Golden Output
- [ ] 비용 대시보드 (토큰/호출수 추적)

---

## 🤝 기여

이슈 / PR 환영. 특히:
- 새로운 유스케이스 카탈로그 항목
- Golden Output 추가
- 적대적 공격 패턴 제보

---

## 📄 라이선스

Apache-2.0 — [LICENSE](./LICENSE) 참조
