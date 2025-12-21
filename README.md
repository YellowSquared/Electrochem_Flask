# Electrochem_Flask
Предсказание продуктов реакции электролиза

## Установка и запуск для разработки (VS Code)

1. Установите расширение **Container Tools** (ms-azuretools.vscode-containers) для VS Code.
2. Установите **Docker Desktop** (GUI) или **Docker Engine** (CLI), запустите Docker.
3. Клонируйте репозиторий:

    ```shell
    git clone git@github.com:YellowSquared/Electrochem_Flask.git
    ```

4. Откройте проект в VS Code:

    ```shell
    code Electrochem_Flask
    ```

5. В левом нижнем углу нажмите на иконку удаленного доступа (Remote Explorer) и выберите **Open Container** или **Reopen in Container**.

6. Дождитесь завершения установки контейнера.

7. Откройте терминал контейнера (Ctrl + Shift + `) и выполните команду:

    ```shell
    poetry run echem
    ```

