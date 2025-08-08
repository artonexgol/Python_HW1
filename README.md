# Автотест для мобильного приложения (Appium + pytest)

Минимальный каркас E2E-тестов на Appium (Python/pytest), который работает для Android и iOS. По умолчанию тесты аккуратно пропускаются, если не настроен Appium URL и капабилити.

## Быстрый старт

1) Установите зависимости Python:

```bash
pip install -r requirements.txt
```

2) Скопируйте `.env.example` в `.env` и заполните нужные поля:

```bash
cp .env.example .env
```

Ключевые переменные:
- `APPIUM_URL` — адрес сервера Appium (локально: `http://localhost:4723/wd/hub` или URL облака).
- `PLATFORM` — `Android` или `iOS`.
- Для Android укажите либо путь к APK в `APP`, либо `APP_PACKAGE` + `APP_ACTIVITY` для already-installed.
- Для iOS укажите `APP` (ipa) или `BUNDLE_ID` установленного приложения.
- Для проверки UI можно задать `CHECK_AID` (accessibility id) или `CHECK_ID` (resource-id/name).

3) (Локально) Поднимите Appium 2 и драйвер:

```bash
npm i -g appium @appium/uiautomator2-driver @appium/xcuitest-driver
appium driver install uiautomator2
appium driver install xcuitest
appium | cat
```

4) Запустите тесты:

```bash
pytest -q
```

Тесты будут пропущены, если `APPIUM_URL` не задан. При корректных капабилити тест `tests/test_smoke.py::test_app_launches_and_shows_first_screen` проверит запуск приложения и, опционально, наличие элемента.

## Примеры настроек

### Android с установленным приложением
```bash
export APPIUM_URL=http://localhost:4723/wd/hub
export PLATFORM=Android
export DEVICE_NAME="Android Emulator"
export APP_PACKAGE=com.example
export APP_ACTIVITY=.MainActivity
export CHECK_AID="login_button"
pytest -q
```

### iOS (симулятор) с bundleId
```bash
export APPIUM_URL=http://localhost:4723/wd/hub
export PLATFORM=iOS
export DEVICE_NAME="iPhone 15"
export PLATFORM_VERSION=17.2
export BUNDLE_ID=com.example.app
export CHECK_ID="Home"
pytest -q
```

## Структура
- `tests/conftest.py` — фикстура `driver`, инициализация Appium на основе env.
- `tests/test_smoke.py` — минимальный smoke.
- `requirements.txt` — зависимости.
- `.env.example` — образец настроек.

## Расширение
- Добавьте Page Object'ы и больше тестов.
- Включите Allure-репорты: `pytest --alluredir=allure-results`.
- Для CI используйте облака (BrowserStack, Sauce Labs) — задайте их `APPIUM_URL` и капабилити.