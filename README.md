# 大数据安全课程大作业项目-语音对抗攻击

参考论文：[Defending Your Voice: Adversarial Attack on Voice Conversion](https://arxiv.org/abs/2005.08781)，

使用对抗攻击来防止他人不当利用语音转换，当对输入语音加上对抗噪声时，语音转换会失败。

## 队伍

队伍：没想好名字队

队员：郭琪、陈风赫、牙祖淦

分工：[分工表](https://kdocs.cn/l/cblvAAGeFvl0)

贡献：郭琪（62%）、陈风赫（25%）、牙祖淦（13%）

## 语音转换模型

[AUTOVC](https://arxiv.org/abs/1905.05879) 模型

[Chou'Model](https://arxiv.org/abs/1904.05742) 模型

## 文件夹`model\`缺失文件

由于文件过大，[点击此处](https://drive.google.com/drive/folders/1vGU7DdfuebG1y8f4s4MOqEMunzsxxAHX) 获取文件 `model.ckpt` 。

## 攻击

你可以使用 `attack.py` 对 两种语音转换模型 执行对抗攻击。

```bash
python attack.py <model_dir> <vc_tgt> <adv_tgt> <output> [--vc_src source] [--eps epsilon] [--n_iters iterations] [--attack_type type]
```

- **model_dir**: 模型文件所在目录。
- **vc_tgt**: 需要防护的目标语音，提供语音转换中的音色信息。
- **adv_tgt**: 对抗攻击使用的目标（论文中的 y）。
- **output**: 输出的防护语音。
- **source**: 提供语言内容的源语音（在端到端和反馈攻击中需要）。
- **epsilon**: 扰动的最大幅度。
- **iterations**: 更新扰动的迭代次数。
- **type**: 使用的对抗攻击类型（端到端攻击、嵌入攻击或反馈攻击）。

## 转换测试

你可以使用 inference.py 执行语音转换。

```bash
python inference.py <model_dir> <source> <target> <output>
```

- **model_dir**: 模型文件所在目录。
- **source**: 提供语言内容的源语音。
- **target**: 提供音色信息的目标语音。
- **output**: 输出的转换语音。

## 系统运行

要启动系统，请运行以下命令：

```bash
python app.py
```
