<picture>
  <source media="(prefers-color-scheme: dark) and (max-width: 500px)" srcset="assets/masthead-narrow-dark.svg">
  <source media="(max-width: 500px)" srcset="assets/masthead-narrow.svg">
  <source media="(prefers-color-scheme: dark)" srcset="assets/masthead-dark.svg">
  <img src="assets/masthead.svg" width="880" alt="Ardalan Askarian. Open to full-time software and ML roles. Software engineer working on machine learning systems, and the ordinary software that has to hold them up. M.Sc. Computer Science, University of Saskatchewan, Applied ML stream. Computer vision and image processing, under Dr. Mark Eramian. 1,552 hand-labelled reports. 36,407 logged events. 6 participants. 4 models. 1 null result.">
</picture>

<picture><source media="(prefers-color-scheme: dark)" srcset="assets/icon-projects-dark.svg"><img src="assets/icon-projects.svg" width="20" align="texttop" alt=""></picture> [See the work](#-selected-projects) · <picture><source media="(prefers-color-scheme: dark)" srcset="assets/icon-talk-dark.svg"><img src="assets/icon-talk.svg" width="20" align="texttop" alt=""></picture> [Get in touch](#-lets-talk) · <picture><source media="(prefers-color-scheme: dark)" srcset="assets/icon-portfolio-dark.svg"><img src="assets/icon-portfolio.svg" width="20" align="texttop" alt=""></picture> [Portfolio](https://ardalanaskarian.github.io) · <picture><source media="(prefers-color-scheme: dark)" srcset="assets/icon-resume-dark.svg"><img src="assets/icon-resume.svg" width="20" align="texttop" alt=""></picture> [Résumé](https://ardalanaskarian.github.io/icons/resume.pdf)

## <picture><source media="(prefers-color-scheme: dark)" srcset="assets/icon-research-dark.svg"><img src="assets/icon-research.svg" width="30" align="texttop" alt=""></picture> &nbsp;Turning research questions into working systems

Most of my work sits between a research question and the software that answers it: annotation platforms, data pipelines, and the interfaces researchers actually use. A good part of it is checking whether a thing works before claiming that it does.

I'm a Master's student specializing in Applied Machine Learning, researching computer vision and image processing under Dr. Mark Eramian. Before that, a B.Sc. Honours in Computer Science, Software Engineering option.

## <picture><source media="(prefers-color-scheme: dark)" srcset="assets/icon-projects-dark.svg"><img src="assets/icon-projects.svg" width="30" align="texttop" alt=""></picture> &nbsp;Selected projects

Research first, then apps and games. Open any one for the detail.

### <picture><source media="(prefers-color-scheme: dark)" srcset="assets/icon-bug-dark.svg"><img src="assets/icon-bug.svg" width="24" align="texttop" alt=""></picture> &nbsp;Fine-tuning LLMs for bug classification

Fine-tuned code transformers to sort GitHub bug reports into seven categories, benchmarked against classical ML on a hand-labelled corpus.

<details>
<summary>Read more</summary>

<picture>
  <source media="(prefers-color-scheme: dark) and (max-width: 500px)" srcset="assets/bench-narrow-dark.svg">
  <source media="(max-width: 500px)" srcset="assets/bench-narrow.svg">
  <source media="(prefers-color-scheme: dark)" srcset="assets/bench-dark.svg">
  <img src="assets/bench.svg" width="880" alt="Bug classification accuracy. GraphCodeBERT 94.54 percent, CodeBERT 93.99 percent, DistilBERT 92.90 percent, all fine-tuned transformers. Naive Bayes, the classical baseline, 74.59 percent. 1,552 hand-labelled reports across seven categories, agreement checked with Fleiss' Kappa.">
</picture>

| | |
|:--|:--|
| <picture><source media="(prefers-color-scheme: dark)" srcset="assets/icon-built-dark.svg"><img src="assets/icon-built.svg" width="20" align="texttop" alt=""></picture> **Built** | A labelling protocol, a scraper over the GitHub API, and one fine-tuning harness run across four models on one corpus |
| <picture><source media="(prefers-color-scheme: dark)" srcset="assets/icon-result-dark.svg"><img src="assets/icon-result.svg" width="20" align="texttop" alt=""></picture> **Result** | GraphCodeBERT **94.54%** · CodeBERT 93.99% · DistilBERT 92.90% · Naïve Bayes 74.59% |
| <picture><source media="(prefers-color-scheme: dark)" srcset="assets/icon-with-dark.svg"><img src="assets/icon-with.svg" width="20" align="texttop" alt=""></picture> **With** | Princess Tayab, Timofei Kabakov, Marmik Patel · January to April 2025 |
| <picture><source media="(prefers-color-scheme: dark)" srcset="assets/icon-tools-dark.svg"><img src="assets/icon-tools.svg" width="20" align="texttop" alt=""></picture> **Stack** | Python · PyTorch · Transformers · CodeBERT · scikit-learn · GitHub API |

> Four people had to agree, 1,552 times, on whether a thing was a runtime bug or a logical one. That is what Fleiss' Kappa is measuring, and it is the part that never shows up in the accuracy column.

[Repo](https://github.com/ArdalanAskarian/LLM-Bug-Classification-Research) · [Full paper](https://drive.google.com/file/d/1-EZ82nrDkz-cz7pluI41sm9CC6QkuIQV/view?usp=sharing) · [Presentation](https://docs.google.com/presentation/d/1UArFkzsltQq3Azejfe2cvDD90rAO6j08/edit?usp=sharing)

</details>

### <picture><source media="(prefers-color-scheme: dark)" srcset="assets/icon-annotate-dark.svg"><img src="assets/icon-annotate.svg" width="24" align="texttop" alt=""></picture> &nbsp;SIFT-assisted image annotation

An annotation platform built to answer one question honestly: does machine assistance make human annotators better, or just busier?

<details>
<summary>Read more</summary>

<picture>
  <source media="(prefers-color-scheme: dark) and (max-width: 500px)" srcset="assets/study-narrow-dark.svg">
  <source media="(max-width: 500px)" srcset="assets/study-narrow.svg">
  <source media="(prefers-color-scheme: dark)" srcset="assets/study-dark.svg">
  <img src="assets/study.svg" width="880" alt="Change from the manual baseline. Annotation time: plus 71.6 percent. IoU: no measurable change. Ground-truth coverage: no measurable change. SIFT-assisted annotation took 1.72 times as long as the manual baseline. 6 participants, 36,407 logged interaction events.">
</picture>

| | |
|:--|:--|
| <picture><source media="(prefers-color-scheme: dark)" srcset="assets/icon-built-dark.svg"><img src="assets/icon-built.svg" width="20" align="texttop" alt=""></picture> **Built** | A Django platform that proposed SIFT-derived bounding boxes for a human to accept, adjust or reject, logging every interaction against a manual baseline |
| <picture><source media="(prefers-color-scheme: dark)" srcset="assets/icon-result-dark.svg"><img src="assets/icon-result.svg" width="20" align="texttop" alt=""></picture> **Result** | Assistance cost **71.6%** more time and returned no measurable gain in IoU or ground-truth coverage · 6 participants · 36,407 logged events |
| <picture><source media="(prefers-color-scheme: dark)" srcset="assets/icon-with-dark.svg"><img src="assets/icon-with.svg" width="20" align="texttop" alt=""></picture> **With** | Dr. Mark Eramian, Imaging &amp; AI Lab · NSERC USRA, May to August 2025 · co-authored research poster |
| <picture><source media="(prefers-color-scheme: dark)" srcset="assets/icon-tools-dark.svg"><img src="assets/icon-tools.svg" width="20" align="texttop" alt=""></picture> **Stack** | Django · Python · SIFT · OpenCV · JavaScript |

> Reviewing a wrong proposal costs more than drawing a box from scratch, and confidence in a suggestion is not the same thing as its accuracy.

</details>

### <picture><source media="(prefers-color-scheme: dark)" srcset="assets/icon-signal-dark.svg"><img src="assets/icon-signal.svg" width="24" align="texttop" alt=""></picture> &nbsp;Dreaming Machines

<img src="banner.gif" width="420" alt="Dreaming Machines, VR experience footage">

Biometric VR driven by a live pulse sensor.

<details>
<summary>Read more</summary>

<picture>
  <source media="(prefers-color-scheme: dark) and (max-width: 500px)" srcset="assets/signal-narrow-dark.svg">
  <source media="(max-width: 500px)" srcset="assets/signal-narrow.svg">
  <source media="(prefers-color-scheme: dark)" srcset="assets/signal-dark.svg">
  <img src="assets/signal.svg" width="880" alt="One heartbeat, four hops. Pulse sensor reads the pulse as an analog signal. Arduino turns it into BPM and IBI. Wi-Fi carries both values into Unity. Unity shader gives breathing and pulsing effects in real time. Phone: a swiped card spawns an object in VR. Team of 4, MIT Reality Hack 2026.">
</picture>

| | |
|:--|:--|
| <picture><source media="(prefers-color-scheme: dark)" srcset="assets/icon-built-dark.svg"><img src="assets/icon-built.svg" width="20" align="texttop" alt=""></picture> **Built** | A Meta Quest experience, a phone companion app that feeds content in as dream artifacts, and the wire between a fingertip and a shader |
| <picture><source media="(prefers-color-scheme: dark)" srcset="assets/icon-result-dark.svg"><img src="assets/icon-result.svg" width="20" align="texttop" alt=""></picture> **Result** | Live biometrics driving the environment in real time, demoed at MIT Reality Hack 2026 |
| <picture><source media="(prefers-color-scheme: dark)" srcset="assets/icon-with-dark.svg"><img src="assets/icon-with.svg" width="20" align="texttop" alt=""></picture> **With** | Samantha Herle (design and PM), Sean Rove (tech art), Ben Branch (hardware) · Ardalan Askarian on software |
| <picture><source media="(prefers-color-scheme: dark)" srcset="assets/icon-tools-dark.svg"><img src="assets/icon-tools.svg" width="20" align="texttop" alt=""></picture> **Stack** | Unity 6 · OpenXR · XR Toolkit · Node.js · WebSocket · Three.js · Arduino · C# |

[Repo](https://github.com/ArdalanAskarian/dream_hackers) · [Demo video](https://www.youtube.com/watch?v=NY5WnzpsTtc) · [Pitch deck](https://docs.google.com/presentation/d/1j2qTOKgDBow35dwZyvudL7hVXUyHlVYta0Yu95tXGPk/edit?usp=sharing)

</details>

### <picture><source media="(prefers-color-scheme: dark)" srcset="assets/icon-pipeline-dark.svg"><img src="assets/icon-pipeline.svg" width="24" align="texttop" alt=""></picture> &nbsp;BEAP Engine

Smartwatch data ingestion and analytics.

<details>
<summary>Read more</summary>

<picture>
  <source media="(prefers-color-scheme: dark) and (max-width: 500px)" srcset="assets/pipeline-narrow-dark.svg">
  <source media="(max-width: 500px)" srcset="assets/pipeline-narrow.svg">
  <source media="(prefers-color-scheme: dark)" srcset="assets/pipeline-dark.svg">
  <img src="assets/pipeline.svg" width="880" alt="From vendor export to something plottable. Ingestion: wearable exports arrive, one format per vendor. Processing: machine learning normalises the formats. Analytics: an interface researchers actually use. Software Developer Intern, October 2024 to September 2025.">
</picture>

| | |
|:--|:--|
| <picture><source media="(prefers-color-scheme: dark)" srcset="assets/icon-built-dark.svg"><img src="assets/icon-built.svg" width="20" align="texttop" alt=""></picture> **Built** | Ingestion, processing and analytics for wearable sensor data, with the interface rebuilt in React and TypeScript |
| <picture><source media="(prefers-color-scheme: dark)" srcset="assets/icon-result-dark.svg"><img src="assets/icon-result.svg" width="20" align="texttop" alt=""></picture> **Result** | Vendor exports that disagree on shape, parsed into one the analytics can read |
| <picture><source media="(prefers-color-scheme: dark)" srcset="assets/icon-with-dark.svg"><img src="assets/icon-with.svg" width="20" align="texttop" alt=""></picture> **With** | BEAP Lab · Software Developer Intern, October 2024 to September 2025 |
| <picture><source media="(prefers-color-scheme: dark)" srcset="assets/icon-tools-dark.svg"><img src="assets/icon-tools.svg" width="20" align="texttop" alt=""></picture> **Stack** | React · TypeScript · Python · Data processing |

</details>

### <picture><source media="(prefers-color-scheme: dark)" srcset="assets/icon-also-dark.svg"><img src="assets/icon-also.svg" width="24" align="texttop" alt=""></picture> &nbsp;Also

| | | |
|:--|:--|:--|
| <picture><source media="(prefers-color-scheme: dark)" srcset="assets/icon-schedule-dark.svg"><img src="assets/icon-schedule.svg" width="24" align="texttop" alt=""></picture> | [Sports Scheduling App](https://github.com/ArdalanAskarian/Sports-Scheduler) | front end for a team-management app |
| <picture><source media="(prefers-color-scheme: dark)" srcset="assets/icon-weather-dark.svg"><img src="assets/icon-weather.svg" width="24" align="texttop" alt=""></picture> | [Weather App](https://github.com/ArdalanAskarian/Ardalan-Weather-App) | a native Swift client for live forecasts |
| <picture><source media="(prefers-color-scheme: dark)" srcset="assets/icon-maps-dark.svg"><img src="assets/icon-maps.svg" width="24" align="texttop" alt=""></picture> | [Dentistry Website](https://github.com/ArdalanAskarian/Dentist-Website) | booking flow and integrated maps |
| <picture><source media="(prefers-color-scheme: dark)" srcset="assets/icon-tower-dark.svg"><img src="assets/icon-tower.svg" width="24" align="texttop" alt=""></picture> | [Darkness Defenders](https://github.com/ArdalanAskarian/Darkness-Defenders) | a Unity tower defence with layered enemy AI |

[Browse every repo](https://github.com/ArdalanAskarian?tab=repositories)

## <picture><source media="(prefers-color-scheme: dark)" srcset="assets/icon-work-dark.svg"><img src="assets/icon-work.svg" width="30" align="texttop" alt=""></picture> &nbsp;Where I've worked

<picture>
  <source media="(prefers-color-scheme: dark) and (max-width: 500px)" srcset="assets/tenure-narrow-dark.svg">
  <source media="(max-width: 500px)" srcset="assets/tenure-narrow.svg">
  <source media="(prefers-color-scheme: dark)" srcset="assets/tenure-dark.svg">
  <img src="assets/tenure.svg" width="880" alt="Three roles, one overlapping summer. Teaching Assistant, January 2023 to now. Software Developer Intern, October 2024 to September 2025. Research Assistant, May to August 2025. All three overlap through the summer of 2025. Projects: bug classification January to April 2025, annotation study May to August 2025, BEAP Engine October 2024 to September 2025, Dreaming Machines January 2026.">
</picture>

| | Role | |
|:--|:--|:--|
| Jan 2023 – present | **Teaching Assistant** | Department of Computer Science · six core courses, including CMPT 332 Operating Systems |
| May – Aug 2025 | **Research Assistant, NSERC USRA** | Imaging & AI Lab · the annotation study above |
| Oct 2024 – Sep 2025 | **Software Developer Intern** | BEAP Lab · BEAP Engine |

Two awards came out of the teaching side: the TESL Saskatchewan Bursary in 2022, one of two given province-wide, and the EAP Scholarship in 2020 as the highest achiever in English for Academic Purposes.

## <picture><source media="(prefers-color-scheme: dark)" srcset="assets/icon-stack-dark.svg"><img src="assets/icon-stack.svg" width="30" align="texttop" alt=""></picture> &nbsp;Stack

<picture>
  <source media="(prefers-color-scheme: dark) and (max-width: 500px)" srcset="assets/stack-narrow-dark.svg">
  <source media="(max-width: 500px)" srcset="assets/stack-narrow.svg">
  <source media="(prefers-color-scheme: dark)" srcset="assets/stack-dark.svg">
  <img src="assets/stack.svg" width="880" alt="Thirty-two things, weighted by how current. Filled chips are in a project this term, tinted a few times a year, outlined used but not current. 32 entries: 11 daily, 14 regular, 7 familiar.">
</picture>

|  | Daily | Regular | Familiar |
|:--|:--|:--|:--|
| **Languages** | Python, TypeScript, JavaScript | C, Java, SQL | C#, PHP, R |
| **Vision & ML** | PyTorch, OpenCV, SIFT | scikit-learn, Transformers, segmentation | TensorFlow |
| **Web** | React, Django | Node.js, Next.js, React Native, Express | Flask |
| **Data** | PostgreSQL | MongoDB, MySQL | SQLite |
| **Tools** | Git, Unix/Linux | Docker, Playwright | Unity |

## <picture><source media="(prefers-color-scheme: dark)" srcset="assets/icon-activity-dark.svg"><img src="assets/icon-activity.svg" width="30" align="texttop" alt=""></picture> &nbsp;Activity

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://streak-stats.demolab.com/?user=ArdalanAskarian&background=0e0f13&border=24272e&stroke=24272e&ring=343841&fire=0e0f13&currStreakNum=eceff0&currStreakLabel=3ecec2&sideNums=eceff0&sideLabels=8a8f99&dates=656a74&border_radius=14&card_width=880&disable_animations=true">
  <img src="https://streak-stats.demolab.com/?user=ArdalanAskarian&background=fbfbfc&border=e6e7ea&stroke=e6e7ea&ring=d3d5da&fire=fbfbfc&currStreakNum=14161c&currStreakLabel=0f7f77&sideNums=14161c&sideLabels=666b75&dates=9498a1&border_radius=14&card_width=880&disable_animations=true" width="880" alt="Total contributions since January 13, 2023. Current streak, and longest streak.">
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/ArdalanAskarian/ArdalanAskarian/output/github-snake-dark.svg">
  <img src="https://raw.githubusercontent.com/ArdalanAskarian/ArdalanAskarian/output/github-snake.svg" width="880" alt="Contribution graph rendered as a snake animation">
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://github-readme-activity-graph.vercel.app/graph?username=ArdalanAskarian&bg_color=0e0f13&color=eceff0&title_color=eceff0&line=8a8f99&point=eceff0&area=true&area_color=343841&radius=14&grid=false&custom_title=Contributions%2C%20last%2031%20days">
  <img src="https://github-readme-activity-graph.vercel.app/graph?username=ArdalanAskarian&bg_color=fbfbfc&color=14161c&title_color=14161c&line=666b75&point=14161c&area=true&area_color=d3d5da&radius=14&grid=false&custom_title=Contributions%2C%20last%2031%20days" width="880" alt="Contributions per day over the last 31 days">
</picture>

## <picture><source media="(prefers-color-scheme: dark)" srcset="assets/icon-talk-dark.svg"><img src="assets/icon-talk.svg" width="30" align="texttop" alt=""></picture> &nbsp;Let's talk.

I'm looking for full-time software and machine learning roles, and I'm interested in research collaborations in computer vision. I answer every email.

<picture><source media="(prefers-color-scheme: dark)" srcset="assets/icon-talk-dark.svg"><img src="assets/icon-talk.svg" width="20" align="texttop" alt=""></picture> [ardalan.askarian@usask.ca](mailto:ardalan.askarian@usask.ca) · <picture><source media="(prefers-color-scheme: dark)" srcset="assets/icon-github-dark.svg"><img src="assets/icon-github.svg" width="20" align="texttop" alt=""></picture> [GitHub](https://github.com/ArdalanAskarian) · <picture><source media="(prefers-color-scheme: dark)" srcset="assets/icon-linkedin-dark.svg"><img src="assets/icon-linkedin.svg" width="20" align="texttop" alt=""></picture> [LinkedIn](https://linkedin.com/in/ardalan-askarian-79221a24b) · <picture><source media="(prefers-color-scheme: dark)" srcset="assets/icon-portfolio-dark.svg"><img src="assets/icon-portfolio.svg" width="20" align="texttop" alt=""></picture> [Portfolio](https://ardalanaskarian.github.io) · <picture><source media="(prefers-color-scheme: dark)" srcset="assets/icon-resume-dark.svg"><img src="assets/icon-resume.svg" width="20" align="texttop" alt=""></picture> [Résumé](https://ardalanaskarian.github.io/icons/resume.pdf)
