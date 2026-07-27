<picture>
  <source media="(prefers-color-scheme: dark) and (max-width: 500px)" srcset="assets/masthead-narrow-dark.svg">
  <source media="(max-width: 500px)" srcset="assets/masthead-narrow.svg">
  <source media="(prefers-color-scheme: dark)" srcset="assets/masthead-dark.svg">
  <img src="assets/masthead.svg" width="880" alt="Ardalan Askarian. Open to full-time software and ML roles. Software engineer working on machine learning systems, and the ordinary software that has to hold them up. M.Sc. Computer Science, University of Saskatchewan, Applied ML stream. Computer vision and image processing, under Dr. Mark Eramian.">
</picture>

[See the work](#selected-projects) · [Get in touch](#lets-talk) · [Portfolio](https://ardalanaskarian.github.io) · [Résumé](https://ardalanaskarian.github.io/icons/resume.pdf)

## Turning research questions into working systems

Most of my work sits between a research question and the software that answers it: annotation platforms, data pipelines, and the interfaces researchers actually use. A good part of it is checking whether a thing works before claiming that it does.

I'm a Master's student specializing in Applied Machine Learning, researching computer vision and image processing under Dr. Mark Eramian. Before that, a B.Sc. Honours in Computer Science, Software Engineering option, at 86%.

## The study

<picture>
  <source media="(prefers-color-scheme: dark) and (max-width: 500px)" srcset="assets/study-narrow-dark.svg">
  <source media="(max-width: 500px)" srcset="assets/study-narrow.svg">
  <source media="(prefers-color-scheme: dark)" srcset="assets/study-dark.svg">
  <img src="assets/study.svg" width="880" alt="Change from the manual baseline. Annotation time: plus 71.6 percent. IoU: no measurable change. Ground-truth coverage: no measurable change. SIFT-assisted annotation took 1.72 times as long as the manual baseline. 6 participants, 36,407 logged interaction events.">
</picture>

**Enhancing Annotation Consistency and Efficiency: A Study of SIFT-Assisted Image Annotation in Computer Vision.** NSERC USRA, Imaging & AI Lab, May to August 2025, with Dr. Mark Eramian.

I built a Django annotation platform that proposed SIFT-derived bounding boxes for a human to accept, adjust, or reject, then measured it against a manual baseline. Six participants, 36,407 logged interaction events.

The assistance made annotation 71.6% slower and produced no measurable improvement in IoU or ground-truth coverage. So the contribution isn't the platform, it's the account of where the time went: reviewing a wrong proposal costs more than drawing a box from scratch, and confidence in a suggestion is not the same as its accuracy. Those are the design lessons the poster reports for anyone building human-in-the-loop annotation systems.

Django · Python · OpenCV · SIFT · image segmentation

## Selected projects

Research first, then apps and games.

### Fine-tuning LLMs for bug classification

Fine-tuned code transformers to sort GitHub bug reports into seven categories, benchmarked against classical ML on a hand-labelled corpus. 1,552 reports from React, VS Code, scikit-learn and TensorFlow, labelled into syntax, runtime, performance, security, logical, dependency and UI/UX, with inter-rater agreement checked using Fleiss' Kappa.

GraphCodeBERT reached 94.54%, CodeBERT 93.99% and DistilBERT 92.90%, against Naïve Bayes at 74.59%.

With Princess Tayab, Timofei Kabakov and Marmik Patel. [Repo](https://github.com/ArdalanAskarian/LLM-Bug-Classification-Research)

### Dreaming Machines

<img src="banner.gif" width="420" alt="Dreaming Machines, VR experience footage">

Does the Internet dream of itself? A VR experience for Meta Quest where players step inside that dream. A companion phone app drives the environment, and an Arduino pulse sensor feeds the player's heartbeat into the shaders in real time over WebSockets, so the world reacts to how calm or agitated the player actually is.

Built at MIT Reality Hack 2026 with Samantha Herle (design and PM), Sean Rove (tech art) and Ben Branch (hardware). Unity 6 · OpenXR · Node.js · Arduino · Three.js. [Repo](https://github.com/ArdalanAskarian/dream_hackers)

### BEAP Engine

A platform for ingesting, processing and analysing smartwatch sensor data at scale. I rebuilt the interface in React and TypeScript, and implemented the machine learning that parses inconsistent vendor export formats into something the analytics could use.

React · TypeScript · Python

### Also

[Sports Scheduling App](https://github.com/ArdalanAskarian/Sports-Scheduler), team management in React Native · [Weather App](https://github.com/ArdalanAskarian/Ardalan-Weather-App) · [Dentistry Website](https://github.com/ArdalanAskarian/Dentist-Website) · [Darkness Defenders](https://github.com/ArdalanAskarian/Darkness-Defenders), a Unity tower defence with layered enemy AI · [Browse every repo](https://github.com/ArdalanAskarian?tab=repositories)

## Experience

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

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/ArdalanAskarian/ArdalanAskarian/output/github-snake-dark.svg">
  <img src="https://raw.githubusercontent.com/ArdalanAskarian/ArdalanAskarian/output/github-snake.svg" width="880" alt="Contribution graph rendered as a snake animation">
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://github-readme-stats.vercel.app/api?username=ArdalanAskarian&show_icons=true&include_all_commits=true&count_private=true&border_color=24272e&bg_color=16181d&title_color=eceff0&text_color=c2c6cd&icon_color=8a8f99">
  <img height="165" alt="GitHub statistics" src="https://github-readme-stats.vercel.app/api?username=ArdalanAskarian&show_icons=true&include_all_commits=true&count_private=true&border_color=e6e7ea&bg_color=ffffff&title_color=14161c&text_color=3b3f49&icon_color=666b75">
</picture>

## Let's talk.

I'm looking for full-time software and machine learning roles, and I'm interested in research collaborations in computer vision. I answer every email.

[ardalan.askarian@usask.ca](mailto:ardalan.askarian@usask.ca) · [GitHub](https://github.com/ArdalanAskarian) · [LinkedIn](https://linkedin.com/in/ardalan-askarian-79221a24b) · [Portfolio](https://ardalanaskarian.github.io) · [Résumé](https://ardalanaskarian.github.io/icons/resume.pdf)

<sub>Saskatoon, SK. Figures are built by <a href="tools/build_svg.py">tools/build_svg.py</a> from the same tokens as <a href="https://ardalanaskarian.github.io">the portfolio</a>: system fonts, one neutral ramp, and colour reserved for links.</sub>
