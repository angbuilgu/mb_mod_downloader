# Mount & Blade Mod Downloader

## 프로젝트 소개
이 프로젝트는 Mount & Blade 게임의 모드를 편리하게 다운로드하고 관리할 수 있도록 돕는 GUI 기반 애플리케이션입니다. PyQt6를 사용하여 직관적인 사용자 인터페이스를 제공하며, 모드 목록 관리 및 설정 기능을 포함합니다.

## 주요 기능
*   **GUI 기반 인터페이스**: PyQt6를 활용한 사용자 친화적인 그래픽 인터페이스.
*   **모드 다운로드**: Mount & Blade 모드를 쉽게 다운로드할 수 있습니다.
*   **모드 목록 관리**: 다운로드한 모드 목록을 효율적으로 관리합니다.
*   **설정 관리**: `config.json` 파일을 통해 애플리케이션 설정을 관리합니다.

## 설치 방법

### 1. Python 환경 설정
Python 3.x 버전이 설치되어 있어야 합니다. 가상 환경을 사용하는 것을 권장합니다.

```bash
python -m venv .venv
source .venv/Scripts/activate  # Windows: .venv\Scripts\activate
```

### 2. 의존성 설치
프로젝트에 필요한 라이브러리들을 설치합니다.

```bash
pip install -r requirements.txt
```

## 사용 방법

### 1. 애플리케이션 실행
의존성 설치가 완료되면 다음 명령어를 사용하여 애플리케이션을 실행할 수 있습니다.

```bash
python src/main.py
```

### 2. 설정 파일 (`config.json`)
애플리케이션은 `config.json` 파일을 사용하여 설정을 관리합니다. 이 파일은 애플리케이션이 실행되는 디렉토리에 위치해야 합니다. 필요한 경우 수동으로 생성하거나, 애플리케이션이 처음 실행될 때 기본 설정으로 생성될 수 있습니다.

## 개발 환경
*   Python 3.x
*   PyQt6
