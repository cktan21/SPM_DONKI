# SPM_DONKI


## Presentation Documents


## Prerequisite
IDE (Any) <br>
bun (Package Manager) <br>
Github Desktop (If you prefer else CLI) <br>
Docker <br>

### Setup
```bash
# Installing Bun
npm install -g bun # the last `npm` command you'll ever need
```

## Instructions

Switch to your branch before starting to code <br>

> Local Setup, ensure Docker Desktop is running
1. Open a terminal and run the following command:

```bash
cd backend
docker-compose up -d --build
docker-compose down
```
2. Open another terminal and run the following command:

```bash
cd frontend
bun i
bun run dev
```
<!-- 3. Setting up SonarQube (access on localhost:9000)
- default credentials username: `admin` password: `admin`

```bash
docker pull sonarqube:lts-community
docker run -d --name sonarqube -p 9000:9000 sonarqube:lts-community
``` -->

## Technical Architecture Diagram
<img width="1195" height="911" alt="image" src="https://github.com/user-attachments/assets/3a79e6c4-eba5-40c2-af26-ebf8b520f63e" />


## Notable Technical Implementations
### Backend
- <b>Microservice Archictecture</b>
- <b>Loosely Coupled</b> Atomic Microservices
- Variety of <b>Languages and Frameworks and Runtimes</b> to show <b>Language Agnostic</b> properties in Microservices
- <b>RabbitMQ as message broker</b> for real time changes
- Websocket as message consumer of RabbitMQ
- <b>Kong API Gateway</b> for aggregating requests and routing
- <b>Grafana + Prometheus</b> for data ingestion and monitoring of microservices and Kong
- <b>CI/CD pipeline</b> to automate Image and Container building on Cloud
- <b>CI/CD pipeline</b> to run automated static code testing with Snyk and Checkov

### Frontend
- Vue + Nuxt + TypeScript
- Supabase Authentication for user accounts

## Frameworks and Databases Utilised

<p align="center"><strong>UI Stack</strong></p>
<p align="center">
<a href="https://www.typescriptlang.org/"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/4/4c/Typescript_logo_2020.svg/1200px-Typescript_logo_2020.svg.png" alt="TypeScript" width="40"/></a>&nbsp;&nbsp;
<a href="https://vuejs.org/"><img src="https://upload.wikimedia.org/wikipedia/commons/9/95/Vue.js_Logo_2.svg" alt="Vue" width="40"/></a>  
<a href="https://nuxt.com/"><img src="https://nuxt.com/assets/design-kit/icon-green.svg" alt="Nuxt" width="50"/></a>  
<!-- <a href="https://tailwindcss.com/"><img src="https://upload.wikimedia.org/wikipedia/commons/d/d5/Tailwind_CSS_Logo.svg" alt="Tailwind" width="30"/></a>&nbsp;&nbsp; -->
<!-- <a href="https://ui.shadcn.com/"><img src="https://github.com/user-attachments/assets/dd2eb75e-28c6-46e5-bb11-734e9e9a04f3" alt="ShadCN" width="30"/></a>&nbsp;&nbsp; -->
<a href="https://supabase.com/auth"><img src="https://www.vectorlogo.zone/logos/supabase/supabase-icon.svg" alt="Supabase" width="40"/></a>&nbsp;&nbsp;
<a href="https://bun.sh/"><img src="https://bun.sh/logo.svg" alt="Bun" width="55"/></a>&nbsp;&nbsp;
<br>
<i>TypeScript · Vue · Nuxt · Supabase Auth · Bun</i>
</p>
<br>

<p align="center"><strong>Microservices Languages</strong></p>
<p align="center">
<a href="https://developer.mozilla.org/en-US/docs/Web/JavaScript"><img src="https://upload.wikimedia.org/wikipedia/commons/6/6a/JavaScript-logo.png" alt="JavaScript" width="40"/></a>&nbsp;&nbsp;
<a href="https://www.typescriptlang.org/"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/4/4c/Typescript_logo_2020.svg/1200px-Typescript_logo_2020.svg.png" alt="TypeScript" width="40"/></a>&nbsp;&nbsp;
<a href="https://www.python.org/"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/1024px-Python-logo-notext.svg.png" alt="Python" width="40"/></a>&nbsp;&nbsp;
<br>
<i>JavaScript · TypeScript · Python</i>
</p>
<br>

<p align="center"><strong>Microservices Frameworks</strong></p>
<p align="center">
<a href="https://hono.dev/"><img src="https://upload.wikimedia.org/wikipedia/commons/6/60/Hono-logo.svg" alt="Hono" width="50"/></a>&nbsp;&nbsp;
<a href="https://fastapi.tiangolo.com/"><img src="https://upload.wikimedia.org/wikipedia/commons/1/1a/FastAPI_logo.svg" alt="FastAPI" width="120"/></a>&nbsp;&nbsp;
<br>
<i>Hono · FastAPI</i>
</p>
<br>

<p align="center"><strong>API Gateway</strong></p>
<p align="center">
<a href="https://konghq.com/"><img src="https://konghq.com/wp-content/uploads/2018/08/kong-combination-mark-color-256px.png" alt="Kong API Gateway" width="88"/></a>
<br>
<i>CORS · Rate Limit Plugin </i>
</p>
<br>  

<p align="center"><strong>Storage Solutions</strong></p>  
<p align="center">
<a href="https://supabase.com/"><img src="https://www.vectorlogo.zone/logos/supabase/supabase-icon.svg" alt="Supabase" width="40" /></a>&nbsp;&nbsp;
<br>
<i>Supabase</i>
</p>
<br> 

<p align="center"><strong>DevSecOps and Site Reliability</strong></p>
<p align="center">
<a href="https://github.com/features/actions"><img src="https://github.com/user-attachments/assets/84046b86-7745-4ddd-8c36-b39b6a9ead91" alt="GitHub Actions" width="60"/></a>&nbsp;&nbsp;
<a href="https://snyk.io/"><img src="https://github.com/user-attachments/assets/f35638ce-2ad1-4664-9cf1-e219222ca4f0" alt="Snyk" width="120"/></a>&nbsp;&nbsp;
<a href="https://grafana.com/"><img src="https://upload.wikimedia.org/wikipedia/commons/a/a1/Grafana_logo.svg" alt="Grafana" width="60"/></a>&nbsp;&nbsp;
<a href="https://prometheus.io/"><img src="https://upload.wikimedia.org/wikipedia/commons/3/38/Prometheus_software_logo.svg" alt="Prometheus" width="60"/></a>&nbsp;&nbsp;
<br>
<i>Github Actions · Snyk · Grafana · Prometheus</i>
</p> 
<br>

<p align="center"><strong>Other Technologies</strong></p>
<p align="center">
<a href="https://www.docker.com/"><img src="https://upload.wikimedia.org/wikipedia/commons/4/4e/Docker_%28container_engine%29_logo.svg" alt="Docker" width="150"/></a>&nbsp;&nbsp;
</p>
<p align="center">
<i>Docker Compose · Docker Hub</i>
</p>
<br> 

## Contributors

**Team 8**

<div align="center">
    <table>
        <tr>
            <th><a href="https://hsr.hoyoverse.com/en-us/">Shu Wen</a></th>
            <th><a href="https://zenless.hoyoverse.com/en-us/">Jun Wei</a></th>
            <th><a href="https://zenless.hoyoverse.com/en-us/">Rui Chen</a></th>
            <th><a href="https://www.linkedin.com/in/kevin-tan-513a9b207/">Kevin</a></th>
            <th><a href="https://zenless.hoyoverse.com/en-us/">Ashley</a></th>
            <th><a href="https://www.linkedin.com/in/joelynchuawl/">Joelyn</a></th>
        </tr>
        <tr>
            <td><img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQWBImo3QArAue--WOdbkcCsmabXCLvPXyxRA&s" alt="Shu Wen" width="120" height="120" style="display:block; margin:0 auto;"></td>
            <td><img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSAazBpLPvB3v_fJo5-74AbncYHsjjMom2TNA&s" alt="Jun Wei" width="120" height="120" style="display:block; margin: 0 auto;"></td>
            <td><img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSAazBpLPvB3v_fJo5-74AbncYHsjjMom2TNA&s" alt="Rui Chen" width="120" height="120" style="display:block; margin: 0 auto;"></td>
            <td><img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSAazBpLPvB3v_fJo5-74AbncYHsjjMom2TNA&s" alt="Kevin" width="120" height="120" style="display:block; margin: 0 auto;"</td>
            <td><img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSAazBpLPvB3v_fJo5-74AbncYHsjjMom2TNA&s" alt="Ashley" width="120" height="120" style="display:block; margin: 0 auto;"</td>
            <td><img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQWBImo3QArAue--WOdbkcCsmabXCLvPXyxRA&s" alt="Joelyn" width="120" height="120" style="display:block; margin: 0 auto;"></td>
        </tr>
    </table>
</div>
