<picture>
  <source media="(prefers-color-scheme: dark) and (max-width: 500px)" srcset="assets/masthead-narrow-dark.svg">
  <source media="(max-width: 500px)" srcset="assets/masthead-narrow.svg">
  <source media="(prefers-color-scheme: dark)" srcset="assets/masthead-dark.svg">
  <img src="assets/masthead.svg" width="880" alt="Ardalan Askarian. Open to full-time software and ML roles. Software engineer working on machine learning systems, and the ordinary software that has to hold them up. M.Sc. Computer Science, University of Saskatchewan, Applied ML stream. Computer vision and image processing, under Dr. Mark Eramian.">
</picture>

[See the work](#selected-projects) · [Get in touch](#lets-talk) · [Portfolio](https://ardalanaskarian.github.io) · [Résumé](https://ardalanaskarian.github.io/icons/resume.pdf)

## Turning research questions into working systems

Most of my work sits between a research question and the software that answers it: annotation platforms, data pipelines, and the interfaces researchers actually use. A good part of it is checking whether a thing works before claiming that it does.

I'm a Master's student specializing in Applied Machine Learning, researching computer vision and image processing under Dr. Mark Eramian. Before that, a B.Sc. Honours in Computer Science, Software Engineering option.

## Selected projects

Research first, then apps and games. Open any one for the detail.

### Fine-tuning LLMs for bug classification

Fine-tuned code transformers to sort GitHub bug reports into seven categories, benchmarked against classical ML on a hand-labelled corpus.

<details>
<summary>Read more</summary>

**Overview.** A study comparing fine-tuned language models with traditional ML for automated bug classification. We hand-labelled 1,552 GitHub bug reports from React, VS Code, scikit-learn and TensorFlow into seven categories: syntax, runtime, performance, security, logical, dependency and UI/UX.

**Key results.** Transformers outperformed the traditional approaches by a wide margin. GraphCodeBERT reached 94.54%, CodeBERT 93.99% and DistilBERT 92.90%, against Naïve Bayes at 74.59%. Dataset quality was checked with Fleiss' Kappa inter-rater agreement.

**Team.** Ardalan Askarian, Princess Tayab, Timofei Kabakov, Marmik Patel. January to April 2025.

Python · Transformers · CodeBERT · scikit-learn · GitHub API · PyTorch

[Repo](https://github.com/ArdalanAskarian/LLM-Bug-Classification-Research) · [Full paper](https://drive.google.com/file/d/1-EZ82nrDkz-cz7pluI41sm9CC6QkuIQV/view?usp=sharing) · [Presentation](https://docs.google.com/presentation/d/1UArFkzsltQq3Azejfe2cvDD90rAO6j08/edit?usp=sharing)

</details>

### SIFT-assisted image annotation

An annotation platform built to answer one question honestly: does machine assistance make human annotators better, or just busier?

<details>
<summary>Read more</summary>

<picture>
  <source media="(prefers-color-scheme: dark) and (max-width: 500px)" srcset="assets/study-narrow-dark.svg">
  <source media="(max-width: 500px)" srcset="assets/study-narrow.svg">
  <source media="(prefers-color-scheme: dark)" srcset="assets/study-dark.svg">
  <img src="assets/study.svg" width="880" alt="Change from the manual baseline. Annotation time: plus 71.6 percent. IoU: no measurable change. Ground-truth coverage: no measurable change. SIFT-assisted annotation took 1.72 times as long as the manual baseline. 6 participants, 36,407 logged interaction events.">
</picture>

**Overview.** NSERC USRA research under Dr. Mark Eramian at the Imaging & AI Lab. A Django annotation platform that proposed SIFT-derived bounding boxes for a human to accept, adjust or reject, measured against a manual baseline. Six participants, 36,407 logged interaction events.

**Key finding.** The assistance increased annotation time by 71.6% without improving IoU or ground-truth coverage. So the contribution isn't the platform, it's the account of where the time went: reviewing a wrong proposal costs more than drawing a box from scratch, and confidence in a suggestion is not the same as its accuracy. Co-authored research poster.

**Lab.** Imaging & AI Lab. Ardalan Askarian, Dr. Mark Eramian. May to August 2025.

Django · Python · SIFT · OpenCV · JavaScript

</details>

### Dreaming Machines

<img src="banner.gif" width="420" alt="Dreaming Machines, VR experience footage">

Biometric VR driven by a live pulse sensor.

<details>
<summary>Read more</summary>

**Overview.** Does the Internet dream of itself? An immersive VR experience for Meta Quest where players step inside the internet's dream of humanity. A phone companion app lets participants feed content into the VR space, reinterpreted as symbolic dream artifacts.

**Biometric integration.** An Arduino pulse sensor streams live BPM and IBI over WiFi into Unity, driving custom breathing and pulsing shader effects in real time. Card swiping on the phone spawns objects live in VR.

**Team Dream Hackers.** Samantha Herle (design and PM), Sean Rove (tech art), Ardalan Askarian (software), Ben Branch (hardware). Built at MIT Reality Hack 2026.

Unity 6 · OpenXR · XR Toolkit · Node.js · WebSocket · Three.js · Arduino · C#

[Repo](https://github.com/ArdalanAskarian/dream_hackers) · [Demo video](https://www.youtube.com/watch?v=NY5WnzpsTtc) · [Pitch deck](https://docs.google.com/presentation/d/1j2qTOKgDBow35dwZyvudL7hVXUyHlVYta0Yu95tXGPk/edit?usp=sharing)

</details>

### BEAP Engine

Smartwatch data ingestion and analytics.

<details>
<summary>Read more</summary>

**Overview.** Led full-stack development of the BEAP Engine, a smartwatch data processing and analytics platform built at BEAP Lab. It handles ingestion, processing and analytics of wearable sensor data for research use. I rebuilt the interface in React and TypeScript, and implemented the machine learning that parses inconsistent vendor export formats into something the analytics could use.

**Role.** Software Developer Intern, October 2024 to September 2025.

React · TypeScript · Python · Data processing

</details>

### Also

[Sports Scheduling App](https://github.com/ArdalanAskarian/Sports-Scheduler), front end for a team-management app · [Weather App](https://github.com/ArdalanAskarian/Ardalan-Weather-App), a native Swift client for live forecasts · [Dentistry Website](https://github.com/ArdalanAskarian/Dentist-Website), booking flow and integrated maps · [Darkness Defenders](https://github.com/ArdalanAskarian/Darkness-Defenders), a Unity tower defence with layered enemy AI · [Browse every repo](https://github.com/ArdalanAskarian?tab=repositories)

## Where I've worked

| | Role | |
|:--|:--|:--|
| Jan 2023 – present | **Teaching Assistant** | Department of Computer Science · six core courses, including CMPT 332 Operating Systems |
| May – Aug 2025 | **Research Assistant, NSERC USRA** | Imaging & AI Lab · the annotation study above |
| Oct 2024 – Sep 2025 | **Software Developer Intern** | BEAP Lab · BEAP Engine |

Two awards came out of the teaching side: the TESL Saskatchewan Bursary in 2022, one of two given province-wide, and the EAP Scholarship in 2020 as the highest achiever in English for Academic Purposes.

|  | Daily | Regular | Familiar |
|:--|:--|:--|:--|
| **Languages** | Python, TypeScript, JavaScript | C, Java, SQL | C#, PHP, R |
| **Vision & ML** | PyTorch, OpenCV, SIFT | scikit-learn, Transformers, segmentation | TensorFlow |
| **Web** | React, Django | Node.js, Next.js, React Native, Express | Flask |
| **Data** | PostgreSQL | MongoDB, MySQL | SQLite |
| **Tools** | Git, Unix/Linux | Docker, Playwright | Unity |

<sub>Daily, in a project this term. Regular, several times a year. Familiar, used but not current.</sub>

<details>
<summary>GitHub activity</summary>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/ArdalanAskarian/ArdalanAskarian/output/github-snake-dark.svg">
  <img src="https://raw.githubusercontent.com/ArdalanAskarian/ArdalanAskarian/output/github-snake.svg" width="880" alt="Contribution graph rendered as a snake animation">
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://github-readme-stats.vercel.app/api?username=ArdalanAskarian&show_icons=true&include_all_commits=true&count_private=true&border_color=24272e&bg_color=16181d&title_color=eceff0&text_color=c2c6cd&icon_color=8a8f99">
  <img height="165" alt="GitHub statistics" src="https://github-readme-stats.vercel.app/api?username=ArdalanAskarian&show_icons=true&include_all_commits=true&count_private=true&border_color=e6e7ea&bg_color=ffffff&title_color=14161c&text_color=3b3f49&icon_color=666b75">
</picture>

</details>

## Let's talk.

I'm looking for full-time software and machine learning roles, and I'm interested in research collaborations in computer vision. I answer every email.

[ardalan.askarian@usask.ca](mailto:ardalan.askarian@usask.ca) · [GitHub](https://github.com/ArdalanAskarian) · [LinkedIn](https://linkedin.com/in/ardalan-askarian-79221a24b) · [Portfolio](https://ardalanaskarian.github.io) · [Résumé](https://ardalanaskarian.github.io/icons/resume.pdf)

<sub>Saskatoon, SK. Figures are built by <a href="tools/build_svg.py">tools/build_svg.py</a> from the same tokens as <a href="https://ardalanaskarian.github.io">the portfolio</a>: system fonts, one neutral ramp, and colour reserved for links.</sub>
