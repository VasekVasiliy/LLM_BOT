Репозиторий содержит скрипт для запуска телеграм бота

**t.me/LAB4_LLM_bot**

## Функциональность бота
* команды: 
   - /start (выводится приветствие и список доступных команд)
   - /model (выводит название используемой LLM)
   - /clear (очистить контекст переписки)
   - /context (посмотреть контекст переписки)
* запросы пользователя пересылаются LLM, запущеной на этом компьютере, и потом пересылаются пользователю

## Особенности бота
Контекст переписки сохраняется и может быть очищен, LLM отвечает в зависимости от контекста.