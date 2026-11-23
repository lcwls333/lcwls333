# 明理 ClearLogic · PWA v1.0

在 HTML 离线版基础上增加：**可安装到桌面/主屏、独立窗口、离线缓存**。
仍然是单页应用，无后端、无账号、无云同步。

## 1. 本地运行（桌面）

PWA 的 Service Worker 需要 **HTTPS 或 localhost**；直接双击 `index.html` 页面能跑，但不会注册 SW、也不能安装。

```powershell
# 在 pwa/ 目录
# 最省事：双击 启动PWA.bat（自动开服务器并打开浏览器）
python -m http.server 8080
# 或双击 start-server.ps1
```

打开 `http://localhost:8080`。

Chrome/Edge 地址栏右侧会出现“安装”图标；或菜单 → “安装 明理 / 添加到主屏幕”。

> 遇到问题先看 **`安装教程.md`**：电脑/手机两条路线、Netlify/GitHub Pages 部署、10 条排错。

## 2. 手机安装

手机通过 `http://192.168.x.x:8080` 访问时，**不是安全上下文，Service Worker 不会启用**。要装到手机，需要 HTTPS：

- 把整个 `pwa/` 目录部署到 GitHub Pages / Netlify / Vercel / Cloudflare Pages；
- 或用 `ngrok http 8080` / Cloudflare Tunnel 临时提供 HTTPS；
- 然后手机 Chrome 打开 HTTPS 地址 → 菜单 → “添加到主屏幕” / “安装应用”。

iOS Safari：分享 → “添加到主屏幕”。iOS 对 PWA 的支持有限（无安装提示、缓存策略不同），能用但不完全等同 Android。

## 3. 包含文件

```text
pwa/
├─ index.html               # 应用（由 ../html/明理ClearLogic.html 注入 PWA 标签生成）
├─ manifest.webmanifest     # 名称/图标/主题/快捷方式
├─ sw.js                    # 离线缓存与导航回退
├─ icons/
│  ├─ icon-192.png
│  ├─ icon-512.png
│  ├─ icon-maskable-512.png
│  ├─ apple-touch-icon-180.png
│  ├─ favicon-32.png / favicon-64.png
│  └─ icon-1024.png
├─ make_icons.py            # 重新生成图标
├─ make_pwa.py              # 从 HTML 重新生成 PWA index
├─ start-server.ps1         # 本地静态服务器（PowerShell）
├─ 启动PWA.bat              # 本地静态服务器（双击，自动开浏览器）
├─ 安装教程.md              # 保姆级安装/部署/排错
└─ README.md
```

## 4. 数据

- 数据仍存 `localStorage`，按 **origin** 隔离：
  - `http://localhost:8080` 与 `https://your-domain` 是两份数据；
  - 换域名/端口，旧数据不会自动迁移。
- 换地址/换设备前：我的 → 数据与备份 → 导出 JSON → 新地址导入。
- 清理浏览器站点数据、卸载 PWA、无痕模式都会丢数据。

## 5. 更新

1. 修改 `index.html`（或从 `../html/` 重新生成）；
2. 把 `sw.js` 里的 `CACHE = 'mingli-pwa-v1.0.0'` 改成新版本号；
3. 重新部署；
4. 打开应用后刷新一次（或关闭重开），新 SW 生效，旧缓存被清理。

不升 `CACHE` 版本，浏览器可能继续用旧缓存。

## 6. 已知边界

- 不是 APK，不能直接安装到 Android 应用列表；安装的是 PWA（桌面图标/独立窗口）。
- 无账号、云同步、PIN。
- iOS PWA 的离线/安装体验弱于 Android/桌面 Chrome。
- 图标为程序生成的品牌占位，不是正式品牌资产；需要可替换 `icons/`。
- 未做真实浏览器 Lighthouse/安装验收（本环境无法启动图形浏览器）；部署后建议跑一次 Lighthouse PWA 审计。

## 7. 重新生成

```powershell
# 从 HTML 源重新生成 PWA index（保留 PWA 注入标签）
python make_pwa.py
# 重新生成图标
python make_icons.py
```
