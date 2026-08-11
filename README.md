# SkyPalace

SkyPalace 是一个生成中式天宫奇观图片与视频的通用 Skill。用户只需提供一句中文创意，`$make-sky-palace-video` 就会把它展开为世界观、奇观递进分镜、逐镜图片提示词、逐镜图生视频提示词、生成执行方案和质量报告。

它解决的不是“再写一段仙侠关键词”，而是四个容易失败的问题：

- 只有大建筑，没有真正违反常规尺度的奇观关系。
- 画面很满，人物没有继续行动的空间。
- 图片提示词很细，视频提示词却只有“镜头缓慢推进”。
- 六个镜头像六张壁纸，没有召唤、穿越、反转和抵达的升级。

Skill 使用“不可能关系＋四级尺度链＋出框延伸＋延迟揭示”构建奇观，并把摄影机、人物、环境、视差、连续性与防漂移要求精确写进同一个视频提示词段落。

人物不是画面主体，而是尺度单位：默认只占画面高度 `0.25%–0.8%`，关键巨物镜头优先 `0.3%–0.6%`，并明确写成“人物小于门钉或栏杆局部”。主巨构占画面 `45%–65%` 且至少一处出框，用近乎点状的人类轮廓衬托建筑不合理的宏大。

## 能生成什么

- 原创东方天宫、天门、云海、天河、神廊、镜海、浮空大陆和天体级奇观。
- 默认六镜头、30 秒、16:9 的电影级超写实天宫朝圣短片。
- 横屏、竖屏、单人、双人或无人物奇观。
- 六张独立关键帧提示词和六条独立图生视频提示词。
- 在当前环境有生成工具时继续生图、生成视频片段和质检。
- 没有生成工具时交付完整生产包，不伪造媒体结果。

## 安装

### 方法一：使用 Codex Skill 安装脚本

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo renmu2017/SkyPalace \
  --path skills/make-sky-palace-video
```

如果设置了自定义 `CODEX_HOME`，把脚本路径和目标 Skill 目录替换成对应位置。

### 方法二：手动复制

```bash
git clone https://github.com/renmu2017/SkyPalace.git
mkdir -p ~/.codex/skills
cp -R SkyPalace/skills/make-sky-palace-video ~/.codex/skills/
```

安装后新建一个 Codex 任务，或让当前环境重新加载 Skills。Skill 的实际入口名称是：

```text
$make-sky-palace-video
```

## 一句话使用

```text
使用 $make-sky-palace-video，把“巨月打开天门，两位旧友沿倒流天河赴九重天宫旧约”做成30秒横屏天宫奇观视频。
```

也可以更短：

```text
用 $make-sky-palace-video 生成一支无人物的星海瀑布天宫视频。
```

```text
使用 $make-sky-palace-video 做15秒竖屏：暴雨散去后，一位女剑客穿过通天神廊看见晨星天宫。
```

没有说明时采用以下默认值：

| 参数 | 默认值 |
| --- | --- |
| 镜头数 | 6 |
| 总时长 | 30 秒 |
| 画幅 | 16:9 |
| 风格 | 电影级超写实东方神话史诗 |
| 人物 | 两位背向镜头、仅占画面高度 0.25%–0.8% 的极小同行者 |
| 建筑 | 原创白玉天阙与天河云宫 |
| 提示词语言 | 精细中文，保留少量通用摄影英文 |

可以在一句话中指定：时长、画幅、人物、天气、时段、主奇观、情绪、镜头数量和交付模式。只有付费调用、必需参考图缺失、输入冲突或具体 IP 复刻风险会触发追问。

## 四种交付模式

| 模式 | 用户说法示例 | 交付 |
| --- | --- | --- |
| 仅提示词 | “只要提示词，不实际生成” | 简报、世界观、分镜、图片与视频提示词 |
| 关键帧 | “帮我把六张关键帧也生成” | 提示词、独立关键帧、图片质检 |
| 视频片段 | “生成每个分镜的视频片段” | 通过的关键帧、逐镜片段、视频质检 |
| 完整生产包 | “给我完整生产包” | 全部文件、剪辑顺序、声音建议、状态与验证报告 |

有工具时，Skill 按当前可用能力执行；没有工具时自动降级为完整提示词生产包，状态停在 `video_prompts_ready`。

## 生产流程

```text
一句话创意
  → brief.json
  → world-bible.md
  → 六镜头奇观曲线
  → 逐镜图片提示词
  → 独立关键帧与图片质检
  → 单段图生视频提示词
  → 独立视频片段与视频质检
  → 剪辑建议和最终状态
```

每个镜头只有一个主奇观，最多两个辅助奇观。默认六镜结构为：

```text
召唤 → 仰望 → 进入 → 穿越 → 反转 → 抵达
```

第五镜必须至少完成一次认知反转，例如“原以为道路通向月亮，后来发现人物已经走在月亮内部”。

## 生成目录

运行项目初始化器或由 Skill 落盘后，会得到：

```text
sky-palace-project/
├── brief.json
├── world-bible.md
├── storyboard.md
├── prompts/
│   ├── image/
│   │   ├── 01.txt
│   │   └── ...
│   └── video/
│       ├── 01.txt
│       └── ...
├── images/
├── clips/
├── qa-report.json
└── status.json
```

`status.json` 明确区分“提示词已完成”“图片已生成”“视频已生成”和“完整交付”，避免把计划、网页预览或命令成功误报为媒体已完成。

## 两个辅助脚本

### 初始化生产包

```bash
python3 skills/make-sky-palace-video/scripts/init_project.py \
  --output ./output \
  --slug moon-gate \
  --prompt '巨月打开天门，两位旧友沿倒流天河赴约' \
  --duration 30 \
  --shots 6 \
  --aspect-ratio 16:9
```

脚本不会覆盖已有非空项目。初始化后的空包尚未包含正式分镜和提示词，因此此时运行完整校验会按预期报告缺项。

### 校验生产包

```bash
python3 skills/make-sky-palace-video/scripts/validate_package.py ./output/moon-gate
```

需要机器可读结果时：

```bash
python3 skills/make-sky-palace-video/scripts/validate_package.py ./output/moon-gate --json
```

校验器会检查必需文件、镜头顺序、主奇观重复、不可能关系、四级尺度链、留白比例、行动区、提示词数量与长度、视频单段结构和付费授权状态。退出码 `0` 表示通过，`1` 表示存在阻塞错误。

## 图片提示词设计

每条图片提示词是一个完整段落，依次包含：

```text
输出约束 → 世界与真实度 → 核心奇观 → 前中远极远四层空间 →
建筑结构 → 人物连续性 → 摄影机 → 构图比例 →
光线与空气 → 色彩与材质 → 失败规避
```

主要构图指标：

- 主巨构视觉占比通常为 45%–65%，至少一处主动出框。
- 人物高度仅为画面 0.25%–0.8%，关键镜头优先 0.3%–0.6%；人物小于门钉、栏杆局部或柱身铆钉。
- 天空、云海、镜面或远山形成 28%–42% 的有效留白。
- 人物行动区约占画面下方 22%–32%。
- 有人物时，人物前方至少保留画面宽度 30% 的无遮挡连续路径。
- 尺度由人物或白鸟、栏杆或门钉、山峰或巨柱、月轮或宫城组成四级尺度链。

## 视频提示词设计

每条视频提示词必须是一个无空行的单段：

```text
首帧锁定 → 摄影机轨迹 → 人物动作 → 分层环境运动 →
视差 → 揭示节拍 → 结束状态 → 连续性与防漂移
```

巨构本身保持刚性稳定。主要运动来自摄影机、前景遮挡、云、水、光、衣袂和白鸟。视频提示词不会另拆“否定词”，而是在段尾自然写入与当前镜头有关的防变形和防漂移要求。

## 工具兼容

Skill 不绑定单一供应商：

- 有生图工具：逐镜独立生成关键帧，禁止用多格拼图替代。
- 有图生视频工具：每张通过的关键帧单独生成片段。
- 只有浏览器：使用用户当前真实登录态；遇到验证码、强制登录或账号风险立即停止。
- 生成工具不可用：输出全部提示词、分镜和参数建议，不声称已生成媒体。
- 有首尾帧能力：只在两帧空间差异合理时使用，避免强迫模型完成不可实现的变形。

仓库不包含 API Key、Cookie、账号登录态或特定平台凭证。

## 费用与发布边界

- 本 Skill 本身不产生图片或视频费用。
- 任何可能产生付费的生成调用前，必须说明模型、次数、预计产物和已知成本边界，并等待用户明确确认。
- 增加镜头、重试或更换付费模型超出原确认范围时，需要再次确认。
- Skill 不自动发布到抖音、小红书、YouTube 或其他平台。
- 不尝试绕过验证码、平台限制或账号风险提示。

## 仓库结构

```text
SkyPalace/
├── README.md
├── skills/make-sky-palace-video/
│   ├── SKILL.md
│   ├── agents/openai.yaml
│   ├── references/
│   │   ├── visual-bible.md
│   │   ├── wonder-design.md
│   │   ├── image-prompts.md
│   │   ├── video-prompts.md
│   │   ├── shot-library.md
│   │   ├── quality-gates.md
│   │   └── examples.md
│   └── scripts/
│       ├── init_project.py
│       └── validate_package.py
├── tests/
└── docs/superpowers/
```

精细视觉知识位于 `references/`，`SKILL.md` 只保留核心工作流和资源路由，避免每次调用加载全部长文。

## 验证开发版本

运行仓库测试：

```bash
python3 -m unittest discover -s tests -v
```

运行 Codex 官方 Skill 结构校验器：

```bash
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py \
  skills/make-sky-palace-video
```

官方 `quick_validate.py` 需要 PyYAML；如果系统 Python 缺少依赖，请使用 Codex 自带的 Python 运行时或在独立虚拟环境中安装 PyYAML，不要修改 Skill 代码来绕过校验。

验证示例生产包：

```bash
python3 skills/make-sky-palace-video/scripts/validate_package.py \
  tests/fixtures/valid-package
```

## 故障排查

### Skill 没有触发

- 确认目录名为 `make-sky-palace-video`，并且直接包含 `SKILL.md`。
- 新建 Codex 任务或重新加载 Skills。
- 显式写 `$make-sky-palace-video`，不要只写仓库名 SkyPalace。

### 画面很美但没有奇观感

- 把抽象形容词改成明确的不可能关系，例如“天河从云海逆流并托举天宫大陆”。
- 补齐人物/白鸟→栏杆/门钉→山峰/巨柱→月轮/宫城的四级尺度链。
- 极力缩小人物；若人物超过画面 1% 且不是用户明确要求的近景，直接重做。
- 让巨构至少一处出框，并通过前景遮挡延迟揭示。
- 删除辅助浮岛、瀑布和宫殿，恢复有效留白。

### 人物没有行动空间

- 扩大中景桥面、平台、神阶或浅水庭院。
- 明确人物前方至少有画面宽度 30% 的无遮挡连续路径。
- 删除横向栏杆、浓雾、断桥和正对人物的门墙。

### 视频建筑漂移或人物滑行

- 降低运动强度，只保留一个摄影机主轨迹和一个人物主动作。
- 复述需要锁定的建筑、人物、光线和道路，不写“保持上一张一样”。
- 让巨构保持静止，用云、水、光、衣袂和前景视差制造运动。

### 生成工具不可用

这是受支持的降级路径。Skill 会完成世界观、分镜、图片提示词与视频提示词，`status.json` 停在 `video_prompts_ready`。更换环境或配置工具后，可以从该阶段继续，不需要重写全部内容。

### 浏览器出现验证码或账号风险

立即停止自动操作，由用户手动处理。不要绕过验证码、强制登录、账号异常或平台警告。

## 完整范例

从一句话到六镜图片与视频提示词的完整示例位于：

[`skills/make-sky-palace-video/references/examples.md`](skills/make-sky-palace-video/references/examples.md)
