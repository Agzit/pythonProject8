Команды:
1)Создание задачи (POST-запрос):
Invoke-WebRequest -Uri http://localhost:8081/tasks -Method Post -Headers @{ "Content-Type" = "application/json" } -Body '{"title": "Go to gym", "priority": "normal"}'

2)Получение всех задач (GET-запрос):
Invoke-WebRequest -Uri http://localhost:8081/tasks -Method Get

3)Отметить задачу как выполненную (POST-запрос):
Invoke-WebRequest -Uri http://localhost:8081/tasks/1/complete -Method Post

Важно:
команды писать в терминал PyCharm

Порядок действий:
1.запустить через терминал | python main.py
2.Создание задачи|команда 1)
3.Отметить как True|команда 3)
4.посмотреть все задачи|команда 2)
5.посмотреть с браузера| http://localhost:8081/tasks




priority ['low', 'normal', 'high']:
