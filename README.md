<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->

[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/github_username/repo_name">
    <img src="images/logo.png" alt="Logo" width="40" height="40">
  </a>

  <h3 align="center">Log Ingestor Interface</h3>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#run-application">Run Application</a></li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project
This application provides the capability of filtering the logs available in the system with the below filters -

<ol>
  <li>Level</li>
  <li>Message</li>   
  <li>Timestamp</li>
  <li>ResourceId</li>
  <li>TraceId</li>
  <li>SpanId</li>
  <li>Commit</li>
  <li>ParentResourceId</li>
</ol>

<h3>This project uses</h3>
<ul>
  <li>Full Test Search functionality of sqlite3 database for filtering the logs based on Message.</li>
  <li>Indexing for the other filters like Level, Timestamp, ResourceId, TraceId, SpanId, Commit and ParentResourceId.</li>
</ul>


[![Product Name Screen Shot][product-screenshot]](http://localhost:3000/)



### Built With

[![HTML][Html-Url]](https://developer.mozilla.org/en-US/docs/Web/HTML)
[![JavaScript][Javascript-Url]](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[![Bootstrap][Bootstrap-Url]](https://getbootstrap.com/)
[![jQuery][JQuery-Url]](https://jquery.com/)
[![Python][Python-url]](https://www.python.org/)
[![Flask][Flask-url]](https://flask.palletsprojects.com/)



<!-- GETTING STARTED -->
## Getting Started

This application gives us the capability of filtering the logs available in the syatem with the below filters -

<ol>
  <li>Level</li>
  <li>Message</li>   
  <li>Timestamp</li>
  <li>ResourceId</li>
  <li>TraceId</li>
  <li>SpanId</li>
  <li>Commit</li>
  <li>ParentResourceId</li>
</ol>

### Prerequisites

Install and download the below packages.
<ol>
  
  <li>Install Dependencies:</li>

```sh
pip install requirements.txt
```
</li>

<li>Download and install Python from <a href="https://www.python.org/">Here</a></li>
</ol>



## Run Application
### Development Mode
```
$ python src/ingestor.py
```
In flask, Default port is `3000`


<!-- USAGE EXAMPLES -->
## Usage
At Home page, All the logs will be populated without any filter and Level radio button will be checked by default.
<h3>Apply Filter</h3>
<ol>
  <li>This feature gives an option to display the logs based on the filter selected.</li>
  <li>Depends on the filter applied, a dynamic user-input will be displayed which accepts the filter value and fetches the logs available from the database.</li>
</ol>

<h3>Advance Search</h3>
<ol>
  <li>This is an extended functionality of 'Apply Filter' functionality where you can combine multiple filter in one search, depending on the user selected filter, logs will be displayed into the UI.</li>
</ol>

## Project Struture

```
.
|──────project/
| |──── images/
| | |──── screenshot.png
| |──── src/
| | |────ingestor.py
| | |────loggerDb.db
| |──── templates/
| | |────home.html
| | |────index.html
| |────README.md
| |────LICENSE.txt
| |──── requirements.txt

```

 
<!-- CONTACT -->
## Contact

[![LinkedIn][linkedin-shield]][linkedin-url]
[![Gmail](https://img.shields.io/badge/Gmail-D14836?style=for-the-badge&logo=gmail&logoColor=white)](https://mail.google.com/) abhishekkr4drive@gmail.com






<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/github_username/repo_name.svg?style=for-the-badge
[contributors-url]: https://github.com/github_username/repo_name/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/github_username/repo_name.svg?style=for-the-badge
[forks-url]: https://github.com/github_username/repo_name/network/members
[stars-shield]: https://img.shields.io/github/stars/github_username/repo_name.svg?style=for-the-badge
[stars-url]: https://github.com/github_username/repo_name/stargazers
[issues-shield]: https://img.shields.io/github/issues/github_username/repo_name.svg?style=for-the-badge
[issues-url]: https://github.com/github_username/repo_name/issues
[license-shield]: https://img.shields.io/github/license/github_username/repo_name.svg?style=for-the-badge
[license-url]: https://github.com/github_username/repo_name/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/abhis2007/
[product-screenshot]: images/screenshot.png
[Python-url]: https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[Flask-url]: https://img.shields.io/badge/Flask-20232A?style=for-the-badge&logo=flask&logoColor=white
[Python-url]: https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white
[Html-Url]: https://img.shields.io/badge/HTML-239120?style=for-the-badge&logo=html5&logoColor=white
[Javascript-Url]: https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black
[JQuery-Url]: https://img.shields.io/badge/jQuery-3.6.4-0769ad?style=flat&logo=jquery&logoColor=white
[Bootstrap-Url]: https://img.shields.io/badge/Bootstrap-5.3.2-563d7c?style=flat&logo=bootstrap&logoColor=white
[React-url]: https://reactjs.org/
[Vue.js]: https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D
[Vue-url]: https://vuejs.org/
[Angular.io]: https://img.shields.io/badge/Angular-DD0031?style=for-the-badge&logo=angular&logoColor=white
[Angular-url]: https://angular.io/
[Svelte.dev]: https://img.shields.io/badge/Svelte-4A4A55?style=for-the-badge&logo=svelte&logoColor=FF3E00
[Svelte-url]: https://svelte.dev/
[Laravel.com]: https://img.shields.io/badge/Laravel-FF2D20?style=for-the-badge&logo=laravel&logoColor=white
[Laravel-url]: https://laravel.com
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
[JQuery.com]: https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white
[JQuery-url]: https://jquery.com 
