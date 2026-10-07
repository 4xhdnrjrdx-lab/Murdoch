from pathlib import Path
import json
import re

folder = Path(__file__).resolve().parent
data = json.loads((folder / 'content.json').read_text())
template = (folder / 'studio.template.html').read_text()
(folder / 'record.html').write_text(template.replace('__CONTENT_JSON__', json.dumps(data, ensure_ascii=False).replace('</', '<\\/')))
spoken = '\n\n'.join(s['script'] for s in data['sections'] if s['script'])
(folder / 'READ_ALOUD_EN.txt').write_text(spoken + '\n')
count = len(re.findall(r"\b[\w'-]+\b", spoken))
guide = f'''# Как записать BUS225 A1

Готов сценарий на английском: {count} слов. При темпе 95-105 слов в минуту текст занимает примерно {count/105:.1f}-{count/95:.1f} минуты без длинных пауз. С источниками и переключениями ориентируйся примерно на 4,5 минуты. Английский упрощён; каждое предложение начинается с новой строки. Проверь время на репетиции. Лимит задания: не больше 5 минут.

## Что открыть

Открой START_RECORDING.command двойным щелчком в Finder. Он открывает record.html прямо в Google Chrome. Локальный сервер и интернет для записи не нужны. Этот запуск работает и после перезагрузки компьютера.

Можно также открыть файл record.html через «Открыть с помощью → Google Chrome». Основной адрес теперь начинается с file://. Старую ссылку http://127.0.0.1:8779/record.html не используй как постоянную закладку: она требует отдельного запуска сервера.

Камера и английский текст находятся по центру страницы: текст сразу под камерой. Разверни страницу на весь экран, чтобы текст оказался под объективом. Автопрокрутка включена, её скорость и размер шрифта можно изменить под текстом. Русские пояснения и просмотр готового видео раскрываются отдельно. Она записывает слайды, твою камеру и микрофон в один файл. Подсказки в запись не попадают. Страница не отправляет запись в интернет.

## Что делать тебе

1. Прочитай все русские пояснения и один раз произнеси английский текст вслух. Проверь, что понимаешь смысл и укладываешься во время.
2. Нажми «Камера и микрофон». Разреши доступ. Проверь свет и уровень микрофона.
3. Сделай короткую пробную запись, скачай и послушай её. После этого запиши полный вариант. Каждая новая запись начинается с первого блока.
4. После каждого блока нажимай «Следующий блок». Говори своими обычными интонациями, иногда смотри прямо в камеру. Не зачитывай русские пояснения.
5. После последней английской фразы покажи References примерно пять секунд и нажми «Закончить». Автоматическая остановка на 4:55 защищает лимит, но может обрезать незавершённый текст. Если не успел, запиши заново.
6. Скачай запись, проверь звук, видимость лица, начало и конец. Видео может иметь формат WebM или MP4 в зависимости от браузера. YouTube принимает оба формата.
7. Загрузи видео на YouTube с доступом Unlisted / «Доступ по ссылке». Вставь название и описание из VIDEO_DESCRIPTION.txt. Ссылку проверь в приватном окне: преподавательнице должен быть доступен просмотр.
8. В Moodle открой Video Presentation Submission, добавь ссылку в Online text и сохрани сдачу. Прочитай заявление, которое Moodle попросит подтвердить. Проверь, что ссылка действительно сохранена в твоей сдаче.

Справка YouTube по форматам: https://support.google.com/youtube/troubleshooter/2888402?hl=ru

Ссылка задания: https://moodleprod.murdoch.edu.au/mod/assign/view.php?id=3076825

Если запись в браузере не подходит, файл READ_ALOUD_EN.txt содержит тот же текст без инструкций. Можно записать себя на телефон, затем добавить готовые экраны из папки visuals рядом со своим видео в редакторе. Твоё лицо должно быть видно во время выступления. Слайды предназначены для визуальной поддержки, они не заменяют твоё выступление.

## Дедлайн

Проверено через Moodle API 25 сентября 2026, assignment 125039 / cmid 3076825:

- 2 октября 2026, 17:00 по Дубаю.
- 2 октября 2026, 21:00 по Перту.
- Исходный duedate: 1790946000.

В Moodle имеется более поздний технический cutoff. Это не продление дедлайна, ориентируемся на duedate. Внешнюю публикацию и сдачу ассистент не выполнял.

## Смысл выступления

Это индивидуальное задание A1. Тема Carrefour связана с нашим групповым проектом, но A1 является отдельным анализом одной научной статьи. Marriott использовался только в упражнении на паре.

Главная мысль: хороший AI-помощник должен давать точные советы и оставлять выбор за покупателем. Приятное общение само по себе не исправляет неподходящую рекомендацию.

'''
for i,s in enumerate(data['sections'],1):
    guide += f"### Блок {i}: {s['title']}\n\n{s['ru']}\n\n"
guide += '''## Если преподавательница задаст вопрос

**What is a taxonomy?**
A taxonomy is a structured way to classify different shopping AI systems.

**What are the two main groups?**
AI capabilities describe what the system can do. Parasocial skills describe features that create a sense of social connection.

**What did the 312 consumers do?**
They used and evaluated the taxonomy. They did not test our proposed Carrefour assistant.

**What is the main limitation?**
The study mainly focuses on the USA, so I would test the ideas with local customers.

**What is your proposal?**
A Carrefour UAE grocery assistant that respects the customer's budget, checks product availability and asks before making substitutions.

**Is this already available in the UAE?**
The assistant is my proposal. The actual company examples are the 2021 City+ launch in Dubai and the 2023 Hopla announcement in France.

**How would you measure success?**
I would compare it with ordinary product search and check budget compliance, basket completion and recommendation errors.

**What is value pre-creation in the article?**
It means AI can prepare useful choices or anticipate needs before the customer actively asks. It is another contribution discussed in the paper, although my short video focuses on the taxonomy and its practical use.

'''
(folder / 'START_HERE_RU.md').write_text(guide)
description=f"{data['title']} | BUS225 A1\n\nAn individual BUS225 presentation by Faiaz Dzhafarov.\n\nA critical discussion of Kennedy, He and Sarantopoulos (2026), applied to Carrefour through a proposed UAE grocery assistant. The shopping scenario and pilot are proposals, not reported test results. The company examples refer to dated launch announcements.\n\nReferences\n\n"
description += '\n\n'.join(r['full']+'\n'+r['url'] for r in data['references'])
(folder / 'VIDEO_DESCRIPTION.txt').write_text(description+'\n')
audit='''# Проверка содержания A1

Проверено 25 сентября 2026. Основной источник: выданный преподавателем Kennedy et al. (2026), Journal of Service Research, 29(3), 408-427. Содержательная часть PDF прочитана; страницы 414, 419 и 423 также проверены визуально.

| Критерий рубрики | Где раскрыт |
|---|---|
| Understanding and critique, 10 marks | Блоки 2 и 3: метод design science, 14 характеристик, две группы, CEM, компромиссы, сильная сторона и ограничения |
| Application, 5 marks | Блоки 4 и 5: реальные исторические инициативы и отдельное предложение для Carrefour UAE |
| Creativity in visuals, 5 marks | Контраст бюджета и корзины, схема характеристик, сопоставление методов и ограничений, этапы покупки |
| Professionalism and technical quality, 5 marks | Лицо на всём видео, микрофон, таймер и пробная запись; результат зависит от фактической записи пользователя |
| Audience engagement, 5 marks | Вопрос про бюджет в начале, понятный пример покупки и прикладные рекомендации |

## Проверенные утверждения

- 14 характеристик, 6 capabilities и 8 parasocial skills: статья, Table 6, p. 418. На экране Anthropomorphism объясняется как Human-like qualities; остальные названия сокращены без изменения смысла.
- Design science, исследования, интервью, патенты, реальные приложения: pp. 412-415.
- 312 участников оценивали классификацию: pp. 419-420. Это не измерение эффективности предлагаемой функции Carrefour.
- CEM и взаимосвязи характеристик: pp. 410-412, 420-421.
- Американский фокус: Limitations, p. 423. Тезис об отсутствии доказанного роста продаж является нашей оценкой дизайна исследования; не утверждается, что в статье вообще отсутствует эмпирическая проверка.
- Гипотетический ужин до AED 50, корзина AED 80 и предложенный пилот не являются реальными ценами, наблюдениями или результатами эксперимента.
- В тексте нет утверждения, что пользователь лично тестировал AI или посещал конкретный магазин.
- City+ и Hopla описаны как объявления о запусках в 2021 и 2023 годах. Нынешняя доступность функций в конкретном магазине не заявляется.
- Press releases подтверждают описание инициатив, но не независимую оценку удовлетворённости покупателей. Это ограничение прямо проговаривается.

## Первичные источники компании

'''+ '\n\n'.join(r['full']+'\n'+r['url'] for r in data['references'][1:])+'''

## Проверка языка

Первоначальный вариант: текст разбит по критериям оценки, содержит терминологию статьи и повторы для обучения.
Редакторская проверка: убраны рекламные оценки технологий и общие обещания роста продаж; короткий бытовой пример заменяет неподтверждённую статистику. Текст различает исследование, корпоративные объявления и собственное предложение. Оставлены необходимые учебные термины с русским объяснением.
Окончательный вариант: READ_ALOUD_EN.txt. В нём нет длинных тире, заглушек или выдуманного личного опыта.
'''
(folder / 'SOURCE_CHECK.md').write_text(audit)
print(f'Built record.html, script ({count} words), Russian guide, description and source check.')
