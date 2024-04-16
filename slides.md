---
theme: seriph
background: https://cover.sli.dev
title: AIFS, Artificial Intelligence File System
info: 
  中期汇报
class: text-center
highlighter: shiki
drawings:
  persist: false
transition: slide-left
mdc: true
---

# AIFS: Artificial Intelligence File System

## 中期汇报

<br>

汇报小组: ArkFS 

成员：杨柄权、常圣、李岱峰、刘明乐

汇报人: 杨柄权

<div class="pt-12">
  <span @click="$slidev.nav.next" class="px-2 py-1 rounded cursor-pointer" hover="bg-white bg-opacity-10">
    Press Space for next page <carbon:arrow-right class="inline"/>
  </span>
</div>

---
layout: image-left
image: https://cover.sli.dev
---

# 目录

<Toc v-click minDepth="1" maxDepth="1"></Toc>

---
transition: slide-right
---

# 项目简介



---
transition: fade-out
---

# 项目背景

近年来，大语言模型发展迅猛，已经在许多领域取得了广泛的应用。


<Transform :scale="0.8">

![AI](https://cioctocdo.com/sites/default/files/inline-images/2e8bfd65-5272-4cf1-8b86-954bab975bab_2400x1350.jpg)

</Transform>

---
layout: image-right
image: https://cover.sli.dev
---

# 理论依据

## Ext4文件系统

<v-click>

Ext4是第四代扩展文件系统，是Linux系统下的日志文件系统，是Ext3文件系统的后继版本。

</v-click>

<v-click>

- 向后兼容性 

- 大文件系统 

- 分配方式改进 

- 无限制的子目录 

- 日志校验 

- 在线碎片整理 
  
</v-click>

---
transition: slide-up
---

# 技术可行性

## 大语言模型
