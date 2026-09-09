# Week 2 — A historical question, two sources, and OCR

## Question

When was the Jingshi Library (京师图书馆), the ancestor of today's National
Library of China, founded — and when did it actually open?

## Answer

The Qing court approved its founding on **宣統元年七月二十五日 (= 9 September
1909)**, by rescript on the Board of Education memorial《奏籌建京師圖書館折》
submitted in the name of Grand Councillor Zhang Zhidong (张之洞), which also
requested the transfer of the Wenjin Pavilion copy of the *Siku Quanshu* at Rehe
to the new library. It **opened to readers on 27 August 1912** (1912年8月27日),
housed temporarily in the Guanghua Temple (广化寺) by the Shichahai lakes. Zhang
Zhidong died about a month after the approval — the dynasty that ordered the
library never saw it work, and neither did the statesman who proposed it.

## Evidence

1. **Contemporary scan + OCR** — 《東方雜誌》第六年第九期 (published
   宣統元年八月二十五日 = 1909-10-08), p. 413, section 「記載一
   宣統元年七月大事記」:
   > **二十五日　學部奏籌建京師圖書館請賞給熱河文津閣四庫全書等　奉　旨依議**
   ("25th day: The Board of Education memorializes on establishing the Metropolitan
   Library and requests the grant of the Wenjin Pavilion *Siku Quanshu* at Rehe,
   etc. — approved by imperial rescript.")
   - Scan: Internet Archive item `dongfangzazhi-1909.10.08`, leaf 11 of 208,
     https://iiif.archive.org/iiif/dongfangzazhi-1909.10.08%2411/full/full/0/default.jpg
     (public domain). Local copy:
     `projects/jingshi_library_1909/sources/raw/dongfangzazhi_6-9_p413_leaf11.jpg`
   - Transcription:
     `projects/jingshi_library_1909/sources/processed/ocr_transcription_p413.md`
     — the key entry was double-checked against two independent high-resolution
     crops of the same page.

2. **Contemporary scan + OCR (timeline context)** — 《東方雜誌》第六年第十期
   (published 宣統元年九月二十五日 = 1909-11-07), p. 429, 「記載一
   宣統元年八月大事記」:
   > 十九日　京張鐵路告成行正式開車禮
   > **二十二日　大學士軍機大臣張之洞卒　奉　諭予諡文襄晉贈太保**
   - Scan: Internet Archive item `dongfangzazhi-1909.11.07`, leaf 7,
     https://iiif.archive.org/iiif/dongfangzazhi-1909.11.07%247/full/full/0/default.jpg
     (public domain). Local copy:
     `projects/jingshi_library_1909/sources/raw/dongfangzazhi_6-10_p429_leaf7.jpg`
   - Transcription:
     `projects/jingshi_library_1909/sources/processed/ocr_transcription_p429.md`
   - Why it matters: it places Zhang Zhidong's death roughly one month after the
     memorial was approved, and the neighbouring "19th day" entry (Jingzhang
     Railway formal opening = 2 Oct 1909) calibrates the lunar-to-solar conversion.

3. **Modern corroboration**
   - National Library of China, official site: 「1909年9月9日清政府批准筹建京师
     图书馆，馆舍设在北京广化寺，1912年8月27日开馆接待读者。」
     https://www.nlc.cn/web/dsb_footer/gygt/lsyg/index_1.shtml
   - 北京日报，《百年国家图书馆的历史，从什刹海边广化寺讲起》：「在宣统元年
     七月二十五日（1909年9月9日）给皇帝上了《奏筹建京师图书馆折》……1912年8月
     正式开馆。」
     https://xinwen.bjd.com.cn/content/s62bc1870e4b01c9fa7b2254f.html
   - 北京青年报（韦力文，中国作家网转载，引奏折首段原文「奏为筹建京师图书馆，
     拟恳天恩赏给热河文津阁所藏《四库全书》……」）：
     http://www.chinawriter.com.cn/n1/2022/0607/c442005-32439746.html

All three modern sources agree with the scan-derived dates (approval
1909-09-09, opening 1912-08-27).

## OCR method

Per the week-02 instructions, methods were tried in the prescribed order:

1. **LLM API (OpenRouter / DeepSeek key in `.env`)** — no API key is available in
   this environment; not used.
2. **PaddleOCR API** — requires a local/service deployment this environment does
   not have; not used.
3. **OpenCode's built-in vision (last resort; used)** — full-page IIIF images plus
   two high-resolution crops of p. 413 were read and transcribed; the key entry
   was verified twice against independent crops. Output:
   `sources/processed/ocr_transcription_p413.md`,
   `sources/processed/ocr_transcription_p429.md`.

Baseline for comparison: the Internet Archive's built-in tesseract (chi_sim) OCR
of p. 413 is pure noise — the saved output
(`sources/processed/ia_tesseract_p413_raw.txt`) contains no readable phrase, and
the strings 學部 / 圖書館 / 文津閣 / 四庫全書 get zero hits across the entire
item's OCR text. Vertical classical-Chinese newspaper print defeats the stock
engine — exactly why this text "had not been effectively machine-transcribed"
and had to be re-OCRed.

## Where the work lives

- Project folder: `projects/jingshi_library_1909/`
- Original scans: `projects/jingshi_library_1909/sources/raw/`
- OCR text: `projects/jingshi_library_1909/sources/processed/`
- Research trail: `projects/jingshi_library_1909/research/research-notes.md`
