"""Create rubric map and concise Russian team review note from verified page map."""
from pathlib import Path
import json,html
ROOT=Path(__file__).resolve().parents[1]
pm=json.loads((ROOT/'qa/page_map.json').read_text())
counts=json.loads((ROOT/'qa/word_count.json').read_text())
def pg(*titles):return sorted(set(pm[t] for t in titles))
rows=[]
def add(code,weight,criterion,sections,pages,gap):rows.append(dict(code=code,weight_percent=weight,criterion=criterion,sections=sections,pages=pages,coverage='Раздел включён; содержание и страницы проверены',remaining_gap=gap))
add('1',5,'Executive summary','1',pg('1. Executive summary'),'Условную рекомендацию должна согласовать команда.')
add('2',5,'Industry business description','2',pg('2. Industry and business description'),'Размер целевого товарного рынка не установлен; доля рынка не выдумана.')
add('3.1',10,'Type of business','3.1',pg('3.1 Business and legal structure'),'В проекте моделируется marketplace; первичная торговля noon исключена явно.')
add('3.2',None,'Legal structure','3.1; 5.3',pg('3.1 Business and legal structure','5.3 Government constraints and incentives'),'Нужна актуальная классификация Jordan entity и допустимое владение; текущая консолидированная норма не получена.')
add('3.3',None,'History / mission / goals / objectives','3.2',pg('3.2 History, mission and ownership'),'Исторические факты отделены от целей проекта; внутреннего одобрения noon нет.')
add('3.4',None,'Principals / ownership','3.2',pg('3.2 History, mission and ownership'),'PIF 50% относится к 2016; текущая cap table неизвестна.')
add('4.1',15,'Product / service analysis','4.1; 6.4',pg('4.1 Offer and customer demand','6.4 Estimated sales and service operations'),'Проверить SKU, гарантии и соответствие требованиям до реального запуска.')
add('4.2',None,'Customer profile / demand','4.1; Exhibit 2',pg('4.1 Offer and customer demand','Exhibit 2a. Customer and order assumptions'),'Нет первичного исследования; 20/40/60 тысяч клиентов являются сценарием.')
add('4.3',None,'Competitive situation','4.2',pg('4.2 Competitive situation'),'Нет аудита реального исполнения доставки или сравнительной корзины; обещания продавцов названы обещаниями.')
add('5.1',15,'Host country business climate','5.1',pg('5.1 Business climate'),'Макроиндикаторы датированы 2025; они не прогнозируют спрос noon.')
add('5.2',None,'SWOT analysis','5.2; Exhibit 1',pg('5.2 SWOT and strategic implications','Exhibit 1. SWOT and response'),'Команде проверить связь каждого фактора с решением.')
add('5.3',None,'Government constraints / incentives','5.3',pg('5.3 Government constraints and incentives'),'Не подтверждены право на льготы и структура владения; в бюджете льгот нет.')
add('5.4',None,'Laws / regulations / administration','5.4',pg('5.4 Laws and administration'),'Нужны HS/origin, местный налоговый и юридический анализ. Конфликт personal-parcel источников раскрыт.')
add('6.1',20,'Positioning','6.1',pg('6.1 International strategy and positioning'),'Команда должна согласовать transnational approach, категорийный фокус и ценность предложения.')
add('6.2',None,'Pricing','6.2; Exhibit 3',pg('6.2 Pricing and promotion','Exhibit 3. Unit economics and fixed budgets'),'Комиссия, delivery fee и налоговая база являются допущениями; требуется договорная проверка.')
add('6.3',None,'Distribution / logistics','6.3',pg('6.3 Entry mode, distribution and logistics'),'Нет выбранного партнёра и коммерческих предложений. JV условный; экспорт дополнен вторым entry mode.')
add('6.4',None,'Promotion / advertising','6.2',pg('6.2 Pricing and promotion'),'План кампаний и бюджет предложены; результатов кампаний нет.')
add('6.5',None,'Estimated sales / sales mix','6.4; Exhibit 2',pg('6.4 Estimated sales and service operations','Exhibit 2a. Customer and order assumptions','Exhibit 2b. Planned sales mix, 2027'),'Сценарий net completed orders и средняя корзина требуют проверки. GMV не выручка.')
add('6.6',None,'Production / service strategies','6.4',pg('6.4 Estimated sales and service operations'),'Проект услуги, не производства. Проверить обещания доставки и reverse logistics.')
add('7.1',10,'Cost / funding / cash flow','7.1; Exhibits 3, 5',pg('7.1 Costs, funding and cash flow','Exhibit 3. Unit economics and fixed budgets','Exhibit 5a. Annual cash flow','Exhibit 5c. Monthly cash control'),'Бюджетные допущения, нет обязательств инвесторов. Без второй суммы January 2028 cash отрицателен.')
add('7.2',None,'Projected profit and loss','7.2; Exhibit 4',pg('7.2 Profitability and financial controls','Exhibit 4. Projected profit and loss'),'21% налоговый резерв условный; классификация agent/principal требует подтверждения.')
add('7.3',None,'Other financial statements / data','Exhibits 5b, 6; financial_model.json',pg('Exhibit 5b. Simplified net-asset reconciliation','Exhibit 6. Break-even and sensitivity'),'Есть net-asset reconciliation, 36 месяцев cash flow, break-even и 6 сценариев. Это не statutory accounts или valuation.')
add('8.1',5,'Personnel / sales force','8.1',pg('8.1 People and advisers'),'Роли и loaded staff budget предложены; сотрудники не наняты.')
add('8.2',None,'Business advisers','8.1',pg('8.1 People and advisers'),'Советники названы по функциям; договоров и консультаций не было.')
add('8.3',None,'Contingency plans','8.2; Exhibit 7',pg('8.2 Contingencies','Exhibit 7. Proposed operating controls'),'Триггеры, владельцы и stop rights предложены; требуется согласие управления.')
add('9',5,'Conclusions / recommendations','9',pg('9. Conclusions and recommendations'),'Рекомендован ограниченный пилот при выполнении условий, а не гарантированный вход.')
add('10.1',10,'Standard / table of contents','Cover; disclaimer; contents; all sections',[1,2,3],'Имена внесены по LMS; Faiaz ID подтверждён LMS, четыре других ID предоставлены пользователем. Именной загрузчик не установлен.')
add('10.2',None,'Expression / mechanics / proof reading','All; humanizer audit',list(range(4,pm['Bibliography'])),'Финальная человеческая редактура и подтверждение допустимости ИИ остаются за командой.')
add('10.3',None,'Illustrations / exhibits / appendices','Appendices A to C',list(range(pm['Appendix A. Market and demand exhibits'],pm['Exhibit 7. Proposed operating controls']+1)),'Таблицы поддерживают основной текст; без выдуманных meeting logs и подписей.')
add('10.4',None,'Referencing / research effort','Bibliography; source register',[pm['Bibliography'],pm['Bibliography']+1],'24 библиографические записи, 31 источник в общем аудите; отдельные правовые и исходные poster-ссылки имеют раскрытые ограничения.')
assert sum(r['weight_percent'] or 0 for r in rows)==100
(ROOT/'qa/rubric_map.json').write_text(json.dumps({'basis':'Major Project Report marking guide, reconfirmed against current Moodle file on 2026-10-20; not Project Proposal guide.','weight_note':'Weight shown once per parent criterion; no invented subcriterion allocation.','total_weight':100,'rows':rows},ensure_ascii=False,indent=2)+'\n')
notes=f'''ОТЧЁТ TAKING NOON TO JORDAN
20 октября 2026 | The Levant Five

Основной DOCX/PDF оформлен как завершённый Major Project Report. Пометки draft/team review удалены из обложки, колонтитулов, текста и свойств файла. Внутренние вопросы и план проверки команды вынесены из отчёта в эту отдельную записку. Обязательный disclaimer и точное раскрытие помощи Codex сохранены. Работа не сдана и никому не отправлена.

Объём: основной текст с заголовками {counts['main_including_headings']} слов; библиография с заголовком, пояснением и URL {counts['bibliography_including_heading_note_urls']}; обложка, disclaimer и оглавление {counts['front_matter_and_contents']}. Консервативный итог до приложений {counts['conservative_total_before_appendices']} из 4000. References включены. Метод: пробельные токены, видимый URL считается одним; Word может давать немного другой результат.

Имена и номера на титуле: Aram Avetisyan 35818705; Faiaz Dzhafarov 35553299; Abdoulaye Wahab Diabagate 34704818; Hatim Hatim 35839091; Dennis Afanasiev 35907935. Имена взяты из LMS, номер Faiaz также подтверждён LMS; остальные четыре номера прямо сообщил пользователь после сопоставления имён. LMS их скрывает, поэтому независимая проверка этих четырёх ID не заявляется. Hatim Hatim и Dennis Afanasiev — точное написание в LMS.

Содержание проверено по 30 строкам и подпунктам Major Project Report marking guide (общий вес 100%). Это подтверждение покрытия требований, не обещание оценки. Фотографии Project Proposal не использовались как рубрика финального отчёта. Пять участников ранее разрешены по подтверждению пользователя.

Что действительно требуется от участников перед сдачей:
1. Каждый должен заполнить подлинный confidential peer evaluation, включая себя. В сохранённой форме указано: отчёт не оценивают, пока не получены формы всех участников. Форма предписывает запечатанный конверт преподавателю для TNE; policy также говорит приложить к сдаваемому проекту. Если местный преподаватель дал другой способ, следовать подтверждённому указанию; оценками других участников не заполнять общий PDF. Подписи, оценки и вклады не придуманы.
2. Group Projects Policy требует подписанного charter для преподавателя и учёта индивидуальных вкладов; outline требует minutes реальных встреч. Их отсутствие нельзя исправить выдуманной записью.
3. Согласовать содержание с командой, проверить одобрение темы, допустимость уровня помощи AI и именного загрузчика. Эти подтверждения не найдены в текущих объявлениях LMS или проверенной почте. Краткое раскрытие фактической помощи оставлено в отчёте.
Номер и фамилия Faiaz используются в имени файла по правилу outline; это не назначает Faiaz загрузчиком. Все пять имён и номеров уже заполнены.

Финансовые допущения: 60/150/240 тысяч net completed orders в 2027/2028/2029; корзина 45 JOD; комиссия 15%; чистый delivery fee 3 JOD; logistics 7/4,8/4,5 JOD; equity 600+300 тысяч JOD. Проверены 22 тождества/расчёта, включая 36 месяцев cash flow. Прибыль третьего года 229100 JOD; совокупный free cash flow за три года отрицательный, −361400 JOD. Это сценарий учебного бизнес-плана, не внутренние данные noon и не коммерческое предложение. Получение реальных юридических заключений и логистических ставок является условием возможного бизнеса, а не выполненным исследованием команды.

Ссылки: повторно проверены адреса и соответствие утверждениям. Вместо общей главной LMS стоят два прямых resource URL. Заголовок Delivery options и APA suffixes исправлены; для ставки 16% дана прямая официальная арабская страница tax rates. Некоторые сайты ограничивают автоматические GET-запросы; это отмечено в qa/link_checks.json отдельно от проверки содержимого браузером. noon Payments — динамическая страница: страна Jordan подтверждается индексированным официальным FAQ, но полное тело не отрисовалось в браузере. Текущая консолидированная investment regulation не получена, поэтому право на конкретный процент владения не утверждается. Нет выдуманных источников, но абсолютная доступность внешних сайтов из любой сети не гарантируется.

Moodle: срок 6 ноября 2026, 19:55 Asia/Dubai; сдаёт лидер. 20 октября в 16:13 текущие rubric-файлы снова совпали с сохранёнными по SHA-256. Gmail по теме BUS219 после 19 октября не показал новых писем; Outlook и WhatsApp не охвачены.

Роли для проверки по исходному постеру: Aram — компания; Faiaz — Jordan/SWOT; Abdoul — стратегия/расчёты; Hatim — источники/редактура; Denis — координация. Это исходное распределение, не подтверждение выполненного вклада.
'''
(ROOT/'REVIEW_NOTES_RU.txt').write_text(notes)
# Single readable HTML companion: plain document, no external assets or scripts.
html_rows=''.join('<tr>'+''.join(f'<td>{html.escape(str(v))}</td>' for v in [r['code'],str(r['weight_percent'])+'%' if r['weight_percent'] is not None else '',r['criterion'],r['sections'],', '.join(map(str,r['pages'])),r['remaining_gap']])+'</tr>' for r in rows)
page='''<!doctype html><html lang="ru"><meta charset="utf-8"><title>BUS219: проверка командой</title><style>body{font:16px/1.55 system-ui,sans-serif;max-width:1200px;margin:40px auto;padding:0 24px;color:#17212b}h1{font-size:28px}pre{font:inherit;white-space:pre-wrap}table{border-collapse:collapse;width:100%;font-size:14px}th,td{border:1px solid #ccd4dc;padding:9px;text-align:left;vertical-align:top}th{background:#edf1f5}a{color:#174e85}@media print{body{margin:10mm}thead{display:table-header-group}tr{break-inside:avoid}}</style>'''+f'<h1>BUS219: проверка итогового отчёта</h1><p><a href="35553299DzhafarovF-2-Final.pdf">Открыть PDF отчёта</a> · <a href="35553299DzhafarovF-2-Final.docx">Редактируемый DOCX</a></p><pre>{html.escape(notes)}</pre><h2>Major Project Report marking guide: проверка всех подпунктов</h2><p>Вес указан один раз для каждого общего критерия; всего 100%. Страницы относятся к PDF от 20 октября.</p><table><thead><tr><th>Пункт</th><th>Вес</th><th>Критерий</th><th>Раздел / exhibit</th><th>Страницы</th><th>Осталось проверить</th></tr></thead><tbody>{html_rows}</tbody></table></html>'
(ROOT/'TEAM_REVIEW_RU.html').write_text(page)
print('Created review note and',len(rows),'rubric rows; weights total 100%')
