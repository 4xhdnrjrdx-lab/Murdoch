---
name: feedback-unik-worktree-isolation
description: "ЖЕЛЕЗНО: общее дерево ~/Documents/Jarvis-assistant = Coder'а; вся моя (Unik) работа — ТОЛЬКО в ~/Documents/Jarvis-wt-unik"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 23eb0fe3-4a0a-419c-947a-fe427c6c3d7e
---

# Изоляция работы Unik в выделенном worktree (правило Сэра 13.07.2026, ПОСТОЯННОЕ)
🔗 [[MEMORY]] · [[feedback_clear_safety]] · [[feedback_user_no_git]] · [[moodle_karen_feature]]


**Правило:** общий working-tree `~/Documents/Jarvis-assistant` принадлежит **Coder'у** — я (терминал
Unik / Murdoch_University) в нём **НЕ работаю вообще**. Вся моя работа — в постоянном выделенном git-worktree
**`~/Documents/Jarvis-wt-unik`**: ветки, правки, тесты, eval, PR — только там.

**Why:** дерево общее между сессиями (Coder, Fable-overnight). 13.07 я обнаружил дерево на ЧУЖОЙ ветке
`feat/voice-cache-w2` с незакоммиченной voice-WIP другой сессии — мои правки легли поверх, test_voice
валила чужая WIP (не я). Работа в общем дереве = риск затереть чужой WIP и запутать git-состояние.

**How to apply:**
1. **Никогда не редактировать/коммитить/переключать ветки в `~/Documents/Jarvis-assistant`.** Даже
   `git checkout`/`stash`/`pull` там — нет.
2. **Вся работа — в `~/Documents/Jarvis-wt-unik`** (создан `git worktree add`, база origin/main). Перед
   задачей: `cd ~/Documents/Jarvis-wt-unik && git fetch origin && git checkout -b feat/<x> origin/main`.
   Тесты/eval/commit/push/PR — оттуда.
3. **Чужой WIP не трогать НИКОГДА** (образец 13.07: выборочный stash своих файлов → worktree → PR →
   вернул всё как было, чужую voice-WIP не тронул).
4. **⚠️ ДЕПЛОЙ/рестарт karen идёт из ОБЩЕГО дерева** (karen там живёт). Если общий tree на чужой/
   разошедшейся ветке без моего кода — рестарт задеплоит НЕ то. Тогда НЕ рестартить самому, а
   флагнуть Сэру/Оркестратору: «origin/main готов (мой PR смержен), но общий tree надо привести к
   origin/main — это владелец дерева (Coder)». Пример: 13.07 #355 смержен в origin/main (fb89d50), но
   общий tree был на b25635d (Coder voice-cache, без #355) → рестарт отложил.
5. Перед ЛЮБЫМ git-действием сверять, где я: `pwd` (должно быть Jarvis-wt-unik) и `git branch --show-current`.

Связано: [[feedback_clear_safety]], [[feedback_user_no_git]] (у Сэра git — только через меня на m1; тут
про Jarvis-репо на Маке), [[moodle_karen_feature]].
