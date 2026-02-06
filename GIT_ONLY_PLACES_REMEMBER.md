# Ветка только с Places Remember

Репозиторий изначально содержит несколько заданий (1_backend_MSstroy, 2_backend_avito, appBooster, Places Remember). Ветка создана от основной, поэтому в ней видны все эти папки.

**Чтобы на этой ветке в Git остался только проект Places Remember**, выполните в корне репозитория:

```bash
# Убрать из индекса (перестать отслеживать), не удаляя папки с диска
git rm -r --cached "1_backend_MSstroy" 2>/dev/null
git rm -r --cached "2_backend_avito"   2>/dev/null
git rm -r --cached "appBooster"       2>/dev/null
git rm -r --cached "ivelum"           2>/dev/null

# Закоммитить — на ветке в репозитории останутся только README и Places Remember
git add .
git commit -m "chore: leave only Places Remember on this branch"
git push
```

После этого на удалённой ветке будут только:
- `README.md`
- `Places Remember/`
- этот файл (при желании удалите: `git rm GIT_ONLY_PLACES_REMEMBER.md` и закоммитьте).

Папки `1_backend_MSstroy`, `appBooster` и т.д. **на диске** не удалятся — они просто перестанут входить в коммиты этой ветки.

Если нужна отдельная репозитория только под Places Remember, скопируйте папку в новый репозиторий и запушьте её одну.
