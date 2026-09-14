# 原始资料索引

本目录统一保存 Vitent AI 教育项目使用的原始资料。可编辑文档分别保存在 `docs/curriculum-design/` 和 `docs/research-analysis/`，原始文件不在此处直接改写。

## 目录结构

```text
source/
├── competitor-curricula/   竞品公开课程页、课程目录和项目清单快照
├── project-documents/       项目早期讨论稿的原始 DOCX
└── standards/               课程标准与学生能力框架原文
    ├── china/               中国义务教育课程方案和课程标准
    ├── us/                  美国 K-12 学术与能力标准
    └── international/       国际组织发布的能力框架
```

## 已归档内容

| 分类 | 内容 | 文件数量 | 详细索引 |
| --- | --- | ---: | --- |
| 项目原稿 | 商业模式、完整讨论稿、单节课结构设计 | 3 份 DOCX | [project-documents](project-documents/) |
| 竞品课程资料 | 15 个国内外产品的公开课程页、项目页和资源索引 | 31 份网页/索引文件 | [竞品课程资料索引](competitor-curricula/README.md) |
| 中国标准 | 义务教育课程方案及16门课程标准（2022年版）、两份中小学AI教育指南（2025） | 17 份 PDF、2 份 HTML | [中国标准索引](standards/china/README.md) |
| 美国标准 | CCSS、NGSS、CSTA、WIDA、NCAS、AI4K12 | 15 份 PDF | [美国标准索引](standards/us/README.md) |
| 国际框架 | UNESCO学生人工智能能力框架（2024）、OECD/欧盟AI素养框架（2026） | 2 份 PDF | [国际标准索引](standards/international/README.md) |

共归档 70 份原始文件或网页快照，其中本次新增竞品课程资料 31 份。

## 维护规则

1. 原始文件应按发布机构或国家/地区归档，不与分析稿混放。
2. 每个标准集合保留来源、版本、适用范围和版权说明。
3. 新增或替换原始标准时，应同步更新对应目录的 `README.md`。
4. 课程设计或分析文档引用原始资料时，使用相对路径，确保 GitHub 中可以直接打开。
5. 不将第三方转述、营销材料或来源不明的文件作为标准原文归档。
